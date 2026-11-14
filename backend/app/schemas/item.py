from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PrisonerSummary(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	slug: str
	name: str
	profession: str
	short_bio: str
	status: str
	image_url: str | None
	is_demo: bool
	is_matched: bool


class PrisonerDetail(PrisonerSummary):
	biography: str
	dreams: str | None
	prayers_count: int = Field(ge=0)
	good_deeds_count: int = Field(ge=0)
	created_at: datetime
	approved_notes: list[dict[str, str]] = Field(default_factory=list)


class PrisonerList(BaseModel):
	items: list[PrisonerSummary]
	total: int
	page: int
	page_size: int
	matched_count: int = Field(ge=0)
