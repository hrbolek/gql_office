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
from sqlalchemy.orm import relationship, foreign

from src.DBDefinitions.BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class ElectronicDocumentModel(BaseModel):
    __tablename__ = "electronic_documents"

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="The title of the digital form")
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="The eng title of the digital form")
    description: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="Document description")

    state_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)

    parent_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("electronic_documents.id"), default=None, nullable=True, comment="Document parent id")
    type_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("document_types.id"), default=None, nullable=True, comment="Document type id")
    
    content: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="Document content")
    mimetype: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="Document mimetype")

    # Relationship to parent document.
    parent = relationship(
        "ElectronicDocumentModel",
        # back_populates="children",
        primaryjoin=lambda: ElectronicDocumentModel.id == foreign(ElectronicDocumentModel.parent_id),
        remote_side=lambda: [ElectronicDocumentModel.id],
        uselist=False,
        viewonly=True
    )
    
    # Relationship to child documents.
    children = relationship(
        "ElectronicDocumentModel",
        # back_populates="parent",
        primaryjoin=lambda: ElectronicDocumentModel.id == foreign(ElectronicDocumentModel.parent_id),
        remote_side=lambda: [ElectronicDocumentModel.parent_id],
        # cascade="all, delete-orphan",
        uselist=True,
        viewonly=True,
        lazy="select"
    )
    
    # Relationship to DocumentType.
    type = relationship(
        "DocumentTypeModel",
        primaryjoin="ElectronicDocumentModel.type_id==DocumentTypeModel.id",
        uselist=False,
        viewonly=True
    )