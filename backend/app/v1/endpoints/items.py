from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.actions import ActionReceipt, ContributionCreate, MatchRequestCreate, SpiritualNoteCreate
from app.schemas.item import PrisonerDetail, PrisonerList, PrisonerSummary
from app.services.action_guide import build_action_guide_pdf
from app.services.item_service import (
	create_match_request,
	create_spiritual_note,
	get_prisoner_by_slug,
	list_approved_notes,
	list_prisoners,
	record_contribution,
)

router = APIRouter(prefix="/prisoners", tags=["prisoners"])


@router.get("")
async def read_prisoners(
	page: int = Query(default=1, ge=1),
	page_size: int = Query(default=12, ge=1, le=100),
	search: str | None = Query(default=None, max_length=100),
	status_filter: str | None = Query(default=None, alias="status", max_length=40),
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	prisoners, total, matched_count = await list_prisoners(
		session,
		page=page,
		page_size=page_size,
		search=search,
		status=status_filter,
	)
	items = []
	for prisoner in prisoners:
		item = PrisonerSummary.model_validate(prisoner)
		if prisoner.image_data:
			item.image_url = f"/api/v1/prisoners/{prisoner.slug}/image"
		items.append(item)
	data = PrisonerList(
		items=items,
		total=total,
		page=page,
		page_size=page_size,
		matched_count=matched_count,
	)
	return {"success": True, "data": data.model_dump(mode="json"), "error": None}


@router.get("/{slug}")
async def read_prisoner(
	slug: str, session: AsyncSession = Depends(get_db)
) -> dict[str, object]:
	prisoner = await get_prisoner_by_slug(session, slug)
	if prisoner is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Prisoner profile was not found",
		)
	data = PrisonerDetail.model_validate(prisoner)
	response_data = data.model_dump(mode="json")
	if prisoner.image_data:
		response_data["image_url"] = f"/api/v1/prisoners/{prisoner.slug}/image"
	response_data["approved_notes"] = await list_approved_notes(session, prisoner.id)
	return {"success": True, "data": response_data, "error": None}


@router.get("/{slug}/image", include_in_schema=False)
async def read_prisoner_image(
	slug: str, session: AsyncSession = Depends(get_db)
) -> Response:
	prisoner = await get_prisoner_by_slug(session, slug)
	if prisoner is None or not prisoner.image_data or not prisoner.image_media_type:
		raise HTTPException(status_code=404, detail="Profile illustration was not found")
	return Response(
		content=prisoner.image_data,
		media_type=prisoner.image_media_type,
		headers={"Cache-Control": "public, max-age=3600"},
	)


@router.get("/{slug}/action-guide/pdf", tags=["resources"])
async def download_action_guide(
	slug: str, session: AsyncSession = Depends(get_db)
) -> Response:
	prisoner = await get_prisoner_by_slug(session, slug)
	if prisoner is None:
		raise HTTPException(status_code=404, detail="Profile was not found")
	if not prisoner.is_matched:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="The guide becomes available after a match is approved",
		)
	return Response(
		content=build_action_guide_pdf(),
		media_type="application/pdf",
		headers={"Content-Disposition": 'attachment; filename="identity-chain-eylem-rehberi.pdf"'},
	)


@router.post("/{slug}/match-requests", status_code=status.HTTP_202_ACCEPTED)
async def request_match(
	slug: str,
	payload: MatchRequestCreate,
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	prisoner = await get_prisoner_by_slug(session, slug)
	if prisoner is None:
		raise HTTPException(status_code=404, detail="Prisoner profile was not found")
	if payload.website:
		return {"success": True, "data": {"status": "pending"}, "error": None}
	if not prisoner.is_demo:
		raise HTTPException(
			status_code=403,
			detail="Match requests are disabled for real profiles until identity, consent, and rate-limit controls are active",
		)
	if prisoner.is_matched:
		raise HTTPException(status_code=409, detail="This profile is already matched")
	await create_match_request(
		session,
		prisoner=prisoner,
		full_name=payload.full_name,
		email=str(payload.email),
		consent=payload.consent,
	)
	return {
		"success": True,
		"data": {"status": "pending", "message": "Talebiniz ekip incelemesine alındı."},
		"error": None,
	}


@router.post("/{slug}/notes", status_code=status.HTTP_202_ACCEPTED)
async def submit_spiritual_note(
	slug: str,
	payload: SpiritualNoteCreate,
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	prisoner = await get_prisoner_by_slug(session, slug)
	if prisoner is None:
		raise HTTPException(status_code=404, detail="Prisoner profile was not found")
	if payload.website:
		return {"success": True, "data": {"status": "pending"}, "error": None}
	if not prisoner.is_demo:
		raise HTTPException(
			status_code=403,
			detail="Public notes are disabled for real profiles until identity, consent, and moderation controls are active",
		)
	await create_spiritual_note(
		session,
		prisoner=prisoner,
		display_name=payload.display_name,
		message=payload.message,
		consent=payload.consent,
	)
	return {
		"success": True,
		"data": {"status": "pending", "message": "Notunuz yayınlanmadan önce moderasyon ekibi tarafından incelenecek."},
		"error": None,
	}


@router.post("/{slug}/contributions", response_model=dict[str, object])
async def add_contribution(
	slug: str,
	payload: ContributionCreate,
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	prisoner = await get_prisoner_by_slug(session, slug)
	if prisoner is None:
		raise HTTPException(status_code=404, detail="Prisoner profile was not found")
	if not prisoner.is_demo:
		raise HTTPException(
			status_code=403,
			detail="Public contribution counters are enabled for demo profiles only until abuse protection is deployed",
		)
	created, prayers_count, good_deeds_count = await record_contribution(
		session,
		prisoner=prisoner,
		action_type=payload.action_type,
		idempotency_key=payload.idempotency_key,
	)
	data = ActionReceipt(
		accepted=True,
		status="recorded" if created else "duplicate",
		prayers_count=prayers_count,
		good_deeds_count=good_deeds_count,
	)
	return {"success": True, "data": data.model_dump(mode="json"), "error": None}
