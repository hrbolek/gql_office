from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, IDType
class FacilityTypeModel(BaseModel):
    """Urcuje typ objektu (areal, budova, patro, mistnost)"""

    __tablename__ = "facilitytypes"

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

    name: Mapped[str] = mapped_column(default=None, nullable=True) # Column(String)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True) # Column(String)

    parent_id: Mapped[IDType] = mapped_column(ForeignKey("facilitytypes.id"), default=None, nullable=True) # Column(String)
    #facilities = relationship("FacilityModel", back_populates="facilitytype")

    parent = relationship(
        "FacilityTypeModel",
        viewonly=True, 
        remote_side="FacilityTypeModel.id",
        uselist=False,
        back_populates="children",
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    children = relationship(
        "FacilityTypeModel", 
        back_populates="parent",
        uselist=True,
        init=True,
        cascade="save-update"
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html
