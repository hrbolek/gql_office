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

from ..BaseGQLModel import BaseGQLModel, IDType

EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
EventInputFilter = typing.Annotated["EventInputFilter", strawberry.lazy(".EventGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy("..FacilityGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("..StateGQLModel")]

@createInputs2
class EventFacilityReservationInputFilter:
    id: IDType
    event_id: IDType
    facility_id: IDType
    state_id: IDType


@strawberry.federation.type(
    description="""Entity representing a reservation of a Facility for the Event """
)
class EventFacilityReservationGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).EventFacilityReservationModel
  

    event_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Event id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    event: typing.Optional[EventGQLModel] = strawberry.field(
        description="event linked to this reservation",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[EventGQLModel](fkey_field_name="event_id")
    )

    facility_id: typing.Optional[IDType] = strawberry.field(
        description="""facility id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    facility: typing.Optional[FacilityGQLModel] = strawberry.field(
        description="facility linked to this reservation",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[FacilityGQLModel](fkey_field_name="facility_id")
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""state of reservation""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state: typing.Optional[StateGQLModel] = strawberry.field(
        description="state of this reservation",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StateGQLModel](fkey_field_name="state_id")
    )



@strawberry.federation.type(
    keys=["id"], description="Reservation of factility to particular event")
class EventFacilityReservationQuery:

    facility_reservation_by_id: typing.Optional[EventFacilityReservationGQLModel] = strawberry.field(
        description="Facility reservation for Event by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=EventFacilityReservationGQLModel.load_with_loader
    )

    facility_reservation_page: typing.List[EventFacilityReservationGQLModel] = strawberry.field(
        description="Facility reservations for Event ",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[EventFacilityReservationGQLModel](whereType=EventFacilityReservationInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin, TreeInputStructureMixin

@strawberry.input(description="Input definition for EventFacilityReservation create")
class EventFacilityReservationInsertGQLModel:
    facility_id: IDType = strawberry.field(description="facility")
    event_id: IDType = strawberry.field(description="event")
    state_id: IDType = strawberry.field(description="reservation state")
    id: typing.Optional[IDType] = strawberry.field(description="client generated primary key", default=None)
    createdby_id: strawberry.Private[IDType]

@strawberry.input(description="Input definition for EventFacilityReservation update")
class EventFacilityReservationUpdateGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    state_id: typing.Optional[IDType] = strawberry.field(description="reservation state")
    changedby_id: strawberry.Private[IDType]

@strawberry.input(description="Input definition for EventFacilityReservation delete")
class EventFacilityReservationDeleteGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

@strawberry.federation.type(description="")
class EventFacilityReservationMutation:

    @strawberry.mutation(
        description="standard insert operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[EventFacilityReservationGQLModel](roles=["administrátor"])
        ]
    )
    async def event_facility_insert(self, info: strawberry.types.Info, event_type: EventFacilityReservationInsertGQLModel) -> typing.Union[EventFacilityReservationGQLModel, InsertError[EventFacilityReservationGQLModel]]:
        result = await Insert[EventFacilityReservationGQLModel].DoItSafeWay(info=info, entity=event_type)
        return result
    
    @strawberry.mutation(
        description="standard update operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[EventFacilityReservationGQLModel](roles=["administrátor"])
        ]
    )
    async def event_facility_update(self, info: strawberry.types.Info, event_type: EventFacilityReservationUpdateGQLModel) -> typing.Union[EventFacilityReservationGQLModel, UpdateError[EventFacilityReservationGQLModel]]:
        result = await Update[EventFacilityReservationGQLModel].DoItSafeWay(info=info, entity=event_type)
        return result


    @strawberry.mutation(
        description="standard delete operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[EventFacilityReservationGQLModel](roles=["administrátor"])
        ]
    )
    async def event_facility_delete(self, info: strawberry.types.Info, event_type: EventFacilityReservationDeleteGQLModel) -> typing.Optional[DeleteError[EventFacilityReservationGQLModel]]:
        result = await Delete[EventFacilityReservationGQLModel].DoItSafeWay(info=info, entity=event_type)
        return result        