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

class DigitalFormFieldPermissionModel(BaseModel):
    __tablename__ = "digital_form_field_permissions"


    form_field_id: Mapped[IDType] = mapped_column(ForeignKey("digital_form_fields.id", ondelete="CASCADE"), default=None, nullable=True)
    state_id: Mapped[IDType] = UUIDFKey(ForeignKey("states.id"), default=None, nullable=True)
    role_type_id: Mapped[IDType] = UUIDFKey(ForeignKey("role_types.id"), default=None, nullable=True)
    operation_id: Mapped[IDType] = UUIDFKey(ForeignKey("operations.id"), default=None, nullable=True)

