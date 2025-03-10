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
DigitalSubmissionGQLModel = typing.Annotated["DigitalSubmissionGQLModel", strawberry.lazy(".DigitalSubmissionGQLModel")]
DigitalSubmissionSectionGQLModel = typing.Annotated["DigitalSubmissionSectionGQLModel", strawberry.lazy(".DigitalSubmissionSectionGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("...StateGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalSubmissionFieldInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    state_id: IDType
    field_id: IDType
    submission_id: IDType


@strawberry.federation.type(
    keys=["id"], description="""Represents a response for a specific submission field within a submission.
Links the user's provided value with the corresponding submission field."""
)
class DigitalSubmissionFieldGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalSubmissionFieldModel

    path: typing.Optional[str] = strawberry.field(
        description="aka materialized path",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    
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

    section_id: typing.Optional[IDType] = strawberry.field(
        description="""Digital Form Submission Section id""",
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

    section: typing.Optional['DigitalSubmissionSectionGQLModel'] = strawberry.field(
        description="""Digital Form Submission Section """,
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="section_id")
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



@strawberry.input(description="DigitalFormField insert parameter description")
class DigitalSubmissionFieldInsertGQLModel:
    type_id: IDType = strawberry.field(description="type id of the field")
    submission_section_id: IDType = strawberry.field(description="section id where the field is placed")
    id: typing.Optional[IDType] = strawberry.field(description="client side generated id", default=None)
    
@strawberry.input(description="DigitalSubmissionField insert parameter description")
class DigitalSubmissionFieldUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    type_id: typing.Optional[IDType] = strawberry.field(description="type id of the field", default=None)
    
@strawberry.input(description="DigitalSubmissionField insert parameter description")
class DigitalSubmissionFieldDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


async def digital_submission_field_insert_internal(self, info: strawberry.types.Info, submission_field: DigitalSubmissionFieldInsertGQLModel):
    return await Insert[DigitalSubmissionFieldGQLModel].DoItSafeWay(info=info, entity=submission_field)

@strawberry.type(
    description=""
)
class DigitalSubmissionFieldMutation:
    @strawberry.mutation(
        description="""Insert a DigitalSubmissionField""",
        permission_classes=[
            SimpleInsertPermission[DigitalSubmissionFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_submission_field_insert(
        self,
        info: strawberry.types.Info,
        submission_field: DigitalSubmissionFieldInsertGQLModel
    ) -> typing.Union[DigitalSubmissionFieldGQLModel, InsertError[DigitalSubmissionFieldGQLModel]]:
        return await digital_submission_field_insert_internal(self, info=info, submission_field=submission_field)
    
    @strawberry.mutation(
        description="""Update a DigitalSubmissionField""",
        permission_classes=[
            SimpleUpdatePermission[DigitalSubmissionFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_submission_field_update(
        self,
        info: strawberry.types.Info,
        submission_field: DigitalSubmissionFieldUpdateGQLModel
    ) -> typing.Union[DigitalSubmissionFieldGQLModel, UpdateError[DigitalSubmissionFieldGQLModel]]:
        return await Update[DigitalSubmissionFieldGQLModel].DoItSafeWay(info=info, entity=submission_field)
    
    @strawberry.mutation(
        description="""Delete a DigitalSubmissionField""",
        permission_classes=[
            SimpleDeletePermission[DigitalSubmissionFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_submission_field_delete(
        self,
        info: strawberry.types.Info,
        submission_field: DigitalSubmissionFieldDeleteGQLModel
    ) -> typing.Optional[DeleteError[DigitalSubmissionFieldGQLModel]]:
        return await Delete[DigitalSubmissionFieldGQLModel].DoItSafeWay(info=info, entity=submission_field)