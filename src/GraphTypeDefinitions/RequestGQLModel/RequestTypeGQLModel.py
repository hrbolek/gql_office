import uuid
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs2,

    getUserFromInfo,

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

from ..StateMachineGQLModel import StateMachineGQLModel
from ..StateGQLModel import StateGQLModel
DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy("..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormGQLModel")]
DigitalFormInsertGQLModel = typing.Annotated["DigitalFormInsertGQLModel", strawberry.lazy("..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormGQLModel")]

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
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    
    initial_form_id: typing.Optional[IDType] = strawberry.field(
        description="",
        default=None,
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

def initial_form_factory():
    from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormGQLModel import DigitalFormInsertGQLModel
    from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormSectionGQLModel import DigitalFormSectionInsertGQLModel
    result = DigitalFormInsertGQLModel(
        id = uuid.uuid4(),
        name="Formulář pro požadavek",
        name_en="Form for the request",
        # sections=[
        #     DigitalFormSectionInsertGQLModel(
        #         name="section1",
        #         label="Hlavička",
        #         label_en="Header",
        #     )
        # ],
    )
    asdict = strawberry.asdict(result)
    print(f"initial_form_factory: {asdict}")
    return result


@strawberry.input(
    description="Params for insert"
)
class RequestTypeInsertGQLModel(InputModelMixin):
    getLoader = RequestTypeGQLModel.getLoader 
    # rbacobject_id: IDType = strawberry.field(
    #     description="""Storage for access control"""
    # )
    mastergroup_id: IDType = strawberry.field(
        description="""Shelter for this request - where it belongs to like faculty or university etc."""
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""RequestTypeGQLModel primary key""",
        default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="name",
        default="New request type"
    )
    # statemachine_id: typing.Optional[IDType] = strawberry.field(
    #     description="statemachine id",
    #     default=None
    # )
    # state_id: typing.Optional[IDType] = strawberry.field(
    #     description="initial state id",
    #     default=None
    # )
    initial_form: typing.Optional[DigitalFormInsertGQLModel] = strawberry.field(
        description="The form defining the structure of data to be submitted",
        # default_factory=initial_form_factory
        # default=initial_form_factory()
        # default=None
        default_factory=lambda: {
            "name": "Formulář pro požadavek",
            "name_en": "Form for the request",
        }
    )
    # initial_form_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None
    # initial_form: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None
    statemachine_id: strawberry.Private[IDType] = None
    state_id: strawberry.Private[IDType] = None

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
            # UserAccessControlExtension[InsertError, RequestTypeGQLModel](
            #     roles=[
            #         "administrátor", 
            #         "personalista"
            #     ]
            # ),


            # UserRoleProviderExtension[InsertError, RequestTypeGQLModel](),
            # RbacInsertProviderExtension[InsertError, RequestTypeGQLModel](),


            # RbacProviderExtension[InsertError, RequestTypeGQLModel](),
            # LoadDataExtension[InsertError, RequestTypeGQLModel](
            #     primary_key_name="request_id",
            #     getLoader=RequestGQLModel.getLoader
            # )
        ],
    )
    async def requesttype_insert(
        self, 
        info: strawberry.types.Info,
        request_type: typing.Annotated[
            RequestTypeInsertGQLModel, 
            strawberry.argument (description="Full description of initial requesttype attributes")
        ],
        # rbacobject_id: IDType,
        # user_roles: typing.List[dict],
        # db_row: typing.Any
    ) -> typing.Union[InsertError[RequestTypeGQLModel], RequestTypeGQLModel]:
        actinguser = getUserFromInfo(info)
        # print(f"actinguser {actinguser}")
        actinguser_id = actinguser.get("id")
        # if request_type.initial_form is None:
        #     request_type.initial_form = initial_form_factory()
        gqlClient = info.context.get("ug_client", None)
        if gqlClient is None:
            return InsertError[RequestTypeGQLModel](
                msg="gqlClient @ requesttype_insert is None",
                code="128510e3-3442-48e6-a4fd-8a21ef9f58ba",
                failed=True,
                _input=request_type
            )
        
        rbacobject_id = f"{uuid.uuid4()}"
        statemachine_id = f"{uuid.uuid4()}"
        state_id_a = f"{uuid.uuid4()}"
        state_id_z = f"{uuid.uuid4()}"
        variables = {
            "rbacobjectId": rbacobject_id,
            "statemachineId": statemachine_id,
            "name": f"RBAC: {request_type.name}",
            "statemachineName": f"Stavy: {request_type.name}",
            "mastergroupId": f"{request_type.mastergroup_id}",
            # "memberships": [],
            "roles": [
                {
                    "roletypeId": "b8dcb508-77a5-4385-bba6-ba55f4ecbeeb", # superadmin
                    "userId": f"{actinguser_id}", #"51d101a0-81f1-44ca-8366-6cf51432e8d6", # Zdenka
                    "groupId": rbacobject_id,
                    "startdate": "2026-01-01T00:01:01",
                    "enddate": None
                }
            ],
            "states": [
                {
                    "id": state_id_a,
                    "statemachineId": statemachine_id,
                    "name": "Žadatel",
                    "order": 0
                },
                {
                    "id": state_id_z,
                    "statemachineId": statemachine_id,
                    "name": "Archiv",
                    "order": 999
                }
            ],
        }
        query = """
mutation rbacInsert(
    $rbacobjectId: UUID! # null, 
    $statemachineId: UUID! # null, 
	$mastergroupId: UUID! # null, 
	$name: String! # null, 
    $statemachineName: String! # null, 
	$roles: [RoleInsertGQLModel!] # null,
    $states: [StateInsertGQLModel!],
    $transitions: [StatetransitionInsertGQLModel!]
) {
  rbacInsert(
	rbac: {
    id: $rbacobjectId,
	mastergroupId: $mastergroupId, 
	name: $name, 
	# abbreviation: $abbreviation, 
	roles: $roles}
  ) {
    ... on RBACObjectGQLModel { __typename id }
    ... on RBACObjectGQLModelInsertError { ...RBACObjectGQLModelInsertError }
  }

  statemachineInsert(
	statemachine: {
	name: $statemachineName, 
	rbacobjectId: $rbacobjectId, 
	id: $statemachineId, 
	states: $states, 
	transitions: $transitions}
  ) {
    ... on StateMachineGQLModel { __typename id name }
    ... on StateMachineGQLModelInsertError { ...StateMachineGQLModelInsertError }
  }

}

fragment RBACObjectGQLModelInsertError on RBACObjectGQLModelInsertError {
  __typename
  
  msg
  failed
  code
  location
  input
  }

fragment StateMachineGQLModelInsertError on StateMachineGQLModelInsertError {
  __typename
  
  msg
  failed
  code
  location
  input
  }

"""
        ug_response = await gqlClient(query=query, variables=variables)
        errors = ug_response.get("errors")
        if errors:
            return InsertError[RequestTypeGQLModel](
                msg=f"{errors}",
                code="b770a479-80d9-4a2a-a483-7018126f9a49",
                _input=request_type
            )
        data = ug_response.get("data")
        if data is None:
            return InsertError[RequestTypeGQLModel](
                msg="request to gql_ug @ requesttype_insert returns no data",
                code="e7e6579e-5687-42cb-8752-87ff0ffdee01",
                _input=request_type
            )
        rbacInsert = data.get("rbacInsert")
        if rbacInsert is None:
            return InsertError[RequestTypeGQLModel](
                msg=f"request to gql_ug @ requesttype_insert returns no rbac",
                code="b19bc1af-4c09-4746-9782-1f7ecb16256d",
                _input=request_type
            )
        __typename = rbacInsert.get("__typename")
        if __typename.endswith("Error") :
            return InsertError[RequestTypeGQLModel](
                msg=f"request to gql_ug @ requesttype_insert returns error {__typename}\n{rbacInsert}",
                code="c0c860e9-c982-4bd1-9acf-2b7d481de933",
                _input=request_type
            )
        
        # request_type
        request_type.set_rbacobject_id(rbacobject_id)
        request_type.statemachine_id = statemachine_id
        request_type.state_id = state_id_a
        request_type = await request_type.intoModel(info=info)
        print(f"requesttype_insert: {request_type.initial_form}")
        print(f"requesttype_insert: {request_type.rbacobject_id}")
        
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
    async def requesttype_delete(
        self, 
        info: strawberry.types.Info,
        request_type: typing.Annotated[
            RequestTypeDeleteGQLModel,
            strawberry.argument (description="Identification of the requesttype record to be removed from db")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[RequestTypeGQLModel]]:
        return await Delete[RequestTypeGQLModel].DoItSafeWay(
            info=info,
            entity=request_type,
        )
    
    