import datetime
from typing import List, Optional
from sqlalchemy import (
    Column,
    String,
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

class DigitalFormModel(BaseModel):
    __tablename__ = "digital_forms"
    

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    
    state_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)

    parent_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_forms.id"), default=None, nullable=True, comment="Document parent id")
    type_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("document_types.id"), default=None, nullable=True)
    # Relationship to a DocumentType model. Adjust foreign key target as needed.
    type_ = relationship(
        "DocumentTypeModel",
        primaryjoin="DigitalFormModel.type_id==DocumentTypeModel.id",
        uselist=False,
        viewonly=True
    )

    # Relationship to form sections.
    # We assume that the DigitalFormSectionModel has a column named "document_id"
    # that refers to this form's id.
    sections = relationship(
        "DigitalFormSectionModel",
        primaryjoin="DigitalFormModel.id==DigitalFormSectionModel.form_id",
        # back_populates="form",
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    # Relationship to form submissions.
    # We assume that the DigitalSubmissionModel has a column named "document_id"
    # that refers to this form's id.
    submissions = relationship(
        "DigitalSubmissionModel",
        primaryjoin="DigitalFormModel.id==DigitalSubmissionModel.form_id",
        # back_populates="form",
        cascade="all, delete-orphan",
        lazy="select"
    )