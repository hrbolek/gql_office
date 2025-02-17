import asyncio
import dataclasses
import datetime
import typing
import strawberry
import uuid

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

from ...BaseGQLModel import BaseGQLModel, IDType

DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy(".DigitalFormGQLModel")]
DigitalFormFieldGQLModel = typing.Annotated["DigitalFormFieldGQLModel", strawberry.lazy(".DigitalFormFieldGQLModel")]
DigitalFormFieldInputFilter = typing.Annotated["DigitalFormFieldInputFilter", strawberry.lazy(".DigitalFormFieldGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFormSectionInputFilter:
    id: IDType
    label: str
    name: str
    label_en: str
    description: str
    parent_id: IDType

@strawberry.federation.type(description="""Represents a section (group) of a digital form.
Supports nested sections and repetition.""")
class DigitalFormSectionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormSectionModel

    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Label for display""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""name for reference, must be unique and must start with a capitalized letter""",
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

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Digital document form section parent id which this section belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ]
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
    async def parent(self, info: strawberry.types.Info) -> typing.Union["DigitalFormSectionGQLModel", DigitalFormGQLModel]:
        from .DigitalFormGQLModel import DigitalFormGQLModel

        futures = [DigitalFormGQLModel.load_with_loader(self.parent_id), DigitalFormSectionGQLModel.load_with_loader(self.parent_id)]
        [document, section] = await asyncio.gather(*futures)
        return document or section
    

    sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital document form section children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="parent_id", whereType=DigitalFormSectionInputFilter)
    )

    fields: typing.List["DigitalFormFieldGQLModel"] = strawberry.field(
        description="""Digital document form section fields""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormFieldGQLModel"](fkey_field_name="form_section_id", whereType=DigitalFormFieldInputFilter)
    )

    order: int = strawberry.field(
        description="""Order of the section""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repatable_min: int = strawberry.field(
        description="""Minimum number of repetitions""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repatable_max: int = strawberry.field(
        description="""Maximum number of repetitions""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repeatable: bool = strawberry.field(
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

    
@strawberry.input(
    description="""DigitalFormSection insert mutation"""
)
class DigitalFormSectionInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection eng name""",
        default=None
    )
    parent_id: IDType = strawberry.field(
        description="""DigitalFormSection master id"""
    )
    id: IDType = strawberry.field(
        description="""DigitalFormSection id client generated"""
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

async def digital_form_section_insert_internal(
        self,
        info: strawberry.types.Info,
        digital_form_section: DigitalFormSectionInsertGQLModel
    ) -> typing.Union[DigitalFormSectionGQLModel, InsertError[DigitalFormSectionGQLModel]]:
        from .DigitalFormFieldGQLModel import digital_form_field_insert_internal
        error_msg = None

        #TODO check what parent_id is

        if digital_form_section.id is None:
            digital_form_section.id = uuid.uuid4()

        masterresult = await Insert[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)
        failed = getattr(masterresult, "failed", False)
        if failed:
            error_msg = getattr(masterresult, "msg", None)
            return InsertError[DigitalFormSectionGQLModel](msg=error_msg, _input=digital_form_section)

        for form_field in digital_form_section.fields:
            if form_field.id is None:
                form_field.id = uuid.uuid4()
            form_field.form_section_id = digital_form_section.id

        for form_field in digital_form_section.fields:
            result = await digital_form_field_insert_internal(self, info=info, form_field=form_field)
            failed = getattr(result, "failed", False)
            if failed:
                error_msg = getattr(result, "msg", None)
                break

        for form_section in digital_form_section.sections:
            if form_section.id is None:
                form_section.id = uuid.uuid4()
            result = await digital_form_section_insert_internal(self, info=info, digital_form_section=form_section)
            failed = getattr(result, "failed", False)
            if failed:
                error_msg = getattr(result, "msg", None)
                break

        if error_msg:
            return InsertError[DigitalFormSectionGQLModel](msg=error_msg, _input=digital_form_section)
        
        return masterresult

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
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSection eng name""",
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


@strawberry.type(
    description="""DigitalFormSection mutation"""
)
class DigitalFormSectionMutation:
    @strawberry.mutation(
        description="""Insert a DigitalFormSection""",
        permission_classes=[
            SimpleInsertPermission[DigitalFormSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_section_insert(
        self,
        info: strawberry.types.Info,
        digital_form_section: DigitalFormSectionInsertGQLModel
    ) -> typing.Union[DigitalFormSectionGQLModel, InsertError[DigitalFormSectionGQLModel]]:
        return await digital_form_section_insert_internal(self=self, info=info, entity=digital_form_section)
    
    @strawberry.mutation(
        description="""Update a DigitalFormSection""",
        permission_classes=[
            SimpleUpdatePermission[DigitalFormSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_section_update(
        self,
        info: strawberry.types.Info,
        digital_form_section: DigitalFormSectionUpdateGQLModel
    ) -> typing.Union[DigitalFormSectionGQLModel, UpdateError[DigitalFormSectionGQLModel]]:
        return await Update[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)
    
    @strawberry.mutation(
        description="""Delete a DigitalFormSection""",
        permission_classes=[
            SimpleDeletePermission[DigitalFormSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_section_delete(
        self,
        info: strawberry.types.Info,
        digital_form_section: DigitalFormSectionDeleteGQLModel
    ) -> typing.Optional[DeleteError[DigitalFormSectionGQLModel]]:
        return await Delete[DigitalFormSectionGQLModel].DoItSafeWay(info=info, entity=digital_form_section)