import asyncio
import uuid
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
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType
from ..DocumentInterfaceGQLModel import DocumentInterfaceGQLModel

DigitalFormSectionGQLModel = typing.Annotated["DigitalFormSectionGQLModel", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalFormSectionInputFilter = typing.Annotated["DigitalFormSectionInputFilter", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalSubmissionGQLModel = typing.Annotated["DigitalSubmissionGQLModel", strawberry.lazy(".DigitalSubmissionGQLModel")]
DigitalSubmissionInputFilter = typing.Annotated["DigitalSubmissionInputFilter", strawberry.lazy(".DigitalSubmissionGQLModel")]

@createInputs2
class DigitalFormInputFilter:
    name: str = strawberry.field(description="name of the form", default=None)
    name_en: str = strawberry.field(description="english name of the form", default=None)
    description: str = strawberry.field(description="description, use case of the form", default=None)
    id: IDType = strawberry.field(description="primary key", default=None)
    parent_id: IDType = strawberry.field(description="parent of this form", default=None)

    sections: DigitalFormSectionInputFilter = strawberry.field(description="filter based on sections", default=None)


@strawberry.federation.type(
    keys=["id"], description="""Represents a digital form used to capture user input.
Defines the overall structure of the form and stores its submissions."""
)
class DigitalFormGQLModel(BaseGQLModel, DocumentInterfaceGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormModel


    @strawberry.field(
        description="""Digital Document sections""",
        permission_classes=[
            OnlyForAuthentized
        ],
    )
    async def sections(self, info: strawberry.types.Info) -> typing.List["DigitalFormSectionGQLModel"]:
        from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel
        loader = DigitalFormSectionGQLModel.getLoader(info)
        db_rows = await loader.filter_by(form_id=self.id)
        #TODO optimize filtering at loader level
        results = (r for r in db_rows if r.section_id is None)
        # results = [r for r in db_rows]
        # print("DigitalFormGQLModel.sections", results)

        return (DigitalFormSectionGQLModel.from_dataclass(row) for row in results)

    # sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
    #     description="""Digital Document sections""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="form_id", whereType=DigitalFormSectionInputFilter)
    # )

    all_sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital Document sections regadless structure of document""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="form_id", whereType=DigitalFormSectionInputFilter)
    )
    # @strawberry.field(
    #     description="""Digital Document sections""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ]
    # )
    # async def sections(
    #     self, 
    #     info: strawberry.types.Info,
    #     skip: typing.Annotated[typing.Optional[int], strawberry.argument(description="how many entities will be ignored")]=0, 
    #     limit: typing.Annotated[typing.Optional[int], strawberry.argument(description="how many entities will be taken")]=10, 
    #     orderby: typing.Annotated[typing.Optional[str], strawberry.argument(description="name of field which will determite the order")]=None, 
    #     where: typing.Annotated[typing.Optional[DigitalFormSectionInputFilter], strawberry.argument(description="filter")]=None,         
    # ) -> typing.List[DigitalFormSectionGQLModel]:
    #     from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel
    #     extendedfilter = {"form_id": self.id}
    #     loader = DigitalFormSectionGQLModel.getLoader(info=info)
    #     where = None if where is None else strawberry.asdict(where)
    #     results = await loader.page(
    #         skip=skip, 
    #         limit=limit, 
    #         orderby=orderby, 
    #         where=where, 
    #         extendedfilter=extendedfilter
    #     )
    #     return (DigitalFormSectionGQLModel.from_dataclass(result) for result in results)        
        


    submissions: typing.List["DigitalSubmissionGQLModel"] = strawberry.field(
        description="""Digital Document submissions""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionGQLModel"](fkey_field_name="form_id", whereType=DigitalSubmissionInputFilter)
    )

@strawberry.type(
    description=""""""
)
class DigitalFormQuery:
    digital_form_by_id: typing.Optional[DigitalFormGQLModel] = strawberry.field(
        description="""Get a DigitalForm by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalFormGQLModel.load_with_loader
    )

    digital_form_page: typing.List[DigitalFormGQLModel] = strawberry.field(
        description="""Get all DigitalForms with pagination""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["DigitalFormGQLModel"](whereType=DigitalFormInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin, TreeInputStructureMixin

@strawberry.input(
    description="""DigitalForm insert mutation input type, can contain whole structure"""
)
class DigitalFormInsertGQLModel(InputModelMixin):
    getLoader = DigitalFormGQLModel.getLoader

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalForm name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalForm eng name""",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalForm id client generated""",
        default=None
        # default_factory=uuid.uuid4
    )

    from .DigitalFormSectionGQLModel import DigitalFormSectionInsertGQLModel
    sections: typing.Optional[typing.List[DigitalFormSectionInsertGQLModel]] = strawberry.field(
        description="sections with fields and sections",
        default_factory=list
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""DigitalForm update mutation"""
)
class DigitalFormUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalForm id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalForm lastchange"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalForm name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalForm eng name""",
        default=None
    )

