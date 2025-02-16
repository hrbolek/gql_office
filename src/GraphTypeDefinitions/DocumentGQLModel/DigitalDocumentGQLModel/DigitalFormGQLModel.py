import asyncio
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
from ..DocumentGQLModel import DocumentGQLModel

DigitalFormSectionGQLModel = typing.Annotated["DigitalFormSectionGQLModel", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalFormSectionInputFilter = typing.Annotated["DigitalFormSectionInputFilter", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalFormSubmissionGQLModel = typing.Annotated["DigitalFormSubmissionGQLModel", strawberry.lazy(".DigitalFormSubmissionGQLModel")]
DigitalFormSubmissionInputFilter = typing.Annotated["DigitalFormSubmissionInputFilter", strawberry.lazy(".DigitalFormSubmissionGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFormInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    parent_id: IDType


@strawberry.federation.type(
    description="""Represents a digital form used to capture user input.
Defines the overall structure of the form and stores its submissions."""
)
class DigitalFormGQLModel(BaseGQLModel, DocumentGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormModel


    sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital Document sections""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="document_id", whereType=DigitalFormSectionInputFilter)
    )

    submissions: typing.List["DigitalFormSubmissionGQLModel"] = strawberry.field(
        description="""Digital Document submissions""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSubmissionGQLModel"](fkey_field_name="document_id", whereType=DigitalFormSubmissionInputFilter)
    )

@strawberry.interface(
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

