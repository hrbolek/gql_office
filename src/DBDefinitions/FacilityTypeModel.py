from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, IDType
class FacilityTypeModel(BaseModel):
    """Urcuje typ objektu (areal, budova, patro, mistnost)"""

    __tablename__ = "facilitytypes"
    name: Mapped[str] = mapped_column(default=None, nullable=True) # Column(String)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True) # Column(String)

    parent_id: Mapped[IDType] = mapped_column(ForeignKey("facilitytypes.id"), default=None, nullable=True) # Column(String)
    #facilities = relationship("FacilityModel", back_populates="facilitytype")