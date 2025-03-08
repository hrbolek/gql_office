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
class EventFacilityReservationModel(BaseModel):
    __tablename__ = "event_facility_reservations"

    id: Mapped[IDType] = mapped_column(primary_key=True, default=None, nullable=True)
    
    event_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("events.id"), default=None, nullable=True, comment="Event id")
    facility_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("facilities.id"), default=None, nullable=True, comment="Facility id")
    state_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True, comment="State of reservation")
    
    # Relationships
    event = relationship(
        "EventModel",
        primaryjoin="EventFacilityReservationModel.event_id==EventModel.id",
        uselist=False,
        viewonly=True
    )
    
    facility = relationship(
        "FacilityModel",
        primaryjoin="EventFacilityReservationModel.facility_id==FacilityModel.id",
        uselist=False,
        viewonly=True
    )
    
