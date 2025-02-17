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


@strawberry.interface(
    description=""""""
)
class DigitalFormSubmissionQuery:
    digital_form_submission_by_id: typing.Optional[DigitalFormSubmissionGQLModel] = strawberry.field(
        description="""Get a DigitalFormSubmission by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalFormSubmissionGQLModel.load_with_loader
    )

    digital_form_submission_page: typing.List[DigitalFormSubmissionGQLModel] = strawberry.field(
        description="""Get a page of DigitalFormSubmissions""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalFormSubmissionInputFilter](whereType=DigitalFormSubmissionInputFilter)
    )

    
@strawberry.input(
    description="""DigitalFormSubmission insert mutation"""
)
class DigitalFormSubmissionInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSubmission eng name""",
        default=None
    )
    parent_id: IDType = strawberry.field(
        description="""DigitalFormSubmission master id"""
    )
    id: IDType = strawberry.field(
        description="""DigitalFormSubmission id client generated"""
    )

@strawberry.input(
    description="""DigitalFormSubmission update mutation"""
)
class DigitalFormSubmissionUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalFormSubmission id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalFormSubmission lastchange"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalFormSubmission eng name""",
        default=None
    )

@strawberry.input(
    description="""DigitalFormSubmission delete mutation"""
)
class DigitalFormSubmissionDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalFormSubmission id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalFormSubmission lastchange"""
    )


@strawberry.type(
    description="""DigitalFormSubmission mutation"""
)
class DigitalFormSubmissionMutation:
    @strawberry.mutation(
        description="""Insert a DigitalFormSubmission""",
        permission_classes=[
            SimpleInsertPermission[DigitalFormSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_insert(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalFormSubmissionInsertGQLModel
    ) -> typing.Union[DigitalFormSubmissionGQLModel, InsertError[DigitalFormSubmissionGQLModel]]:
        return await Insert[DigitalFormSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    
    @strawberry.mutation(
        description="""Update a DigitalFormSubmission""",
        permission_classes=[
            SimpleUpdatePermission[DigitalFormSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_update(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalFormSubmissionUpdateGQLModel
    ) -> typing.Union[DigitalFormSubmissionGQLModel, UpdateError[DigitalFormSubmissionGQLModel]]:
        return await Update[DigitalFormSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    
    @strawberry.mutation(
        description="""Delete a DigitalFormSubmission""",
        permission_classes=[
            SimpleDeletePermission[DigitalFormSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_delete(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalFormSubmissionDeleteGQLModel
    ) -> typing.Optional[DeleteError[DigitalFormSubmissionGQLModel]]:
        return await Delete[DigitalFormSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)    