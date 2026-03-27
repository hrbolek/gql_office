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

from src.DBDefinitions.BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

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
    
#                     +-------------+
#                     |   created   |
#                     +-------------+
#                           |
#                           v
#                   +----------------+
#          book     |   requested    | --- cancel --> [canceled]
#                   +----------------+
#                           |
#                   approve |    | reject
#                           v    v
#                 [approved]   [rejected]
#                           |
#                     use   |
#                           v
#                       [used]

# | UUID                                   | Code        | Label CZ  | Popis                                 | Initial | Final |
# | -------------------------------------- | ----------- | --------- | ------------------------------------- | ------- | ----- |
# | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | `created`   | Vytvořeno | Rezervace byla vytvořena              | ✅       | ❌     |
# | `7093f90c-5cf3-4d9f-b421-e8fe6f3c194d` | `requested` | Požádáno  | Uživatel požádal o rezervaci zařízení | ❌       | ❌     |
# | `01776d6f-e2ab-49ee-b7b2-77db47e77a2f` | `approved`  | Schváleno | Rezervace byla schválena              | ❌       | ❌     |
# | `5ffb13aa-dbd4-40ae-843a-138ef07d90e2` | `rejected`  | Zamítnuto | Rezervace byla zamítnuta              | ❌       | ✅     |
# | `afda8d2e-e1aa-4de7-a6c9-52960cc77ea2` | `canceled`  | Zrušeno   | Rezervace byla uživatelem zrušena     | ❌       | ✅     |
# | `fdcf22c1-7a2b-45e0-8a3c-bd689cb6f818` | `used`      | Využito   | Rezervace byla využita                | ❌       | ✅     |
