import datetime
from typing import Optional
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

class EventInvitationModel(BaseModel):
    __tablename__ = "event_invitations"

    id: Mapped[IDType] = mapped_column(primary_key=True, default=None, nullable=True)
    
    event_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("events.id"), default=None, nullable=True, comment="Event assigned to the invitation")
    user_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True, comment="User assigned to the invitation")
    state_id: Mapped[Optional[IDType]] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True, comment="State assigned to the invitation")
    
    # Relationships: viewonly indicates that these relationships are loaded via foreign keys.
    event = relationship(
        "EventModel",
        primaryjoin="EventInvitationModel.event_id==EventModel.id",
        uselist=False,
        viewonly=True
    )
