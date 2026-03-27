import typing
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

from src.DBDefinitions.BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class RequestTypeModel(BaseModel):
    __tablename__ = "request_types"

    name: Mapped[str] = mapped_column(String, default=None, nullable=True)
    initial_form_id: Mapped[IDType] = mapped_column(ForeignKey("digital_forms.id"), default=None, nullable=True)
    state_id: Mapped[IDType] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True, comment="initial state")
    statemachine_id: Mapped[IDType] = UUIDFKey(ForeignKey("statemachines.id"), default=None, nullable=True, comment="statemachine ruling requesttype")

    initial_form = relationship(
        "DigitalFormModel",
        foreign_keys=[initial_form_id],
        uselist=False,
        init=True,
        cascade="save-update"
    )