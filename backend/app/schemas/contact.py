from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class ContactMessageCreate(BaseModel):
	model_config = ConfigDict(extra="forbid")

	name: str = Field(min_length=2, max_length=120)
	email: EmailStr
	subject: str = Field(min_length=3, max_length=120)
	message: str = Field(min_length=10, max_length=3000)
	consent: bool
	website: str = Field(default="", max_length=300)

	@field_validator("name", "subject", "message", mode="before")
	@classmethod
	def trim_text_fields(cls, value: object) -> object:
		return value.strip() if isinstance(value, str) else value

	@model_validator(mode="after")
	def require_consent(self) -> "ContactMessageCreate":
		if not self.consent:
			raise ValueError("Consent is required to send a message")
		return self