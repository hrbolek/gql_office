import asyncio
import dataclasses
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)

from ..BaseGQLModel import BaseGQLModel, IDType

@createInputs
@dataclasses.dataclass
class TaskInputFilter:
    name: str
    name_en: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    id: IDType

@strawberry.federation.type(description="Task definition", keys=["id"])
class TaskGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).TaskModel
    
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Task name """,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Task eng name""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Task description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Task start date""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Task end date""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    