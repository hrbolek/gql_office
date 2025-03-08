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

EventTypeGQLModel = typing.Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]
EventInvitationGQLModel = typing.Annotated["EventInvitationGQLModel", strawberry.lazy(".EventInvitationGQLModel")]
EventInvitationInputFilter = typing.Annotated["EventInvitationInputFilter", strawberry.lazy(".EventInvitationGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy("..FacilityGQLModel")]

EventFacilityReservationGQLModel = typing.Annotated["EventFacilityReservationGQLModel", strawberry.lazy(".EventFacilityReservationGQLModel")]
EventFacilityReservationInputFilter = typing.Annotated["EventFacilityReservationInputFilter", strawberry.lazy(".EventFacilityReservationGQLModel")]

@createInputs
@dataclasses.dataclass
class EventInputFilter:
    name: str
    name_en: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    id: IDType


@strawberry.federation.type(
    description="""Entity representing a Event""",
    keys=["id"]
)
class EventGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).EventModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Event start date""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Event end date""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    place: typing.Optional[str] = strawberry.field(
        default=None,
        description="where the event will happen",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    facility_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="place where the event will happen",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    facility: typing.Optional[FacilityGQLModel] = strawberry.field(
        description="place where the event will happen",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[FacilityGQLModel](fkey_field_name="facility_id")
    )

    reservations: typing.List[EventFacilityReservationGQLModel] = strawberry.field(
        description="reservations for this event",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[EventFacilityReservationGQLModel](fkey_field_name="facility_id", whereType=EventFacilityReservationInputFilter)
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Event parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["EventGQLModel"] = strawberry.field(
        description="""Event parent""",
        permission_classes=[
            OnlyForAuthentized
        ],
        metadata={
            # "alchemy": lambda selectStatement, leftModel, rightModel: selectStatement.join(rightModel)
        },
        resolver=ScalarResolver["EventGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["EventGQLModel"] = strawberry.field(
        description="""Event children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EventGQLModel"](fkey_field_name="parent_id", whereType=EventInputFilter)
    )

    type_id: typing.Optional[IDType] = strawberry.field(
        description="""Event type id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type_: typing.Optional["EventTypeGQLModel"] = strawberry.field(
        name="type",
        description="""Event type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["EventTypeGQLModel"](fkey_field_name="type_id")
    )

    invitations: typing.List["EventInvitationGQLModel"] = strawberry.field(
        description="""Event invitations""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EventInvitationGQLModel"](fkey_field_name="event_id", whereType=EventInvitationInputFilter)
    )



@strawberry.interface(
    description="""Event queries"""
)
class EventQuery:
    event_by_id: typing.Optional[EventGQLModel] = strawberry.field(
        description="""get a event by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=EventGQLModel.load_with_loader
    )

    event_page: typing.List[EventGQLModel] = strawberry.field(
        description="""get a page of events""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[EventGQLModel](whereType=EventInputFilter)
    )

@strawberry.input(
    description="""Input type for creating a Event"""
)
class EventInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="""Event name assigned by an administrator""",
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Event eng name assigned by an administrator""",
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Event description""",
    )
    start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event start date""",
    )
    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event end date""",
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Event parent id""",
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""Event id""",
    )
    rbacobject_id: typing.Optional[IDType] = strawberry.field(
        description="""Event rbacobject id""",
    )
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for updating a Event"""
)
class EventUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Event id""",
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Event name assigned by an administrator""",
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Event eng name assigned by an administrator""",
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Event description""",
    )
    start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event start date""",
    )
    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event end date""",
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Event parent id""",
    )
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Event"""
)
class EventDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Event id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Event mutations"""
)
class EventMutation:
    @strawberry.mutation(
        description="""Insert a Event""",
        permission_classes=[
            SimpleInsertPermission[EventGQLModel](roles=["administrátor"])
        ]
    )
    async def event_insert(
        self,
        info: strawberry.Info,
        event: EventInsertGQLModel
    ) -> typing.Union[EventGQLModel, InsertError[EventGQLModel]]:
        return await Insert[EventGQLModel].DoItSafeWay(info=info, entity=event)
    
    @strawberry.mutation(
        description="""Update a Event""",
        permission_classes=[
            SimpleUpdatePermission[EventGQLModel](roles=["administrátor"])
        ]
    )
    async def event_update(
        self,
        info: strawberry.Info,
        event: EventUpdateGQLModel
    ) -> typing.Union[EventGQLModel, UpdateError[EventGQLModel]]:
        return await Update[EventGQLModel].DoItSafeWay(info=info, entity=event)
    
    @strawberry.mutation(
        description="""Delete a Event""",
        permission_classes=[
            SimpleDeletePermission[EventGQLModel](roles=["administrátor"])
        ]
    )   
    async def event_delete(
        self,
        info: strawberry.Info,
        event: EventDeleteGQLModel
    ) -> typing.Optional[DeleteError[EventGQLModel]]:
        return await Delete[EventGQLModel].DoItSafeWay(info=info, entity=event)
    