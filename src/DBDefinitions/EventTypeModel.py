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

class EventTypeModel(BaseModel):
    __tablename__ = "eventtypes"

    name: Mapped[str] = mapped_column(default=None, comment="aka lecture, laboratory, ...")
    name_en: Mapped[str] = mapped_column(default=None, comment="aka lecture, laboratory, ...")

    parent_id = Column(ForeignKey("eventtypes.id"), index=True, comment="aka academic, admnistrative, ...")


    events = relationship("EventModel", back_populates="type")
