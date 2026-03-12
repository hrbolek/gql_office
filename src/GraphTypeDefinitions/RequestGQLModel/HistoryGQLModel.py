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

RequestGQLModel = typing.Annotated["RequestGQLModel", strawberry.lazy(".RequestGQLModel")]
DigitalSubmissionGQLModel = typing.Annotated["DigitalSubmissionGQLModel", 
    strawberry.lazy("..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel")
]
RequestInputFilter = typing.Annotated["RequestInputFilter", strawberry.lazy(".RequestGQLModel")]

@createInputs2
class HistoryInputFilter:
    id: IDType
    name: str
    request_id: IDType
    submission_id: IDType
    state_id: IDType
    createdby_id: IDType
    request: RequestInputFilter

    from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionInputFilter
    submission: DigitalSubmissionInputFilter

@strawberry.federation.type(keys=["id"])
class HistoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).HistoryModel

    request_id: typing.Optional[IDType] = strawberry.field(
        description="The request to which this history entry is related",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name: typing.Optional[str] = strawberry.field(
        description="Message attached to history",
        default=None
    )

    submission_id: typing.Optional[IDType] = strawberry.field(
        description="The submission to which this history entry is related",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="The state to which this history entry is related",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    request: typing.Optional[RequestGQLModel] = strawberry.field(
        description="The request to which this history entry is related",
        resolver=ScalarResolver[RequestGQLModel](fkey_field_name="request_id")
    )

    submission: typing.Optional[DigitalSubmissionGQLModel] = strawberry.field(
        description="The submission to which this history entry is related",
        resolver=ScalarResolver[DigitalSubmissionGQLModel](fkey_field_name="submission_id")
    )

    from ..StateGQLModel import StateGQLModel
    state: typing.Optional[StateGQLModel] = strawberry.field(
        description="The state to which this history entry is related",
        resolver=ScalarResolver[StateGQLModel](fkey_field_name="state_id")
    )

@strawberry.interface(
    description="HistoryGQLModel related queries"
)
class HistoryQueries:
    history_by_id: typing.Optional[HistoryGQLModel] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=HistoryGQLModel.load_with_loader
    )

@strawberry.input(
    description="Params for insert"
)
class HistoryInsertGQLModel(InputModelMixin):
    getLoader = HistoryGQLModel.getLoader 
    request_id: IDType = strawberry.field(
        description="The request to which this history entry is related"
    )
    submission_id: IDType = strawberry.field(
        description="The submission to which this history entry is related"
    )
    state_id: IDType = strawberry.field(
        description="The state to which this history entry is related"
    )
    name: typing.Optional[str] = strawberry.field(
        description="Message attached to history",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""HistoryGQLModel primary key""",
        default=None
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="Params for update"
)
class HistoryUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""HistoryGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""HistoryGQLModel lastchange"""
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="Params for delete"
)
class HistoryDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""HistoryGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""HistoryGQLModel lastchange"""
    )

@strawberry.interface(
    description="HistoryGQLModel related mutations"
)
class HistoryMutations:
    from .RequestGQLModel import RequestGQLModel
    @strawberry.mutation(
        description="""Insert a history""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[InsertError, HistoryGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[InsertError, HistoryGQLModel](),
            RbacProviderExtension[InsertError, HistoryGQLModel](),
            LoadDataExtension[InsertError, HistoryGQLModel](
                primary_key_name="request_id",
                getLoader=RequestGQLModel.getLoader
            )
        ],
    )
    async def history_insert(
        self, 
        info: strawberry.types.Info,
        history: typing.Annotated[
            HistoryInsertGQLModel, 
            strawberry.argument (description="Full description of initial history attributes")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[InsertError[HistoryGQLModel], HistoryGQLModel]:
        history.rbacobject_id = rbacobject_id
        return await Insert[HistoryGQLModel].DoItSafeWay(
            info=info,
            entity=history,
        )

    @strawberry.mutation(
        description="""Update the history""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, HistoryGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, HistoryGQLModel](),
            RbacProviderExtension[UpdateError, HistoryGQLModel](),
            LoadDataExtension[UpdateError, HistoryGQLModel]()
        ],
    )
    async def history_update(
        self, 
        info: strawberry.types.Info,
        history: typing.Annotated[
            HistoryUpdateGQLModel,
            strawberry.argument (description="Full description of history attributes to be updated")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[UpdateError[HistoryGQLModel], HistoryGQLModel]:
        return await Update[HistoryGQLModel].DoItSafeWay(
            info=info,
            entity=history,
        )

    @strawberry.mutation(
        description="""Delete the history""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, HistoryGQLModel](
                roles=[
                    "administrátor", 
                    "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, HistoryGQLModel](),
            RbacProviderExtension[DeleteError, HistoryGQLModel](),
            LoadDataExtension[DeleteError, HistoryGQLModel]()
        ],
    )
    async def history_update(
        self, 
        info: strawberry.types.Info,
        history: typing.Annotated[
            HistoryDeleteGQLModel,
            strawberry.argument (description="Identification of the history record to be removed from db")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[DeleteError[HistoryGQLModel], HistoryGQLModel]:
        return await Delete[HistoryGQLModel].DoItSafeWay(
            info=info,
            entity=history,
        )