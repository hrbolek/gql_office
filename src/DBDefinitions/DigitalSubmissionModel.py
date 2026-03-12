import datetime
from typing import Optional, List
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    select
)
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, foreign

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class DigitalSubmissionModel(BaseModel):
    __tablename__ = "digital_submissions"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="name of the submission, can be used as folder name")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="name of the submission, can be used as folder name")

    form_id: Mapped[IDType] = mapped_column(ForeignKey("digital_forms.id"), default=None, nullable=True)
    state_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)

    # # A computed property for all submitted sections (placeholder returning empty list)
    # @property
    # def submitted_sections_all(self) -> Optional[List["DigitalSubmissionSectionModel"]]:
    #     return []

    # parent_id: Mapped[IDType] = UUIDFKey()
    parent_id: Mapped[IDType] = mapped_column(ForeignKey("digital_submissions.id"), default=None, nullable=True)
    # parent = relationship(
    #     "DigitalSubmissionModel",
    #     # back_populates="submission",
    #     primaryjoin=lambda: foreign(DigitalSubmissionModel.parent_id)==DigitalSubmissionModel.id,
    #     remote_side=lambda: DigitalSubmissionModel.id,
    #     viewonly=True,
    #     # cascade="all, delete-orphan",
    #     lazy="select"
    # )

    # Relationship to parent document.
    parent = relationship(
        "DigitalSubmissionModel",
        remote_side="DigitalSubmissionModel.id",
        primaryjoin="DigitalSubmissionModel.parent_id==DigitalSubmissionModel.id",
        back_populates="children",
        uselist=False
    )
    
    # Relationship to child document.
    children = relationship(
        "DigitalSubmissionModel",
        back_populates="parent",
        uselist=True,
        init=True,
        cascade="save-update",
    )

    form = relationship(
        "DigitalFormModel",
        # back_populates="submission",
        primaryjoin="DigitalSubmissionModel.form_id==DigitalFormModel.id",
        viewonly=True,
        # remote_side="DigitalFormModel.id",
        # cascade="all, delete-orphan",
        lazy="select"
    )

    # Relationship to submitted sections; assumes DigitalSubmissionSectionModel has a column "submission_id"
    sections = relationship(
        "DigitalSubmissionSectionModel",
        init=True,
        # back_populates="submission",
        primaryjoin="DigitalSubmissionSectionModel.submission_id==DigitalSubmissionModel.id",
        # cascade="all, delete-orphan",
        cascade="save-update",
        # viewonly=True,
        collection_class=list,
        lazy="select"
    )

    # Relationship to submitted fields; assumes DigitalSubmissionFieldModel has a column "submission_id"
    fields = relationship(
        "DigitalSubmissionFieldModel",
        # back_populates="submission",
        primaryjoin="DigitalSubmissionFieldModel.submission_id==DigitalSubmissionModel.id",
        # cascade="all, delete-orphan",
        viewonly=True,
        lazy="select"
    )

    request = relationship(
        "RequestModel",
        remote_side="RequestModel.active_submission_id",
        uselist=False,
        init=False,
        viewonly=True
    )

async def load_submission_dataset(session, submission_id):
    from .DigitalSubmissionSectionModel import DigitalSubmissionSectionModel as SubSec
    from .DigitalSubmissionFieldModel import DigitalSubmissionFieldModel as SubField

    sec_stmt = select(SubSec).where(SubSec.submission_id == submission_id)
    fld_stmt = select(SubField).where(SubField.submission_id == submission_id)

    sec_res = await session.execute(sec_stmt)
    fld_res = await session.execute(fld_stmt)

    submission_sections = list(sec_res.scalars())
    submission_fields = list(fld_res.scalars())
    return submission_sections, submission_fields