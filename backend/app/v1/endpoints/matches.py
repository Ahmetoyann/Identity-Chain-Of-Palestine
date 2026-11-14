from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.actions import MatchDrawRequest, VolunteerActionCreate
from app.schemas.item import PrisonerSummary
from app.services.action_guide import build_action_guide_pdf
from app.services.item_service import draw_demo_match, get_active_volunteer_match, record_volunteer_action
from fastapi.responses import Response

router = APIRouter(prefix="/matches", tags=["volunteer matches"])


@router.post("/draw", status_code=status.HTTP_201_CREATED)
async def draw_match(
	payload: MatchDrawRequest,
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	result = await draw_demo_match(session, payload.visitor_id)
	if result is None:
		raise HTTPException(status_code=503, detail="No representative profiles are currently available")
	match, prisoner = result
	profile = PrisonerSummary.model_validate(prisoner).model_dump(mode="json")
	if prisoner.image_data:
		profile["image_url"] = f"/api/v1/prisoners/{prisoner.slug}/image"
	return {
		"success": True,
		"data": {
			"match_id": str(match.id),
			"visitor_id": str(match.visitor_id),
			"status": match.status,
			"prisoner": profile,
		},
		"error": None,
	}


@router.post("/{match_id}/actions")
async def create_match_action(
	match_id: UUID,
	payload: VolunteerActionCreate,
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	result = await record_volunteer_action(
		session,
		match_id=match_id,
		visitor_id=payload.visitor_id,
		action_type=payload.action_type,
		content=payload.content,
		idempotency_key=payload.idempotency_key,
	)
	if result is None:
		raise HTTPException(status_code=404, detail="Active representative match was not found")
	created, prayers_count, good_deeds_count = result
	return {
		"success": True,
		"data": {
			"status": "recorded" if created else "duplicate",
			"prayers_count": prayers_count,
			"good_deeds_count": good_deeds_count,
		},
		"error": None,
	}


@router.get("/{match_id}/action-guide.pdf", tags=["resources"])
async def download_matched_action_guide(
	match_id: UUID,
	visitor_id: UUID,
	session: AsyncSession = Depends(get_db),
) -> Response:
	match = await get_active_volunteer_match(session, match_id, visitor_id)
	if match is None:
		raise HTTPException(status_code=403, detail="Guide access requires your active representative match")
	return Response(
		content=build_action_guide_pdf(),
		media_type="application/pdf",
		headers={"Content-Disposition": 'attachment; filename="identity-chain-eylem-rehberi.pdf"'},
	)
