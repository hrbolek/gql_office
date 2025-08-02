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

from ..BaseGQLModel import BaseGQLModel, IDType

from ..StateMachineGQLModel import StateMachineGQLModel
from ..StateGQLModel import StateGQLModel
DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy("..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormGQLModel")]

@createInputs2
class RequestTypeInputFilter:
    id: IDType
    name: str
    initial_form_id: IDType
    statemachine_id: IDType
    state_id: IDType
    createdby_id: IDType

@strawberry.federation.type(keys=["id"])
class RequestTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RequestTypeModel

    name: typing.Optional[str] = strawberry.field(
        description="",
        default=None
    )

    statemachine_id: typing.Optional[IDType] = strawberry.field(
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
    
    initial_form_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    statemachine: typing.Optional[StateMachineGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StateMachineGQLModel](fkey_field_name="statemachine_id")
    )

    state: typing.Optional[StateGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StateGQLModel](fkey_field_name="state_id")
    )

    initial_form: typing.Optional[DigitalFormGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[DigitalFormGQLModel](fkey_field_name="initial_form_id")
    )


@strawberry.interface(
    description="RequestTypeGQLModel related queries"
)
class RequestTypeQueries:
    requesttype_by_id: typing.Optional[RequestTypeGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=RequestTypeGQLModel.load_with_loader
    )
    requesttype_page: typing.List[RequestTypeGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[RequestTypeGQLModel](whereType=RequestTypeInputFilter)
    )


@strawberry.input(
    description="Params for insert"
)
class RequestTypeInsertGQLModel(InputModelMixin):
    getLoader = RequestTypeGQLModel.getLoader 
    id: typing.Optional[IDType] = strawberry.field(
        description="""RequestTypeGQLModel primary key""",
        default=None
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="Params for update"
)
class RequestTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""RequestTypeGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""RequestTypeGQLModel lastchange"""
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="Params for delete"
)
class RequestTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""RequestTypeGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""RequestTypeGQLModel lastchange"""
    )

@strawberry.interface(
    description="RequestTypeGQLModel related mutations"
)
class RequestTypeMutations:
    from .RequestGQLModel import RequestGQLModel
    @strawberry.mutation(
        description="""Insert a requesttype""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[InsertError, RequestTypeGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[InsertError, RequestTypeGQLModel](),
            RbacProviderExtension[InsertError, RequestTypeGQLModel](),
            LoadDataExtension[InsertError, RequestTypeGQLModel](
                primary_key_name="request_id",
                getLoader=RequestGQLModel.getLoader
            )
        ],
    )
    async def requesttype_insert(
        self, 
        info: strawberry.types.Info,
        request_type: typing.Annotated[
            RequestTypeInsertGQLModel, 
            strawberry.argument (description="Full description of initial requesttype attributes")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[InsertError[RequestTypeGQLModel], RequestTypeGQLModel]:
        request_type.rbacobject_id = rbacobject_id
        return await Insert[RequestTypeGQLModel].DoItSafeWay(
            info=info,
            entity=request_type,
        )

    @strawberry.mutation(
        description="""Update the requesttype""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, RequestTypeGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, RequestTypeGQLModel](),
            RbacProviderExtension[UpdateError, RequestTypeGQLModel](),
            LoadDataExtension[UpdateError, RequestTypeGQLModel]()
        ],
    )
    async def requesttype_update(
        self, 
        info: strawberry.types.Info,
        request_type: typing.Annotated[
            RequestTypeUpdateGQLModel,
            strawberry.argument (description="Full description of requesttype attributes to be updated")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[UpdateError[RequestTypeGQLModel], RequestTypeGQLModel]:
        return await Update[RequestTypeGQLModel].DoItSafeWay(
            info=info,
            entity=request_type,
        )

    @strawberry.mutation(
        description="""Delete the requesttype""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, RequestTypeGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, RequestTypeGQLModel](),
            RbacProviderExtension[DeleteError, RequestTypeGQLModel](),
            LoadDataExtension[DeleteError, RequestTypeGQLModel]()
        ],
    )
    async def requesttype_update(
        self, 
        info: strawberry.types.Info,
        request_type: typing.Annotated[
            RequestTypeDeleteGQLModel,
            strawberry.argument (description="Identification of the requesttype record to be removed from db")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[DeleteError[RequestTypeGQLModel], RequestTypeGQLModel]:
        return await Delete[RequestTypeGQLModel].DoItSafeWay(
            info=info,
            entity=request_type,
        )