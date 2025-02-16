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

DigitalFormFieldGQLModel = typing.Annotated["DigitalFormFieldGQLModel", strawberry.lazy(".DigitalFormFieldGQLModel")]
DigitalFormSubmissionGQLModel = typing.Annotated["DigitalFormSubmissionGQLModel", strawberry.lazy(".DigitalFormSubmissionGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("...StateGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFieldSubmissionInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    state_id: IDType
    field_id: IDType
    submission_id: IDType


@strawberry.federation.type(
    description="""Represents a response for a specific form field within a submission.
Links the user's provided value with the corresponding form field."""
)
class DigitalFieldSubmissionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFieldResponseModel

    value: typing.Optional[str] = strawberry.field(
        description="""Digital Field Response value typed by a user""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    field_id: typing.Optional[IDType] = strawberry.field(
        description="""Digital Field id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    submission_id: typing.Optional[IDType] = strawberry.field(
        description="""Digital Form Submission id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    field: typing.Optional['DigitalFormFieldGQLModel'] = strawberry.field(
        description="""Digital Field""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalFormFieldGQLModel"](fkey_field_name="field_id")
    )

    submission: typing.Optional['DigitalFormSubmissionGQLModel'] = strawberry.field(
        description="""Digital Form Submission""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalFormSubmissionGQLModel"](fkey_field_name="submission_id")
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""State id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state: typing.Optional['StateGQLModel'] = strawberry.field(
        description="""State""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StateGQLModel"](fkey_field_name="state_id")
    )