@strawberry.input(
    description="""DigitalForm delete mutation"""
)
class DigitalFormDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalForm id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalForm lastchange"""
    )


@strawberry.interface(
    description="""DigitalForm mutations"""
)
class DigitalFormMutation:
    @strawberry.mutation(
        description="""Insert a DigitalForm""",
        # permission_classes=[
        #     # SimpleInsertPermission[DigitalFormGQLModel](roles=["administrátor"])
            
        # ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, DigitalFormGQLModel](roles=["superadmin"]),
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            # UserAccessControlExtension[InsertError, DigitalFormGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[InsertError, DigitalFormGQLModel](),
            # RbacProviderExtension[InsertError, DigitalFormGQLModel](),
            # LoadDataExtension[InsertError, DigitalFormGQLModel]()
        ],
    )
    async def digital_form_insert(
        self,
        info: strawberry.types.Info,
        digital_form: typing.Annotated[DigitalFormInsertGQLModel, strawberry.argument (description="full structure of the form, including sections and fields")],
        user_roles: typing.List[typing.Any],
    ) -> typing.Union[DigitalFormGQLModel, InsertError[DigitalFormGQLModel]]:
        # digital_form.rbacobject_id = "d75d64a4-bf5f-43c5-9c14-8fda7aff6c09"
        # modelinstance = digital_form.intoModel(info=info)
        # print(f"{strawberry.asdict(modelinstance)}")
        # for section in modelinstance.sections:
        #     print(f"section: {strawberry.asdict(section)}")
        return await Insert[DigitalFormGQLModel].DoItSafeWay(info=info, entity=digital_form)
        # return await digital_form_insert_internal(self, info=info, digital_form=digital_form)
    
    @strawberry.mutation(
        description="""Update a DigitalForm""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, DigitalFormGQLModel](
                roles=[
                    "procesní administrátor"
                ]),
            UserRoleProviderExtension[UpdateError, DigitalFormGQLModel](),
            RbacProviderExtension[UpdateError, DigitalFormGQLModel](),
            LoadDataExtension[UpdateError, DigitalFormGQLModel]()
        ]
    )
    async def digital_form_update(
        self,
        info: strawberry.types.Info,
        digital_form: typing.Annotated[DigitalFormUpdateGQLModel, strawberry.argument (description="atributes of the form, which can be updated")],
        user_roles: typing.List[typing.Any],
        db_row: typing.Any,
        rbacobject_id: IDType
    ) -> typing.Union[DigitalFormGQLModel, UpdateError[DigitalFormGQLModel]]:
        return await Update[DigitalFormGQLModel].DoItSafeWay(info=info, entity=digital_form)
    
    @strawberry.mutation(
        description="""Delete a DigitalForm""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, DigitalFormGQLModel](
                roles=[
                    "procesní administrátor"
                ]),
            UserRoleProviderExtension[UpdateError, DigitalFormGQLModel](),
            RbacProviderExtension[UpdateError, DigitalFormGQLModel](),
            LoadDataExtension[UpdateError, DigitalFormGQLModel]()
        ]
    )
    async def digital_form_delete(
        self,
        info: strawberry.types.Info,
        digital_form: typing.Annotated[DigitalFormDeleteGQLModel, strawberry.argument(description="id and lastchange of the form, which will be deleted")],
        user_roles: typing.List[typing.Any],
        db_row: typing.Any,
        rbacobject_id: IDType
    ) -> typing.Optional[DeleteError[DigitalFormGQLModel]]:
        return await Delete[DigitalFormGQLModel].DoItSafeWay(info=info, entity=digital_form)