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
    keys=["id"], description="""Entity representing a Invitation to an Event and also presence of a user, invitation state and presence is managed by state"""
)
class EventInvitationGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).EventInvitationModel

    event_id: typing.Optional[IDType] = strawberry.field(
        description="""Event assigned to the invitation""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned to the invitation""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""State assigned to the invitation""",
        default=None,
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
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    state: typing.Optional[StateGQLModel] = strawberry.field(
        description="""State assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StateGQLModel](fkey_field_name="state_id")
    )

@strawberry.type(description="")
class EventInvitationQuery:

    event_invitation_by_id: typing.Optional[EventInvitationGQLModel] = strawberry.field(
        description="Invitation by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=EventInvitationGQLModel.load_with_loader
    )

    event_invitation_page: typing.List[EventInvitationGQLModel] = strawberry.field(
        description="selected invitations to events",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[EventInvitationGQLModel](whereType=EventInvitationInputFilter)
    )


    
@strawberry.input(
    description="""EventInvitation insert mutation"""
)
class EventInvitationInsertGQLModel:
    event_id: typing.Optional[IDType] = strawberry.field(
        description="event id to which invitation is sent",
        default=None,
    )

    user_id: typing.Optional[IDType] = strawberry.field(
        description="user id who receive invitation",
        default=None,
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="invitation kind",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""client generated id""",
        default=None,
    )

@strawberry.input(
    description="""EventInvitation update mutation"""
)
class EventInvitationUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""id"""
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""timestamp"""
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="invitation kind and presence type",
        default=None
    )

    user_id: typing.Optional[IDType] = strawberry.field(
        description="user id who receive invitation",
        default=None,
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="invitation kind",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""EventInvitation delete mutation"""
)
class EventInvitationDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""EventInvitation id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""EventInvitation lastchange"""
    )


@strawberry.type(
    description="""EventInvitation mutation"""
)
class EventInvitationMutation:
    @strawberry.field(
        description="""Insert a EventInvitation""",
        permission_classes=[
            SimpleInsertPermission[EventInvitationGQLModel](roles=["administrátor"])
        ]
    )
    async def event_invitation_insert(
        self,
        info: strawberry.types.Info,
        invitation: EventInvitationInsertGQLModel
    ) -> typing.Union[EventInvitationGQLModel, InsertError[EventInvitationGQLModel]]:
        # TODO check if invitation already exists and reject to invite that user again
        return await Insert[EventInvitationGQLModel].DoItSafeWay(info=info, entity=invitation)
    
    @strawberry.field(
        description="""Update a EventInvitation""",
        permission_classes=[
            SimpleUpdatePermission[EventInvitationGQLModel](roles=["administrátor"])
        ]
    )
    async def event_invitation_update(
        self,
        info: strawberry.types.Info,
        invitation: EventInvitationUpdateGQLModel
    ) -> typing.Union[EventInvitationGQLModel, UpdateError[EventInvitationGQLModel]]:
        return await Update[EventInvitationGQLModel].DoItSafeWay(info=info, entity=invitation)
    
    @strawberry.field(
        description="""Delete a EventInvitation""",
        permission_classes=[
            SimpleDeletePermission[EventInvitationGQLModel](roles=["administrátor"])
        ]
    )
    async def event_invitation_delete(
        self,
        info: strawberry.types.Info,
        invitation: EventInvitationDeleteGQLModel
    ) -> typing.Optional[DeleteError[EventInvitationGQLModel]]:
        return await Delete[EventInvitationGQLModel].DoItSafeWay(info=info, entity=invitation)        