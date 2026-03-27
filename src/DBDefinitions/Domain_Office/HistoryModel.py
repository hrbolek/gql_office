
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

class HistoryModel(BaseModel):
    __tablename__ = "histories"

    name: Mapped[str] = mapped_column(String, default=None, nullable=True)
    request_id: Mapped[IDType] = mapped_column(ForeignKey("requests.id"), default=None, nullable=True)
    submission_id: Mapped[IDType] = mapped_column(ForeignKey("digital_submissions.id"), default=None, nullable=True)
    state_id: Mapped[IDType] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)

    submission = relationship(
        "DigitalSubmissionModel",
        # remote_side="DigitalSubmissionModel.id",
        # back_populates="histories",
        uselist=False,
        init=False,
        viewonly=True,
        # cascade="save-update",
    )
    request = relationship(
        "RequestModel",
        uselist=False,
        init=False,
        viewonly=True,
    )