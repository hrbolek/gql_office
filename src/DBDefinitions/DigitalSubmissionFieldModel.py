import datetime
from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class DigitalSubmissionFieldModel(BaseModel):
    """Represents a response for a specific form field within a submission.
    Links the user's provided value with the corresponding form field.
    """
    __tablename__ = "digital_submission_fields"

    id: Mapped[IDType] = mapped_column(primary_key=True, default=None, nullable=True)
    path: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    value: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    field_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_form_fields.id"), default=None, nullable=True)
    section_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_submission_sections.id"), default=None, nullable=True)
    submission_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_submissions.id"), default=None, nullable=True)
    state_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)
