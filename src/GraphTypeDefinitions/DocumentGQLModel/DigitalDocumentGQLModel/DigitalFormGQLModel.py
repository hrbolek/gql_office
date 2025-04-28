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
from ..DocumentInterfaceGQLModel import DocumentInterfaceGQLModel

DigitalFormSectionGQLModel = typing.Annotated["DigitalFormSectionGQLModel", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalFormSectionInputFilter = typing.Annotated["DigitalFormSectionInputFilter", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalSubmissionGQLModel = typing.Annotated["DigitalSubmissionGQLModel", strawberry.lazy(".DigitalSubmissionGQLModel")]
DigitalSubmissionInputFilter = typing.Annotated["DigitalSubmissionInputFilter", strawberry.lazy(".DigitalSubmissionGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFormInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    parent_id: IDType


@strawberry.federation.type(
    keys=["id"], description="""Represents a digital form used to capture user input.
Defines the overall structure of the form and stores its submissions."""
)
class DigitalFormGQLModel(BaseGQLModel, DocumentInterfaceGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormModel


    sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital Document sections""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="form_id", whereType=DigitalFormSectionInputFilter)
    )

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
    digital_document_by_id: typing.Optional[DigitalFormGQLModel] = strawberry.field(
        description="""Get a DigitalForm by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalFormGQLModel.load_with_loader
    )

    digital_document_page: typing.List[DigitalFormGQLModel] = strawberry.field(
        description="""Get all DigitalForms with pagination""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["DigitalFormGQLModel"](whereType=DigitalFormInputFilter)
    )

    
@strawberry.input(
    description="""DigitalForm insert mutation input type, can contain whole structure"""
)
class DigitalFormInsertGQLModel:
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
    )

    from .DigitalFormSectionGQLModel import DigitalFormSectionInsertGQLModel
    sections: typing.Optional[typing.List[DigitalFormSectionInsertGQLModel]] = strawberry.field(
        description="sections with fields and sections",
        default_factory=list
    )

async def digital_form_insert_internal(self, info: strawberry.types.Info, digital_form: DigitalFormInsertGQLModel):
    from .DigitalFormSectionGQLModel import digital_form_section_insert_internal, from_SectionInputIntoSectionModel
    if digital_form.id is None:
        digital_form.id = uuid.uuid4()
    # sections = digital_form.sections
    digital_form.sections = [from_SectionInputIntoSectionModel(info, section) for section in digital_form.sections]
    master_result = await Insert[DigitalFormGQLModel].DoItSafeWay(info=info, entity=digital_form)
    # failed = getattr(master_result, "failed", False)
    # if failed:
    #     msg_error = getattr(master_result, "msg", "")
    #     return InsertError[DigitalFormGQLModel](msg=msg_error, _input=digital_form)

    # for section in sections:
    #     if section.id is None:
    #         section.id = uuid.uuid4()
    #     section.parent_id = digital_form.id

    # msg_error = None
    # for section in digital_form.sections:
    #     result = await digital_form_section_insert_internal(self, info=info, digital_form_section=section)
    #     failed = getattr(result, "failed", False)
    #     if failed:
    #         msg_error = getattr(result, "msg", "")
    #     break

    # if msg_error:
    #     return InsertError[DigitalFormGQLModel](msg=msg_error, _input=digital_form)
    return master_result


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


@strawberry.type(
    description="""DigitalForm mutation"""
)
class DigitalFormMutation:
    @strawberry.mutation(
        description="""Insert a DigitalForm""",
        permission_classes=[
            SimpleInsertPermission[DigitalFormGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_insert(
        self,
        info: strawberry.types.Info,
        digital_form: DigitalFormInsertGQLModel
    ) -> typing.Union[DigitalFormGQLModel, InsertError[DigitalFormGQLModel]]:
        return await digital_form_insert_internal(self, info=info, digital_form=digital_form)
    
    @strawberry.mutation(
        description="""Update a DigitalForm""",
        permission_classes=[
            SimpleUpdatePermission[DigitalFormGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_update(
        self,
        info: strawberry.types.Info,
        digital_form: DigitalFormUpdateGQLModel
    ) -> typing.Union[DigitalFormGQLModel, UpdateError[DigitalFormGQLModel]]:
        return await Update[DigitalFormGQLModel].DoItSafeWay(info=info, entity=digital_form)
    
    @strawberry.mutation(
        description="""Delete a DigitalForm""",
        permission_classes=[
            SimpleDeletePermission[DigitalFormGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_delete(
        self,
        info: strawberry.types.Info,
        digital_form: DigitalFormDeleteGQLModel
    ) -> typing.Optional[DeleteError[DigitalFormGQLModel]]:
        return await Delete[DigitalFormGQLModel].DoItSafeWay(info=info, entity=digital_form)