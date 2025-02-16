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

DigitalFieldSubmissionGQLModel = typing.Annotated["DigitalFieldSubmissionGQLModel", strawberry.lazy(".DigitalFieldSubmissionGQLModel")]
DigitalFieldSubmissionInputFilter = typing.Annotated["DigitalFieldSubmissionInputFilter", strawberry.lazy(".DigitalFieldSubmissionGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFormSubmissionInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    parent_id: IDType


@strawberry.federation.type(
    description="""Represents a submission of a digital form filled out by a user.
Aggregates responses for all the fields defined in the form."""
)
class DigitalFormSubmissionGQLModel(BaseGQLModel, DocumentGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormSubmissionModel
    

    submitted_fields: typing.List["DigitalFieldSubmissionGQLModel"] = strawberry.field(
        description="""Digital Form Submission fields assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFieldSubmissionGQLModel"](fkey_field_name="submission_id", whereType=DigitalFieldSubmissionInputFilter)
    )