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

from src.DBDefinitions.BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class DocumentTypeModel(BaseModel):
    __tablename__ = "document_types"

    path_attribute_name = "path"
    parent_attribute_name = "parent"
    parent_id_attribute_name = "parent_id"
    children_attribute_name = "children"

    # Materialized path technique
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique, not implemented"
    )

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="Document type name")
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="Document eng name")
    description: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="Document type description")
    parent_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("document_types.id"), default=None, nullable=True, comment="Parent document type id")
    
    # Relationship to parent document type.
    parent = relationship(
        "DocumentTypeModel",
        remote_side="DocumentTypeModel.id",
        back_populates="children",
        uselist=False
    )
    
    # Relationship to child document types.
    children = relationship(
        "DocumentTypeModel",
        back_populates="parent",
        uselist=True,
        init=True,
        cascade="save-update",
    )
