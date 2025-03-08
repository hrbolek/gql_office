import datetime
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

class DigitalFormFieldModel(BaseModel):
    __tablename__ = "digital_form_fields"

    # Primary key (if you have an id column, you might want to include it)
    id: Mapped[IDType] = mapped_column(primary_key=True, default=None, nullable=True)

    name: Mapped[str] = mapped_column(String, default=None, nullable=True)
    label: Mapped[str] = mapped_column(String, default=None, nullable=True)
    label_en: Mapped[str] = mapped_column(String, default=None, nullable=True)
    description: Mapped[str] = mapped_column(String, default=None, nullable=True)

    required: Mapped[bool] = mapped_column(default=None, nullable=True)
    order: Mapped[int] = mapped_column(default=None, nullable=True)
    computed: Mapped[int] = mapped_column(default=None, nullable=True)

    formula: Mapped[str] = mapped_column(String, default=None, nullable=True)

    # Foreign key references (but here declared simply as nullable columns)
    form_section_id: Mapped[IDType] = mapped_column(ForeignKey("digital_form_sections.id"), default=None, nullable=True)
    form_id: Mapped[IDType] = mapped_column(ForeignKey("digital_forms.id"), default=None, nullable=True)

    type_id: Mapped[IDType] = mapped_column(default=None, nullable=True)
    backend_formula: Mapped[str] = mapped_column(String, default=None, nullable=True)
    flatten_formula: Mapped[str] = mapped_column(String, default=None, nullable=True)