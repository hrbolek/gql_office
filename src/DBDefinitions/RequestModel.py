
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

class RequestModel(BaseModel):
    __tablename__ = "requests"

    name: Mapped[str] = mapped_column(String, default=None, nullable=True)
    active_submission_id: Mapped[IDType] = mapped_column(ForeignKey("digital_submissions.id"), default=None, nullable=True)
    request_type_id: Mapped[IDType] = mapped_column(ForeignKey("request_types.id"), default=None, nullable=True)
    state_id: Mapped[IDType] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)
    active_submission = relationship(
        "DigitalSubmissionModel",
        # remote_side="DigitalSubmissionModel.id",
        back_populates="request",
        uselist=False,
        init=False
        # cascade="save-update",
    )
    histories = relationship(
        "HistoryModel",
        # remote_side="HistoryModel.request_id",
        uselist=True,
        viewonly=True,
        init=False
    )
    request_type = relationship(
        "RequestTypeModel",
        uselist=False,
        viewonly=True,
        init=False
    )


