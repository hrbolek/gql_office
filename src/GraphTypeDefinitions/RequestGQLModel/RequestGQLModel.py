import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
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
    ScalarResolver,
    InputModelMixin, 
    TreeInputStructureMixin
)
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension

from ..BaseGQLModel import BaseGQLModel, IDType

HistoryGQLModel = typing.Annotated["HistoryGQLModel", strawberry.lazy(".HistoryGQLModel")]
HistoryInputFilter = typing.Annotated["HistoryInputFilter", strawberry.lazy(".HistoryGQLModel")]
RequestTypeInputFilter = typing.Annotated["RequestTypeInputFilter", strawberry.lazy(".RequestTypeGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("..StateGQLModel")]

@createInputs2
class RequestInputFilter:
    id: IDType
    name: str
    request_type_id: IDType
    active_submission_id: IDType
    state_id: IDType

    request_type: RequestTypeInputFilter
    from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionInputFilter
    active_submission: DigitalSubmissionInputFilter

@strawberry.federation.type(keys=["id"])
class RequestGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RequestModel

    name: typing.Optional[str] = strawberry.field(
        description="",
        default=None
    )

    active_submission_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    request_type_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    # from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormGQLModel import DigitalFormGQLModel
    from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
    active_submission: typing.Optional[DigitalSubmissionGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[DigitalSubmissionGQLModel](fkey_field_name="active_submission_id")
    )
    
    histories: typing.List[HistoryGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[HistoryGQLModel](fkey_field_name="request_id", whereType=HistoryInputFilter)
    )

    state: typing.Optional[StateGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StateGQLModel](fkey_field_name="state_id")
    )

@strawberry.interface(
    description="RequestGQLModel related queries"
)
class RequestQueries:
    request_by_id: typing.Optional[RequestGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=RequestGQLModel.load_with_loader
    )

    request_page: typing.List[RequestGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[RequestGQLModel](whereType=RequestInputFilter)
    )

@strawberry.input(
    description="Parameters for creating a new request by requesting user"
)
class RequestInsertGQLModel(InputModelMixin):
    getLoader = RequestGQLModel.getLoader 
    requesttype_id: IDType = strawberry.field(
        description="from which type the new request is derived"
    )
    rbacobject_id: IDType = strawberry.field(
        description="rbac object ... " # TODO
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""RequestGQLModel primary key""",
        default=None
    )
    # rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="Parameters for creating a new request by administrator for an user"
)
class RequestForInsertGQLModel(InputModelMixin):
    getLoader = RequestGQLModel.getLoader 
    requesttype_id: IDType = strawberry.field(
        description="from which type the new request is derived"
    )
    rbacobject_id: IDType = strawberry.field(
        description="rbac object ... " # TODO
    )
    user_id: IDType = strawberry.field(
        description="user who will be marked as requester"
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""RequestGQLModel primary key""",
        default=None
    )
    # rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="Params for update"
)
class RequestUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""RequestGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""RequestGQLModel lastchange"""
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="Params for delete"
)
class RequestDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""RequestGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""RequestGQLModel lastchange"""
    )

@strawberry.interface(
    description="RequestGQLModel related mutations"
)
class RequestMutations:
    from .RequestGQLModel import RequestGQLModel
    from .RequestTypeGQLModel import RequestTypeGQLModel
    @strawberry.mutation(
        description="""Insert a request""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            # UserAccessControlExtension[InsertError, RequestGQLModel](
            #     roles=[
            #         "procesní administrátor", 
            #         # "personalista"
            #     ]
            # ),
            UserRoleProviderExtension[InsertError, RequestGQLModel](),
            RbacInsertProviderExtension[InsertError, RequestGQLModel](),
            # RbacProviderExtension[InsertError, RequestGQLModel](),
            LoadDataExtension[InsertError, RequestGQLModel](
                primary_key_name="requesttype_id",
                getLoader=RequestTypeGQLModel.getLoader
            )
        ],
    )
    async def request_insert(
        self, 
        info: strawberry.types.Info,
        request: typing.Annotated[
            RequestInsertGQLModel, 
            strawberry.argument (description="Full description of initial request attributes")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[InsertError[RequestGQLModel], RequestGQLModel]:
        # request.rbacobject_id = rbacobject_id
        return await Insert[RequestGQLModel].DoItSafeWay(
            info=info,
            entity=request,
        )

    @strawberry.mutation(
        description="""Insert a request""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[InsertError, RequestGQLModel](
                roles=[
                    "procesní administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[InsertError, RequestGQLModel](),
            RbacProviderExtension[InsertError, RequestGQLModel](),
            LoadDataExtension[InsertError, RequestGQLModel](
                primary_key_name="requesttype_id",
                getLoader=RequestTypeGQLModel.getLoader
            )
        ],
    )
    async def request_insert_for(
        self, 
        info: strawberry.types.Info,
        request: typing.Annotated[
            RequestForInsertGQLModel, 
            strawberry.argument (description="Full description of initial request attributes")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[InsertError[RequestGQLModel], RequestGQLModel]:
        request.rbacobject_id = rbacobject_id
        return await Insert[RequestGQLModel].DoItSafeWay(
            info=info,
            entity=request,
        )
    
    @strawberry.mutation(
        description="""Update the request""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, RequestGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, RequestGQLModel](),
            RbacProviderExtension[UpdateError, RequestGQLModel](),
            LoadDataExtension[UpdateError, RequestGQLModel]()
        ],
    )
    async def request_update(
        self, 
        info: strawberry.types.Info,
        request: typing.Annotated[
            RequestUpdateGQLModel,
            strawberry.argument (description="Full description of request attributes to be updated")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[UpdateError[RequestGQLModel], RequestGQLModel]:
        return await Update[RequestGQLModel].DoItSafeWay(
            info=info,
            entity=request,
        )

    @strawberry.mutation(
        description="""Delete the request""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, RequestGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, RequestGQLModel](),
            RbacProviderExtension[DeleteError, RequestGQLModel](),
            LoadDataExtension[DeleteError, RequestGQLModel]()
        ],
    )
    async def request_update(
        self, 
        info: strawberry.types.Info,
        request: typing.Annotated[
            RequestDeleteGQLModel,
            strawberry.argument (description="Identification of the request record to be removed from db")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[DeleteError[RequestGQLModel], RequestGQLModel]:
        return await Delete[RequestGQLModel].DoItSafeWay(
            info=info,
            entity=request,
        )
    

# {
#   requestPage {
#     __typename
#     id
#     activeSubmission {
#       __typename
#       id
#       form {
#         __typename
#         id
#         name
#         description
#       }
#       name
#       sections {
#         __typename
#         section {
#           __typename
#           id
#           index
#         }
#         formSection {
#           __typename
#           id
#           name
#           label
#           order
#           repatableMin
#           repatableMax
#         }
#         id
#         fields {
#           __typename
#           id
#           value
#           field {
#             __typename
#             id
#             name
#             label
#             description
#             required
#             typeId
#           }
#           rbacobject {
#             currentUserRoles {
#               roletype {
#                 id
#                 name
#               }
#             }
#           }
#         }
#         rbacobject {
#           currentUserRoles {
#             roletype {
#               id
#               name
#             }
#           }
#         }
#       }
#       rbacobject {
#         currentUserRoles {
#           roletype {
#             id
#             name
#           }
#         }
#       }
#     }
#   }
# }