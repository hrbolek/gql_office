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

class DigitalSubmissionSectionModel(BaseModel):
    __tablename__ = "digital_submission_sections"

    path: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    index: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
    # This column stores the parent section's id.
    section_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_submission_sections.id"), default=None, nullable=True)
    # This column references the submission owning this section.
    submission_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_submissions.id"), default=None, nullable=True)

    # Parent relationship (corresponds to the GraphQL field "section").
    section = relationship(
        "DigitalSubmissionSectionModel",
        remote_side="DigitalSubmissionSectionModel.id",
        # back_populates="child_sections",
        uselist=False
    )

    # Child sections relationship (corresponds to the GraphQL field "sections").
    child_sections = relationship(
        "DigitalSubmissionSectionModel",
        # back_populates="section",
        viewonly=True,
        cascade="all, delete-orphan",
        lazy="select"
    )

    # Relationship to the submission owning this section.
    submission = relationship(
        "DigitalSubmissionModel",
        # back_populates="sections",
        viewonly=True,
        uselist=False
    )

    # Relationship to the field (DigitalSubmissionFieldModel) associated with this section.
    fields = relationship(
        "DigitalSubmissionFieldModel",
        # back_populates="section",
        uselist=False
    )