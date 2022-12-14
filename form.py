import enum
from uuid import UUID

from pydantic import BaseModel, Field


class DueDiligenceFormQuestionEnum(enum.Enum):
    social_media = 'social_media'
    personal_data = 'personal_data'
    professional_data = 'professional_data'


class RepresentationActivityForm(BaseModel):
    """Representation activity form."""

    role: str = Field(alias='occupation')
    corporate_name: str = Field(description='')


class SocialNetworkForm(BaseModel):
    """Social Network form."""

    type: str = Field(alias='type')
    address: str = Field(description='Electronic address of the social network.')


class PersonForm(BaseModel):
    """Map a person's fields."""

    name: str | None
    age: int | None


class FormResponse(BaseModel):
    uuid: UUID
    person: PersonForm
    social_network: SocialNetworkForm
    professional_activity: RepresentationActivityForm
