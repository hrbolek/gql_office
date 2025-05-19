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
    createInputs2,

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

from ..BaseGQLModel import BaseGQLModel, IDType, Relation
from .TimeUnit import TimeUnit

EventTypeGQLModel = typing.Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]
EventInvitationGQLModel = typing.Annotated["EventInvitationGQLModel", strawberry.lazy(".EventInvitationGQLModel")]
EventInvitationInputFilter = typing.Annotated["EventInvitationInputFilter", strawberry.lazy(".EventInvitationGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy("..FacilityGQLModel")]

EventFacilityReservationGQLModel = typing.Annotated["EventFacilityReservationGQLModel", strawberry.lazy(".EventFacilityReservationGQLModel")]
EventFacilityReservationInputFilter = typing.Annotated["EventFacilityReservationInputFilter", strawberry.lazy(".EventFacilityReservationGQLModel")]


# from ..TreeGQLModel import TreeGQLModel

@createInputs2
class EventInputFilter:
    name: str
    name_en: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    id: IDType
    type_id: IDType
    
    from .EventTypeGQLModel import EventTypeInputFilter
    type_: EventTypeInputFilter = strawberry.field(name="type", description="Event type", default=None)


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

    # parent_id: typing.Optional[IDType] = strawberry.field(
    #     description="Parent id",
    #     default=None,
    #     permission_classes=[OnlyForAuthentized]
    # )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Event description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Event start date""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Event end date""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    # duration: strawberry.Private[object] = None
    duration: typing.Optional[datetime.timedelta] = strawberry.field(
        name="duration_raw",
        default=None,
        description="""len""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    @strawberry.field(
        name="duration",
        description="""Event duration, implicitly in minutes""",
        permission_classes=[
            # OnlyForAuthentized,
            # OnlyForAdmins
        ],
    )
    def _duration(self, unit: TimeUnit=TimeUnit.MINUTES) -> typing.Optional[float]:
        duration = self.duration or (self.enddate - self.startdate)
        result = duration.total_seconds()
        if unit == TimeUnit.SECONDS:
            return result
        if unit == TimeUnit.MINUTES:
            return result / 60
        if unit == TimeUnit.HOURS:
            return result / 60 / 60
        if unit == TimeUnit.DAYS:
            return result / 60 / 60 / 24
        if unit == TimeUnit.WEEKS:
            return result / 60 / 60 / 24 / 7
        # raise Exception("Unknown unit for duration")


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
        ],
        directives=[Relation(to="FacilityGQLModel")]
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

    masterevent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Event parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    # parent: typing.Optional["EventGQLModel"] = strawberry.field(
    #     description="""Event parent""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     metadata={
    #         # "alchemy": lambda selectStatement, leftModel, rightModel: selectStatement.join(rightModel)
    #     },
    #     resolver=ScalarResolver["EventGQLModel"](fkey_field_name="masterevent_id")
    # )

    # children: typing.List["EventGQLModel"] = strawberry.field(
    #     description="""Event children""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=VectorResolver["EventGQLModel"](fkey_field_name="masterevent_id", whereType=EventInputFilter)
    # )

    type_id: typing.Optional[IDType] = strawberry.field(
        description="""Event type id""",
        default=None,
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
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Event eng name assigned by an administrator""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Event description""",
        default=None
    )
    start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event start date""",
        default=None
    )
    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event end date""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Event parent id""",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""Event id""",
        default=None
    )
    rbacobject_id: typing.Optional[IDType] = strawberry.field(
        description="""Event rbacobject id""",
        default=None
    )
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for updating a Event"""
)
class EventUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Event id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Event name assigned by an administrator""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Event eng name assigned by an administrator""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Event description""",
        default=None
    )
    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event start date""",
        default=None
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Event end date""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Event parent id""",
        default=None
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
    