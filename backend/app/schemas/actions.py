from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class MatchRequestCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")

	full_name: str = Field(min_length=2, max_length=120)
	email: EmailStr
	consent: bool
	website: str = Field(default="", max_length=300)

	@field_validator("full_name", mode="before")
	@classmethod
	def trim_name(cls, value: object) -> object:
		return value.strip() if isinstance(value, str) else value

	@model_validator(mode="after")
	def require_consent(self) -> "MatchRequestCreate":
		if not self.consent:
			raise ValueError("Consent is required to request a match")
		return self


class SpiritualNoteCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")

	display_name: str | None = Field(default=None, max_length=80)
	message: str = Field(min_length=5, max_length=1200)
	consent: bool
	website: str = Field(default="", max_length=300)

	@field_validator("display_name", "message", mode="before")
	@classmethod
	def trim_text(cls, value: object) -> object:
		return value.strip() if isinstance(value, str) else value

	@model_validator(mode="after")
	def require_consent(self) -> "SpiritualNoteCreate":
		if not self.consent:
			raise ValueError("Consent is required to submit a note")
		return self


class ContributionCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")

	action_type: Literal["prayer", "good_deed"]
	idempotency_key: UUID


class MatchDrawRequest(BaseModel):
	model_config = ConfigDict(extra="forbid")

	visitor_id: UUID


class VolunteerActionCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")

	visitor_id: UUID
	action_type: Literal["prayer", "good_deed", "note", "share"]
	idempotency_key: UUID
	content: str | None = Field(default=None, max_length=1200)

	@field_validator("content", mode="before")
	@classmethod
	def trim_content(cls, value: object) -> object:
		return value.strip() if isinstance(value, str) else value

	@model_validator(mode="after")
	def validate_note(self) -> "VolunteerActionCreate":
		if self.action_type == "note" and not (self.content and len(self.content) >= 3):
			raise ValueError("A note must contain at least 3 characters")
		if self.action_type != "note" and self.content:
			raise ValueError("Only note actions can contain text")
		return self


class ActionReceipt(BaseModel):
	accepted: bool
	status: Literal["pending", "recorded", "duplicate"]
	prayers_count: int = Field(ge=0)
	good_deeds_count: int = Field(ge=0)