import asyncio
import dataclasses
import datetime
import typing
import strawberry
import uuid

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,
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
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension


from ...BaseGQLModel import BaseGQLModel, IDType

DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy(".DigitalFormGQLModel")]
DigitalFormFieldGQLModel = typing.Annotated["DigitalFormFieldGQLModel", strawberry.lazy(".DigitalFormFieldGQLModel")]
DigitalFormFieldInputFilter = typing.Annotated["DigitalFormFieldInputFilter", strawberry.lazy(".DigitalFormFieldGQLModel")]

@createInputs2
class DigitalFormSectionInputFilter:
    id: IDType = strawberry.field(description="primary key")
    label: str = strawberry.field(description="label for section")
    name: str = strawberry.field(description="name of section")
    label_en: str = strawberry.field(description="english label for section")
    description: str = strawberry.field(description="description of section")
    
    section_id: IDType
    form_id: IDType

@strawberry.federation.type(
    keys=["id"], description="""Represents a section (group) of a digital form.
Supports nested sections and repetition. Contains fields definition""")
class DigitalFormSectionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormSectionModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""name for reference, must be unique and must start with a capitalized letter""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    path: typing.Optional[str] = strawberry.field(
        description="aka materialized path",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Label for display""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    label_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Label for display in english""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Explanation of the form section""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    # section_id: strawberry.Private[IDType] = None
    # form_id: strawberry.Private[IDType] = None

    section_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Digital document form section parent id which this section belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Digital document form parent id which this section belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form: typing.Optional[DigitalFormGQLModel] = strawberry.field(
        description="""Digital document form parent which this section belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[DigitalFormGQLModel](fkey_field_name="form_id")
    )

    section: typing.Optional["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital document form section parent which this section belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalFormSectionGQLModel"](fkey_field_name="section_id")
    )

    # parent: typing.Optional["DigitalFormSectionGQLModel"] = strawberry.field(
    #     description="""Digital document form section parent which this section belongs to""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=ScalarResolver["DigitalFormSectionGQLModel"](fkey_field_name="parent_id")
    # )

    @strawberry.field(
        description=""""form section or document """,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def parent(self, info: strawberry.types.Info) -> typing.Union["DigitalFormSectionGQLModel", DigitalFormGQLModel, None]:
        from .DigitalFormGQLModel import DigitalFormGQLModel

        futures = [DigitalFormGQLModel.load_with_loader(info=info, id=self.form_id), DigitalFormSectionGQLModel.load_with_loader(info=info, id=self.section_id)]
        [document, section] = await asyncio.gather(*futures)
        return document or section
    

    sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital document form section children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="section_id", whereType=DigitalFormSectionInputFilter)
    )

    fields: typing.List["DigitalFormFieldGQLModel"] = strawberry.field(
        description="""Digital document form section fields""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormFieldGQLModel"](fkey_field_name="form_section_id", whereType=DigitalFormFieldInputFilter)
    )

    order: typing.Optional[int] = strawberry.field(
        default=None,
        description="""Order of the section""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repeatable_min: typing.Optional[int] = strawberry.field(
        default=None,
        description="""Minimum number of repetitions""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repeatable_max: typing.Optional[int] = strawberry.field(
        default=None,
        description="""Maximum number of repetitions""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repeatable: typing.Optional[bool] = strawberry.field(
        default=None,
        description="""Is section repeatable""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )



@strawberry.interface(
    description=""""""
)
class DigitalFormSectionQuery:
    digital_form_section_by_id: typing.Optional[DigitalFormSectionGQLModel] = strawberry.field(
        description="""Get a DigitalFormSection by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalFormSectionGQLModel.load_with_loader
    )

    digital_form_section_page: typing.List[DigitalFormSectionGQLModel] = strawberry.field(
        description="""Get a page of DigitalFormSections""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalFormSectionInputFilter](whereType=DigitalFormSectionInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin, TreeInputStructureMixin
@strawberry.input(
    description="""DigitalFormSection insert mutation"""
)
class DigitalFormSectionInsertGQLModel(TreeInputStructureMixin):
    getLoader = DigitalFormSectionGQLModel.getLoader 

    form_id: IDType = strawberry.field(
        description="""DigitalForm id which the section will be part of"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection name""",
        default=None
    )
    label: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection label""",
        default=None
    )
    label_en: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection eng label""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection description / explanation""",
        default=None
    )
    order: typing.Optional[int] = strawberry.field(
        description="""DigitalFormSection order""",
        default=None
    )

    section_id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalFormSection master id""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalFormSection id client generated""",
        default=None,
        # default_factory=lambda: uuid.uuid4()
    )

    repeatable_min: typing.Optional[int] = strawberry.field(
        description="""Minimum number of repetitions""",
        default=None
    )
    repeatable_max: typing.Optional[int] = strawberry.field(
        description="""Maximum number of repetitions""",
        default=None
    )
    repeatable: typing.Optional[bool] = strawberry.field(
        description="""Is section repeatable""",
        default=False
    )

    from .DigitalFormFieldGQLModel import DigitalFormFieldInsertGQLModel

    fields: typing.Optional[typing.List[DigitalFormFieldInsertGQLModel]] = strawberry.field(
        description="fields inside this section",
        default_factory=list
    )
    sections: typing.Optional[typing.List["DigitalFormSectionInsertGQLModel"]] = strawberry.field(
        description="sections inside this section",
        default_factory=list
    )

    path: strawberry.Private[str] = None

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

    # from ...utils import intoModel

# def from_FieldInputIntoFieldModel(info: strawberry.types.Info, field):
#     from .DigitalFormFieldGQLModel import DigitalFormFieldGQLModel
#     FieldLoader = DigitalFormFieldGQLModel.getLoader(info=info)
#     FieldDBModel = FieldLoader.getModel()

#     result = {**strawberry.asdict(field)}
#     return FieldDBModel(**result)


# def from_SectionInputIntoSectionModel(info: strawberry.types.Info, section: DigitalFormSectionInsertGQLModel) -> DigitalFormSectionGQLModel:
#     from .DigitalFormFieldGQLModel import DigitalFormFieldGQLModel
#     SectionLoader = DigitalFormSectionGQLModel.getLoader(info=info)
#     SectionDBModel = SectionLoader.getModel()
#     # FieldLoader = DigitalFormFieldGQLModel.getLoader(info=info)
#     # FieldDBModel = FieldLoader.getModel()
#     if section.id is None:
#         section.id = uuid.uuid4()
#     result = {**strawberry.asdict(section)}
#     sections = result.pop("sections", None)
#     fields = result.pop("fields", None)
#     if sections:
#         result["sections"] = [from_SectionInputIntoSectionModel(info, section) for section in sections]
#     if fields:
#         result["fields"] = [from_FieldInputIntoFieldModel(info, field) for field in fields]
#     return SectionDBModel(**result)
    
# async def digital_form_section_insert_internal(
#         self,
#         info: strawberry.types.Info,
#         digital_form_section: DigitalFormSectionInsertGQLModel
#     ) -> typing.Union[DigitalFormSectionGQLModel, InsertError[DigitalFormSectionGQLModel]]:
#         from .DigitalFormFieldGQLModel import digital_form_field_insert_internal
#         error_msg = None

#         #TODO check what parent_id is

#         if digital_form_section.id is None:
#             digital_form_section.id = uuid.uuid4()
#         sections = digital_form_section.sections
#         fields = digital_form_section.fields
        
#         digital_form_section.sections = [from_SectionInputIntoSectionModel(info=info, section=section) for section in sections]
#         digital_form_section.fields = [from_FieldInputIntoFieldModel(info=info, field=field) for field in fields]

#         masterresult = await Insert[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)
#         # failed = getattr(masterresult, "failed", False)
#         # if failed:
#         #     error_msg = getattr(masterresult, "msg", None)
#         #     return InsertError[DigitalFormSectionGQLModel](msg=error_msg, _input=digital_form_section)

#         # for form_field in fields:
#         #     if form_field.id is None:
#         #         form_field.id = uuid.uuid4()
#         #     form_field.form_section_id = digital_form_section.id

#         # for form_field in fields:
#         #     form_field.form_id = digital_form_section.form_id
#         #     form_field.form_section_id = digital_form_section.id
#         #     result = await digital_form_field_insert_internal(self, info=info, form_field=form_field)
#         #     failed = getattr(result, "failed", False)
#         #     if failed:
#         #         error_msg = getattr(result, "msg", None)
#         #         break

#         # for form_section in sections:
#         #     if form_section.id is None:
#         #         form_section.id = uuid.uuid4()
            
#         #     result = await digital_form_section_insert_internal(self, info=info, digital_form_section=form_section)
#         #     failed = getattr(result, "failed", False)
#         #     if failed:
#         #         error_msg = getattr(result, "msg", None)
#         #         break

#         # if error_msg:
#         #     return InsertError[DigitalFormSectionGQLModel](msg=error_msg, _input=digital_form_section)
        
#         return masterresult

@strawberry.input(
    description="""DigitalFormSection update mutation"""
)
class DigitalFormSectionUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalFormSection id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalFormSection lastchange"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection name""",
        default=None
    )
    label: typing.Optional[str] = strawberry.field(
        description="""visual label""",
        default=None
    )
    label_en: typing.Optional[str] = strawberry.field(
        description="""visual label in english""",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="""detailed description""",
        default=None
    )
    order: typing.Optional[int] = strawberry.field(
        description="""parameter for ordering within siblings""",
        default=None
    )
    repeatable_min: typing.Optional[int] = strawberry.field(
        description="""Minimum number of repetitions""",
        default=None
    )
    repeatable_max: typing.Optional[int] = strawberry.field(
        description="""Maximum number of repetitions""",
        default=None
    )
    repeatable: typing.Optional[bool] = strawberry.field(
        description="""Is section repeatable""",
        default=None
    )

@strawberry.input(
    description="""DigitalFormSection delete mutation"""
)
class DigitalFormSectionDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalFormSection id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalFormSection lastchange"""
    )


@strawberry.interface(
    description="""DigitalFormSection mutation"""
)
class DigitalFormSectionMutation:
    from .DigitalFormGQLModel import DigitalFormGQLModel
    @strawberry.mutation(
        description="""Insert a DigitalFormSection""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, DigitalFormSectionGQLModel](
                roles=[
                    "procesní administrátor", 
                ]
            ),
            UserRoleProviderExtension[InsertError, DigitalFormSectionGQLModel](),
            RbacProviderExtension[InsertError, DigitalFormSectionGQLModel](),
            LoadDataExtension[InsertError, DigitalFormSectionGQLModel](
                getLoader=DigitalFormGQLModel.getLoader,
                primary_key_name="form_id"
            )
        ]
    )
    async def digital_form_section_insert(
        self,
        info: strawberry.types.Info,
        digital_form_section: typing.Annotated[DigitalFormSectionInsertGQLModel, strawberry.argument(description="form section attributes, including fields to be inserted")],
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[DigitalFormSectionGQLModel, InsertError[DigitalFormSectionGQLModel]]:
        digital_form_section.rbacobject_id = rbacobject_id
        return await Insert[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)
    
    @strawberry.mutation(
        description="""Update a DigitalFormSection""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, DigitalFormSectionGQLModel](
                roles=[
                    "procesní administrátor", 
                ]
            ),
            UserRoleProviderExtension[InsertError, DigitalFormSectionGQLModel](),
            RbacProviderExtension[InsertError, DigitalFormSectionGQLModel](),
            LoadDataExtension[InsertError, DigitalFormSectionGQLModel]()
        ]
    )
    async def digital_form_section_update(
        self,
        info: strawberry.types.Info,
        digital_form_section: typing.Annotated[DigitalFormSectionUpdateGQLModel, strawberry.argument(description="form section attributes, to be updated")],
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[DigitalFormSectionGQLModel, UpdateError[DigitalFormSectionGQLModel]]:
        return await Update[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)
    
    @strawberry.mutation(
        description="""Delete a DigitalFormSection""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, DigitalFormSectionGQLModel](
                roles=[
                    "procesní administrátor", 
                ]
            ),
            UserRoleProviderExtension[InsertError, DigitalFormSectionGQLModel](),
            RbacProviderExtension[InsertError, DigitalFormSectionGQLModel](),
            LoadDataExtension[InsertError, DigitalFormSectionGQLModel]()
        ]
    )
    async def digital_form_section_delete(
        self,
        info: strawberry.types.Info,
        digital_form_section: typing.Annotated[DigitalFormSectionDeleteGQLModel, strawberry.argument(description="id and lastchange of form section to be deleted")],
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[DigitalFormSectionGQLModel]]:
        return await Delete[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)