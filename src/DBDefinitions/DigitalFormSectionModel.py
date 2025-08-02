import datetime
from typing import Optional, List
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
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

class DigitalFormSectionModel(BaseModel):
    __tablename__ = "digital_form_sections"

    path_attribute_name = "path"
    parent_attribute_name = "section"
    parent_id_attribute_name = "section_id"
    children_attribute_name = "sections"

    # Materialized path technique
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique, not implemented"
    )

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    label: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    label_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    order: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
    repatable_min: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
    repatable_max: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
    repeatable: Mapped[Optional[bool]] = mapped_column(Boolean, default=None, nullable=True)

    section_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_form_sections.id"), default=None, nullable=True)
    form_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("digital_forms.id"), default=None, nullable=True)

    # Relationship: child sections (self-referential)
    sections = relationship(
        "DigitalFormSectionModel",
        back_populates="section",
        uselist=True,
        init=True,
        cascade="save-update",
    )

    section = relationship(
        "DigitalFormSectionModel",
        remote_side="DigitalFormSectionModel.id",
        back_populates="sections",
        uselist=False
    )

    # Relationship: fields within this section.
    fields = relationship(
        "DigitalFormFieldModel",
        primaryjoin="DigitalFormFieldModel.form_section_id==DigitalFormSectionModel.id",
        # backref="form_section",
        uselist=True,
        init=True,
        cascade="save-update",
    )

    # @property
    # def parent(self) -> Optional[object]:
    #     """
    #     Returns the parent for this section.
    #     This property attempts to load a parent DigitalFormSectionModel first;
    #     if not found, you could extend this to attempt loading a DigitalFormModel.
    #     """
    #     # If parent_section relationship is set by backref, return it.
    #     # Otherwise, custom logic (e.g. querying DigitalFormModel) could be added.
    #     return self.parent_section  # May be None if not set.
