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
class EventModel(BaseModel):
    __tablename__ = "events"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    place: Mapped[str] = mapped_column(default=None, nullable=True)
    facility_id: Mapped[IDType] = UUIDFKey(nullable=True)

    @hybrid_property
    def duration(self):
        return self.enddate - self.startdate

    masterevent_id: Mapped[IDType] = mapped_column(ForeignKey("events.id"), index=True, nullable=True, default=None)
    type_id: Mapped[IDType] = mapped_column(ForeignKey("eventtypes.id"), index=True, nullable=True, default=None)
    # type = relationship("EventTypeModel", back_populates="events")
    type = relationship("EventTypeModel", viewonly=True)
    # presences = relationship("PresenceModel", viewonly=True)
    sub_events = relationship("EventModel", viewonly=True, uselist=True)
    master_event = relationship("EventModel", viewonly=True, uselist=False)

    # groups = relationship("EventGroupModel", viewonly=True, uselist=True)
