from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models.actions import Contribution, MatchRequest, SpiritualNote, VolunteerAction, VolunteerMatch
from app.models.item import Prisoner


async def list_prisoners(
	session: AsyncSession,
	*,
	page: int,
	page_size: int,
	search: str | None = None,
	status: str | None = None,
) -> tuple[list[Prisoner], int, int]:
	filters = [Prisoner.is_published.is_(True)]
	if search:
		search_term = f"%{search.strip()}%"
		filters.append(
			or_(
				Prisoner.name.ilike(search_term),
				Prisoner.profession.ilike(search_term),
				Prisoner.short_bio.ilike(search_term),
			)
		)
	if status:
		filters.append(Prisoner.status == status)

	total = await session.scalar(select(func.count()).select_from(Prisoner).where(*filters))
	result = await session.scalars(
		select(Prisoner)
		.where(*filters)
		.order_by(Prisoner.name, Prisoner.slug)
		.offset((page - 1) * page_size)
		.limit(page_size)
	)
	matched_count = await session.scalar(
		select(func.count(func.distinct(VolunteerMatch.prisoner_id))).where(
			VolunteerMatch.status == "active"
		)
	)
	return list(result), total or 0, matched_count or 0


async def get_prisoner_by_slug(
	session: AsyncSession, slug: str
) -> Prisoner | None:
	result = await session.scalars(
		select(Prisoner).where(
			Prisoner.slug == slug,
			Prisoner.is_published.is_(True),
		)
	)
	return result.one_or_none()


async def list_approved_notes(
	session: AsyncSession, prisoner_id: object
) -> list[dict[str, str]]:
	result = await session.execute(
		select(SpiritualNote.display_name, SpiritualNote.message)
		.where(
			SpiritualNote.prisoner_id == prisoner_id,
			SpiritualNote.status == "approved",
		)
		.order_by(SpiritualNote.created_at.desc())
		.limit(30)
	)
	return [
		{"display_name": display_name or "Gönüllü", "message": message}
		for display_name, message in result.all()
	]


async def create_match_request(
	session: AsyncSession, *, prisoner: Prisoner, full_name: str, email: str, consent: bool
) -> MatchRequest:
	request = MatchRequest(
		prisoner_id=prisoner.id,
		full_name=full_name,
		email=email,
		consent=consent,
		is_demo=prisoner.is_demo,
		status="pending",
	)
	session.add(request)
	await session.commit()
	return request


async def create_spiritual_note(
	session: AsyncSession,
	*,
	prisoner: Prisoner,
	display_name: str | None,
	message: str,
	consent: bool,
) -> SpiritualNote:
	note = SpiritualNote(
		prisoner_id=prisoner.id,
		display_name=display_name or None,
		message=message,
		consent=consent,
		status="pending",
	)
	session.add(note)
	await session.commit()
	return note


async def record_contribution(
	session: AsyncSession,
	*,
	prisoner: Prisoner,
	action_type: str,
	idempotency_key: object,
) -> tuple[bool, int, int]:
	prisoner_id = prisoner.id
	statement = (
		insert(Contribution)
		.values(
			prisoner_id=prisoner_id,
			action_type=action_type,
			idempotency_key=idempotency_key,
		)
		.on_conflict_do_nothing(index_elements=["idempotency_key"])
		.returning(Contribution.id)
	)
	contribution_id = await session.scalar(statement)
	if contribution_id is not None:
		counter_column = (
			Prisoner.prayers_count if action_type == "prayer" else Prisoner.good_deeds_count
		)
		await session.execute(
			update(Prisoner)
			.where(Prisoner.id == prisoner_id)
			.values({counter_column.key: counter_column + 1})
		)
		await session.flush()
	else:
		await session.flush()

	counters = await session.execute(
		select(Prisoner.prayers_count, Prisoner.good_deeds_count).where(
			Prisoner.id == prisoner_id
		)
	)
	prayers_count, good_deeds_count = counters.one()
	await session.commit()
	return contribution_id is not None, prayers_count, good_deeds_count


async def draw_demo_match(
	session: AsyncSession, visitor_id: object
) -> tuple[VolunteerMatch, Prisoner] | None:
	previous_profiles = select(VolunteerMatch.prisoner_id).where(
		VolunteerMatch.visitor_id == visitor_id
	)
	query = (
		select(Prisoner)
		.where(
			Prisoner.is_demo.is_(True),
			Prisoner.is_published.is_(True),
			~Prisoner.id.in_(previous_profiles),
		)
		.order_by(func.random())
		.limit(1)
		.with_for_update(skip_locked=True)
	)
	prisoner = await session.scalar(query)
	if prisoner is None:
		prisoner = await session.scalar(
			select(Prisoner)
			.where(Prisoner.is_demo.is_(True), Prisoner.is_published.is_(True))
			.order_by(func.random())
			.limit(1)
			.with_for_update(skip_locked=True)
		)
	if prisoner is None:
		return None

	match = VolunteerMatch(visitor_id=visitor_id, prisoner_id=prisoner.id, status="active")
	session.add(match)
	await session.commit()
	await session.refresh(match)
	return match, prisoner


async def record_volunteer_action(
	session: AsyncSession,
	*,
	match_id: object,
	visitor_id: object,
	action_type: str,
	content: str | None,
	idempotency_key: object,
) -> tuple[bool, int, int] | None:
	match = await session.scalar(
		select(VolunteerMatch).where(
			VolunteerMatch.id == match_id,
			VolunteerMatch.visitor_id == visitor_id,
			VolunteerMatch.status == "active",
		)
	)
	if match is None:
		return None

	statement = (
		insert(VolunteerAction)
		.values(
			match_id=match.id,
			action_type=action_type,
			content=content,
			idempotency_key=idempotency_key,
		)
		.on_conflict_do_nothing(constraint="uq_volunteer_action_idempotency")
		.returning(VolunteerAction.id)
	)
	created_id = await session.scalar(statement)
	if created_id and action_type in {"prayer", "good_deed"}:
		column = Prisoner.prayers_count if action_type == "prayer" else Prisoner.good_deeds_count
		await session.execute(
			update(Prisoner)
			.where(Prisoner.id == match.prisoner_id)
			.values({column.key: column + 1})
		)

	counters = await session.execute(
		select(Prisoner.prayers_count, Prisoner.good_deeds_count).where(
			Prisoner.id == match.prisoner_id
		)
	)
	prayers_count, good_deeds_count = counters.one()
	await session.commit()
	return created_id is not None, prayers_count, good_deeds_count


async def get_active_volunteer_match(
	session: AsyncSession, match_id: object, visitor_id: object
) -> tuple[VolunteerMatch, Prisoner] | None:
	result = await session.execute(
		select(VolunteerMatch, Prisoner)
		.join(Prisoner, Prisoner.id == VolunteerMatch.prisoner_id)
		.where(
			VolunteerMatch.id == match_id,
			VolunteerMatch.visitor_id == visitor_id,
			VolunteerMatch.status == "active",
			Prisoner.is_demo.is_(True),
		)
	)
	return result.one_or_none()
