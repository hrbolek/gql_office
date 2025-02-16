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
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("..UserGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("..StateGQLModel")]

@createInputs
@dataclasses.dataclass
class EventInvitationInputFilter:
    id: IDType
    event_id: IDType
    user_id: IDType
    state_id: IDType

@strawberry.federation.type(
    description="""Entity representing a Invitation to an Event and also presence of a user, invitation state and presence is managed by state"""
)
class EventInvitationGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).EventInvitationModel

    event_id: typing.Optional[IDType] = strawberry.field(
        description="""Event assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""State assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    event: typing.Optional[EventGQLModel] = strawberry.field(
        description="""Event assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[EventGQLModel](fkey_field_name="event_id")
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ],
        
    )

    state: typing.Optional[StateGQLModel] = strawberry.field(
        description="""State assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ],
        
    )

