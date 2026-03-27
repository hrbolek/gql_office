import typing
import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
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
from .BaseGQLModel import IDType

EventInvitationInputFilter = typing.Annotated["EventInvitationInputFilter", strawberry.lazy(".EventGQLModel.EventInvitationGQLModel")]
EventInvitationGQLModel = typing.Annotated["EventInvitationGQLModel", strawberry.lazy(".EventGQLModel.EventInvitationGQLModel")]

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: IDType = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    # @strawberry.field(
    #     description="Invitations which the user has",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ]
    # )
    # async def invitations(
    #     self, 
    #     info: strawberry.types.Info, 
    #     skip: int = 0,
    #     limit: int = 0,
    # ):
    #     pass

    invitations: typing.Optional[EventInvitationGQLModel] = strawberry.field(
        description="Invitations related to the user",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[EventInvitationGQLModel](fkey_field_name="user_id", whereType=EventInvitationInputFilter)
    )