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

from src.DBDefinitions.BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class DocumentModel(BaseModel):
    """
    Interface for a Document, either a DigitalDocument or a PhysicalDocument.
    This abstract model provides common fields.
    """
    __abstract__ = True

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    
    state_id: Mapped[Optional[IDType]] = mapped_column(default=None, nullable=True)
    

    type_id: Mapped[Optional[IDType]] = mapped_column(default=None, nullable=True)
    # Relationship to a DocumentType model. Adjust foreign key target as needed.
    type_: Mapped[Optional["DocumentTypeModel"]] = relationship(
        "DocumentTypeModel",
        primaryjoin="DocumentModel.type_id==DocumentTypeModel.id",
        uselist=False,
        viewonly=True
    )