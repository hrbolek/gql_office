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

EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
EventInputFilter = typing.Annotated["EventInputFilter", strawberry.lazy(".EventGQLModel")]

@createInputs
@dataclasses.dataclass
class EventTypeInputFilter:
    name: str
    name_en: str
    id: IDType
    parent_id: IDType


@strawberry.federation.type(
    description="""Entity representing a Event Type"""
)
class EventTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).EventTypeModel
  

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event Type name""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event Type eng name""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event Type description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Event Type parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["EventTypeGQLModel"] = strawberry.field(
        description="""Event Type parent""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["EventTypeGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["EventTypeGQLModel"] = strawberry.field(
        description="""Event Type children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EventTypeGQLModel"](fkey_field_name="parent_id", whereType=EventTypeInputFilter)
    )

    # from .EventGQLModel import EventInputFilter
    events: typing.List["EventGQLModel"] = strawberry.field(
        description="""Event Type events""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EventGQLModel"](fkey_field_name="type_id", whereType=EventInputFilter)
    )