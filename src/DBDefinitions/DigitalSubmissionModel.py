import datetime
from typing import Optional, List
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

class DigitalSubmissionModel(BaseModel):
    __tablename__ = "digital_submissions"

    form_id: Mapped[IDType] = mapped_column(ForeignKey("digital_forms.id"), default=None, nullable=True)

    # # A computed property for all submitted sections (placeholder returning empty list)
    # @property
    # def submitted_sections_all(self) -> Optional[List["DigitalSubmissionSectionModel"]]:
    #     return []

    parent_id: Mapped[IDType] = UUIDFKey()
    
    # Relationship to submitted sections; assumes DigitalSubmissionSectionModel has a column "submission_id"
    submitted_sections = relationship(
        "DigitalSubmissionSectionModel",
        # back_populates="submission",
        primaryjoin="DigitalSubmissionSectionModel.submission_id==DigitalSubmissionModel.id",
        cascade="all, delete-orphan",
        lazy="select"
    )

    # Relationship to submitted fields; assumes DigitalSubmissionFieldModel has a column "submission_id"
    submitted_fields = relationship(
        "DigitalSubmissionFieldModel",
        # back_populates="submission",
        primaryjoin="DigitalSubmissionFieldModel.submission_id==DigitalSubmissionModel.id",
        cascade="all, delete-orphan",
        lazy="select"
    )