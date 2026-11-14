from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.item import ContactMessage
from app.schemas.contact import ContactMessageCreate

router = APIRouter(prefix="/contact-messages", tags=["contact"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_contact_message(
	payload: ContactMessageCreate,
	session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
	if payload.website:
		return {
			"success": True,
			"data": {"received": True},
			"error": None,
		}

	contact_message = ContactMessage(
		name=payload.name.strip(),
		email=str(payload.email),
		subject=payload.subject.strip(),
		message=payload.message.strip(),
		consent=payload.consent,
	)
	session.add(contact_message)
	await session.commit()
	return {
		"success": True,
		"data": {"received": True},
		"error": None,
	}