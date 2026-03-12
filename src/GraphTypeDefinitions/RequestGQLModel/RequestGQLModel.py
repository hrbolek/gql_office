import asyncio
import dataclasses
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

HistoryGQLModel = typing.Annotated["HistoryGQLModel", strawberry.lazy(".HistoryGQLModel")]
HistoryInputFilter = typing.Annotated["HistoryInputFilter", strawberry.lazy(".HistoryGQLModel")]
RequestTypeInputFilter = typing.Annotated["RequestTypeInputFilter", strawberry.lazy(".RequestTypeGQLModel")]
RequestTypeGQLModel = typing.Annotated["RequestTypeGQLModel", strawberry.lazy(".RequestTypeGQLModel")]
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
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    request_type_id: typing.Optional[IDType] = strawberry.field(
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

    # from .RequestTypeGQLModel import RequestTypeGQLModel
    request_type: typing.Optional[RequestTypeGQLModel] = strawberry.field(
        description="reference to description of the flow",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[RequestTypeGQLModel](fkey_field_name="request_type_id")
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
    request_type_id: IDType = strawberry.field(
        description="from which type the new request is derived"
    )
    # rbacobject_id: IDType = strawberry.field(
    #     description="rbac object ... " # TODO
    # )
    id: typing.Optional[IDType] = strawberry.field(
        description="""RequestGQLModel primary key""",
        default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="name of the request",
        default=None
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None
    state_id: strawberry.Private[IDType] = None

    from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
    active_submission: strawberry.Private[DigitalSubmissionGQLModel] = None


@strawberry.input(
    description="Parameters for creating a new request by administrator for an user"
)
class RequestForInsertGQLModel(InputModelMixin):
    getLoader = RequestGQLModel.getLoader 
    request_type_id: IDType = strawberry.field(
        description="from which type the new request is derived"
    )
    rbacobject_id: IDType = strawberry.field(
        description="rbac object ... " # TODO
    )
    user_id: IDType = strawberry.field(
        description="user who will be marked as requester"
    )
    name: typing.Optional[str] = strawberry.field(
        description="name of the request",
        default=None
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
    description="Params for update"
)
class RequestUseTransitionGQLModel:
    id: IDType = strawberry.field(
        description="""RequestGQLModel primary key"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""RequestGQLModel lastchange"""
    )
    target_state_id: IDType = strawberry.field(
        description="""Target state to which the request should be moved"""
    )
    msg: typing.Optional[str] = strawberry.field(
        description="""Optional message accompanying the state transition""",
        default=""
    )

    changedby_id: strawberry.Private[IDType] = None

    # from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionInsertGQLModel2
    # active_submission: strawberry.Private[DigitalSubmissionInsertGQLModel2] = None
    active_submission_id: strawberry.Private[IDType] = None

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
                primary_key_name="request_type_id",
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
        print(f"request_insert \n{request}")

        actinguser = getUserFromInfo(info)
        user_id = IDType(actinguser["id"])

        gqlClient = info.context.get("ug_client", None)
        if gqlClient is None:
            return InsertError[RequestGQLModel](
                msg="gqlClient @ request_insert is None",
                code="984c7ccf-aec9-4982-8de3-96601a0bd225",
                failed=True,
                _input=request
            )
        
        child_rbacobject_id = f"{request.id}" or f"{uuid.uuid4()}"

        # 1. create rbacobject inherited from rbacobject of requesttype
        variables = {
            "rbacobjectId": child_rbacobject_id,
            "name": f"RBAC: {request.name}",
            "mastergroupId": f"{rbacobject_id}",
            # "memberships": [],
            "roles": [
                {
                    # TODO place here roletype "Zadatel"
                    "roletypeId": "b8dcb508-77a5-4385-bba6-ba55f4ecbeeb", # superadmin
                    # TODO place here current user
                    "userId": "51d101a0-81f1-44ca-8366-6cf51432e8d6", # Zdenka
                    "groupId": child_rbacobject_id,
                    "startdate": "2026-01-01T00:01:01",
                    "enddate": None
                }
            ]
        }

        query = """
mutation rbacInsert(
  $rbacobjectId: UUID! # null, 
	$mastergroupId: UUID! # null, 
	$name: String! # null, 
	$roles: [RoleInsertGQLModel!] # null,
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
}

fragment RBACObjectGQLModelInsertError on RBACObjectGQLModelInsertError {
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
            return InsertError[RequestGQLModel](
                msg=f"{errors}",
                code="c5f6ebcb-cf31-4ed0-87d9-c21750eae3a6",
                _input=request
            )
        data = ug_response.get("data")
        if data is None:
            return InsertError[RequestGQLModel](
                msg="request to gql_ug @ request_insert returns no data",
                code="71634547-c39b-456e-ae85-281a6f585956",
                _input=request
            )
        rbacInsert = data.get("rbacInsert")
        if rbacInsert is None:
            return InsertError[RequestGQLModel](
                msg=f"request to gql_ug @ request_insert returns no rbac",
                code="26cdbd42-6b7b-4fcc-ab9f-fb7f3396a747",
                _input=request
            )
        __typename = rbacInsert.get("__typename")
        if __typename.endswith("Error") :
            return InsertError[RequestGQLModel](
                msg=f"request to gql_ug @ request_insert returns error {__typename}\n{rbacInsert}",
                code="fc4a4582-b39f-4937-b3d1-71b7d5b69efc",
                _input=request
            )
        
        request.rbacobject_id = IDType(child_rbacobject_id)
        # 2. create submission linked to form
        # TODO zobecnit s digital_form_submission_insert2
        # tento fragment je podobny resolveru digital_form_submission_insert2

        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormFieldGQLModel import DigitalFormFieldGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalFormSectionGQLModel import DigitalFormSectionGQLModel

        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionInsertGQLModel

        from ..DocumentGQLModel.DigitalDocumentGQLModel.helpers import create_SubmissionSectionInsertGQLModel, create_DigitalSubmissionFieldInsertGQLModel

        fieldLoader = DigitalFormFieldGQLModel.getLoader(info=info)
        sectionLoader = DigitalFormSectionGQLModel.getLoader(info=info)

        # ziskat data z tabulek, vsechny sekce a polozky/fieldy, ktere patri k formulari
        form_fields, form_sections = await asyncio.gather(
            fieldLoader.filter_by(form_id=db_row.initial_form_id),
            sectionLoader.filter_by(form_id=db_row.initial_form_id)
        )

        # rekonstruujeme strukturu
        form_section_map = {
            section.id: {
                "section": dataclasses.asdict(section),
                "name": section.name,
                "sections": [],
                "fields": []
            } for section in form_sections
        }

        for section in form_section_map.values():
            parent_id = section["section"]["section_id"]
            if parent_id is None:
                continue
            form_section_map[parent_id]["sections"].append(
                section
            )
        
        form_field_map = {
            field.id: {
                "field": dataclasses.asdict(field),
                "name": field.name,
                "section": form_section_map[field.form_section_id]
            }
            for field in form_fields
        }

        for field in form_field_map.values():
            form_section_id = field["field"]["form_section_id"]
            form_section_map[form_section_id]["fields"].append(field)

        # struktura rekonstruovana
        # submission_id = child_rbacobject_id or uuid.uuid4()
        submission_id = uuid.uuid4()
        submission = DigitalSubmissionInsertGQLModel(
            id=submission_id,
            name=f"FORM: {request.name}",
            form_id=db_row.initial_form_id,
            sections=[], # SubmissionSectionInsertGQLModel()]
            fields=[], # DigitalSubmissionFieldInsertGQLModel()

            rbacobject_id=child_rbacobject_id,
            createdby_id=user_id
        )

        submission.sections = [
            create_SubmissionSectionInsertGQLModel(
                section,
                submission_id=submission_id, # nepouziva se dovodi se jinde
                submission_section_id=None,
                index=index
            )
            for (index, section) in enumerate(form_section_map.values()) if section["section"]["section_id"] is None
        ]

        # submission.fields = [
        #     create_DigitalSubmissionFieldInsertGQLModel(
        #         form_field=form_field,
        #         section_id=id,
        #         submission_id=submission_id,
        #         index=index
        #     )
        #     for (index, form_field) in enumerate(form_section_fields)]


        # 3. setup other attributes
        request.active_submission = submission
        request.set_rbacobject_id(IDType(child_rbacobject_id))
        request.state_id = db_row.state_id
        request.active_submission.state_id = db_row.state_id

        # 5e1d4798-98cd-444b-a9ec-0937c67c6daa
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
                primary_key_name="request_type_id",
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
    async def request_move_to_state(
        self, 
        info: strawberry.types.Info,
        request: typing.Annotated[
            RequestUseTransitionGQLModel,
            strawberry.argument (description="Full description of request to be moved to target state")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Union[UpdateError[RequestGQLModel], RequestGQLModel]:
        # TODO
        # 1. validate that transition from current state to target_state_id is allowed
        
        actinguser = getUserFromInfo(info)
        # submission: DigitalSubmissionGQLModel = await RequestGQLModel.getLoader(info).load(db_row.active_submission_id)
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionGQLModel import DigitalSubmissionInsertGQLModel2
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
        from ..DocumentGQLModel.DigitalDocumentGQLModel.DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
        from .HistoryGQLModel import HistoryInsertGQLModel

        submission_loader = DigitalSubmissionGQLModel.getLoader(info)
        submission = await submission_loader.load(db_row.active_submission_id)
        all_sections = await DigitalSubmissionSectionGQLModel.getLoader(info).filter_by(submission_id=db_row.active_submission_id)
        all_fields = await DigitalSubmissionFieldGQLModel.getLoader(info).filter_by(submission_id=db_row.active_submission_id)

        result = DigitalSubmissionInsertGQLModel2(
            name=submission.name,
            form_id=submission.form_id,
            sections=[],
            fields=[],
            rbacobject_id=submission.rbacobject_id,
            createdby_id=submission.createdby_id,
            state_id=request.target_state_id
        )
        result.id = uuid.uuid4()
        result.name = submission.name
        
        id_register = {}
        new_sections_register = {}
        new_fields_register = {}
        for section in all_sections:
            new_section_id = uuid.uuid4()
            id_register[section.id] = new_section_id
            new_section = SubmissionSectionInsertGQLModel(
                id=new_section_id,
                # name=section.name,
                index=section.index,
                section_id=section.section_id,
                submission_id=result.id,
                form_section_id=section.form_section_id,
                state_id=request.target_state_id,
                rbacobject_id=section.rbacobject_id
            )
            new_sections_register[section.id] = new_section
            
        for field in all_fields:
            new_field_id = uuid.uuid4()
            # id_register[field.id] = new_field_id
            new_field = DigitalSubmissionFieldInsertGQLModel(
                id=new_field_id,
                value=field.value,
                field_id=field.field_id,
                section_id=id_register.get(field.section_id),
                submission_id=result.id,
                state_id=request.target_state_id,
                rbacobject_id=field.rbacobject_id
            )
            new_fields_register[field.id] = new_field
        
        for master_key, section in new_sections_register.items():
            section.sections = [
                child_section
                for child_key, child_section in new_sections_register.items()
                if master_key == child_section.section_id
            ]

        for master_key, section in new_sections_register.items():
            section.fields = [
                field
                for field in new_fields_register.values()
                if field.section_id == section.id
            ]

        for master_key, section in new_sections_register.items():
            section.section_id = id_register.get(section.section_id)

        result.sections = [
            section
            for key, section in new_sections_register.items()
            if section.section_id is None
        ]
        
        entity = await result.intoModel(info=info)
        # print(f"Submitting new submission for request_move_to_state: {entity}")
        db_result = await submission_loader.insert(entity)

        history = HistoryInsertGQLModel(
            request_id=request.id,
            submission_id=db_row.active_submission_id,
            state_id=db_row.state_id,
            name=request.msg,
            createdby_id=IDType(actinguser["id"]),
            rbacobject_id=db_row.rbacobject_id
        )
        await HistoryInsertGQLModel.getLoader(info).insert(await history.intoModel(info=info))

        request.active_submission_id = result.id
        request.changedby_id = IDType(actinguser["id"])
        return await Update[RequestGQLModel].DoItSafeWay(
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
    async def request_delete(
        self, 
        info: strawberry.types.Info,
        request: typing.Annotated[
            RequestDeleteGQLModel,
            strawberry.argument (description="Identification of the request record to be removed from db")
        ],
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[RequestGQLModel]]:
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