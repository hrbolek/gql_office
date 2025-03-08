import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
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
    keys=["id"], description="""Entity representing a Event Type"""
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
        default=None,
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


@strawberry.federation.type(description="")
class EventTypeQuery:

    event_type_by_id: typing.Optional[EventTypeGQLModel] = strawberry.field(
        description="Event type by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=EventTypeGQLModel.load_with_loader
    )

    event_type_page: typing.List[EventTypeGQLModel] = strawberry.field(
        description="return list of events",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[EventTypeGQLModel](whereType=EventTypeInputFilter)
    )

@strawberry.input(description="Input definition for EventType create")
class EventTypeInsertGQLModel:
    name: str = strawberry.field(description="name of the type")
    name_en: typing.Optional[str] = strawberry.field(description="eng name of the type", default=None)
    parent_id: typing.Optional[IDType] = strawberry.field(description="for which type this type belongs", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="client generated primary key", default=None)
    createdby_id: strawberry.Private[IDType]

@strawberry.input(description="Input definition for EventType update")
class EventTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: IDType = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="eng name of the type", default=None)
    changedby_id: strawberry.Private[IDType]

@strawberry.input(description="Input definition for EventType delete")
class EventTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: IDType = strawberry.field(description="timestamp for concurrent update")

@strawberry.federation.type(description="")
class EventTypeMutation:

    @strawberry.mutation(
        description="standard insert operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[EventTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def event_type_insert(self, info: strawberry.types.Info, event_type: EventTypeInsertGQLModel) -> typing.Union[EventTypeGQLModel, InsertError[EventTypeGQLModel]]:
        result = await Insert[EventTypeGQLModel].DoItSafeWay(info=info, entity=event_type)
        return result
    
    @strawberry.mutation(
        description="standard update operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[EventTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def event_type_update(self, info: strawberry.types.Info, event_type: EventTypeUpdateGQLModel) -> typing.Union[EventTypeGQLModel, UpdateError[EventTypeGQLModel]]:
        result = await UpdateError[EventTypeGQLModel].DoItSafeWay(info=info, entity=event_type)
        return result


    @strawberry.mutation(
        description="standard delete operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[EventTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def event_type_delete(self, info: strawberry.types.Info, event_type: EventTypeDeleteGQLModel) -> typing.Optional[DeleteError[EventTypeGQLModel]]:
        result = await Delete[EventTypeGQLModel].DoItSafeWay(info=info, entity=event_type)
        return result        