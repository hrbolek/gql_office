import uuid
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
from ..DocumentInterfaceGQLModel import DocumentInterfaceGQLModel

DigitalSubmissionFieldGQLModel = typing.Annotated["DigitalSubmissionFieldGQLModel", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
DigitalSubmissionFieldInputFilter = typing.Annotated["DigitalSubmissionFieldInputFilter", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
DigitalSubmissionSectionGQLModel = typing.Annotated["DigitalSubmissionSectionGQLModel", strawberry.lazy(".DigitalSubmissionSectionGQLModel")]
DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy(".DigitalFormGQLModel")]

DigitalSubmissionFieldInputFilter = typing.Annotated["DigitalSubmissionFieldInputFilter", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
@createInputs
@dataclasses.dataclass
class DigitalSubmissionInputFilter:
    name: str
    name_en: str
    # description: str
    id: IDType
    parent_id: IDType

    # parent: "DigitalSubmissionInputFilter"
    # from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInputFilter
    submitted_fields: DigitalSubmissionFieldInputFilter
    from .DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionInputFilter
    submitted_sections: DigitalSubmissionSectionInputFilter
    from .DigitalFormGQLModel import DigitalFormInputFilter
    form: DigitalFormInputFilter


@strawberry.federation.type(
    keys=["id"], description="""Represents a submission of a digital form filled out by a user.
Aggregates responses for all the fields defined in the form."""
)
class DigitalSubmissionGQLModel(BaseGQLModel): #, DocumentInterfaceGQLModel
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalSubmissionModel
    
    name: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="state of the submission,",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    form_id: typing.Optional[IDType] = strawberry.field(
        description="Form which is associated to this submission.",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        description="This is id of submission which owns this submission (recursive tree). Submission can contain submissions.",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )    

    # section_id: typing.Optional[IDType] = strawberry.field(
    #     description="this is id of section which owns this section (recursive tree)",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     default=None
    # )    

    form: typing.Optional[DigitalFormGQLModel] = strawberry.field(
        description="form which is associated to this submission",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[DigitalFormGQLModel](fkey_field_name="form_id")
    )

    parent: typing.Optional["DigitalSubmissionGQLModel"] = strawberry.field(
        description="This is submission which owns this submission (recursive tree). Submission can contain submissions. It is like a folder",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionGQLModel"](fkey_field_name="parent_id")
    )

    @strawberry.field(
        description="all sumbitted sections on all levels, thanks to materialized path",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def submitted_sections_all(self, info: strawberry.types.Info) -> typing.List[DigitalSubmissionSectionGQLModel]:
        return []

    submitted_sections: typing.List["DigitalSubmissionSectionGQLModel"] = strawberry.field(
        description="""Digital Submission sections.""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="submission_id", whereType=DigitalSubmissionFieldInputFilter)
    )

    # @strawberry.field(
    #     description="""Digital Submission sections.""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    # )
    # async def submitted_sections(self, info: strawberry.types.Info) -> typing.List["DigitalSubmissionSectionGQLModel"]:
    #     from .DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionGQLModel
    #     loader = DigitalSubmissionSectionGQLModel.getLoader(info)
    #     rows = await loader.filter_by(submission_id=self.id)
    #     # for row in rows:
    #     #     print("submitted_sections", dir(row), flush=True)
    #     #     print("submitted_sections", strawberry.asdict(row), flush=True)
    #     # assert False
    #     result = [DigitalSubmissionSectionGQLModel.from_dataclass(row) for row in rows]
    #     return result

    submitted_fields: typing.List["DigitalSubmissionFieldGQLModel"] = strawberry.field(
        description="""Digital Submission fields.""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionFieldGQLModel"](fkey_field_name="submission_id", whereType=DigitalSubmissionFieldInputFilter)
    )


@strawberry.interface(
    description=""""""
)
class DigitalSubmissionQuery:
    digital_form_submission_by_id: typing.Optional[DigitalSubmissionGQLModel] = strawberry.field(
        description="""Get a DigitalSubmission by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalSubmissionGQLModel.load_with_loader
    )

    digital_form_submission_page: typing.List[DigitalSubmissionGQLModel] = strawberry.field(
        description="""Get a page of DigitalSubmissions""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalSubmissionInputFilter](whereType=DigitalSubmissionInputFilter)
    )

    
@strawberry.input(
    description="""DigitalSubmission insert mutation"""
)
class DigitalSubmissionInsertGQLModel:
    form_id: IDType = strawberry.field(
        description="[form](#digitalformgqlmodel) for this submission"
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission eng name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission master id""",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission id client generated""",
        default=None
    )

    from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel

    sections: typing.Optional[typing.List[SubmissionSectionInsertGQLModel]] = strawberry.field(
        description="", 
        # default_factory=list,
        default=None
    )

@strawberry.input(
    description="""DigitalSubmission update mutation"""
)
class DigitalSubmissionUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalSubmission id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalSubmission lastchange"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission eng name""",
        default=None
    )

@strawberry.input(
    description="""DigitalSubmission delete mutation"""
)
class DigitalSubmissionDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalSubmission id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalSubmission lastchange"""
    )

from .DigitalSubmissionSectionGQLModel import section_into_dbmodel
import logging
async def digital_form_submission_insert_internal(
    self,
    info: strawberry.types.Info,
    digital_form_submission: DigitalSubmissionInsertGQLModel
) -> typing.Union[DigitalSubmissionGQLModel, InsertError[DigitalSubmissionGQLModel]]:

    loader = DigitalSubmissionGQLModel.getLoader(info=info)
    DBModel = loader.getModel()
    # digital_form_submission.id = digital_form_submission.id if digital_form_submission.id is not None else uuid.uuid4()
    # for section in (digital_form_submission.sections or []):
    #     section.submission_id = digital_form_submission.id

    sections = [section_into_dbmodel(self, info, section) for section in (digital_form_submission.sections or [])]
    digital_form_submission_as_dict = strawberry.asdict(digital_form_submission)
    del digital_form_submission_as_dict["sections"]
    model = DBModel(**digital_form_submission_as_dict)
    model.submitted_sections.extend(sections)

    return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=model)


@strawberry.type(
    description="""DigitalSubmission mutation"""
)
class DigitalSubmissionMutation:
    @strawberry.mutation(
        description="""Insert a DigitalSubmission""",
        permission_classes=[
            SimpleInsertPermission[DigitalSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_insert(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionInsertGQLModel
    ) -> typing.Union[DigitalSubmissionGQLModel, InsertError[DigitalSubmissionGQLModel]]:
        return await digital_form_submission_insert_internal(self, info, digital_form_submission)
        # return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    
    @strawberry.mutation(
        description="""Update a DigitalSubmission""",
        permission_classes=[
            SimpleUpdatePermission[DigitalSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_update(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionUpdateGQLModel
    ) -> typing.Union[DigitalSubmissionGQLModel, UpdateError[DigitalSubmissionGQLModel]]:
        return await Update[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    
    @strawberry.mutation(
        description="""Delete a DigitalSubmission""",
        permission_classes=[
            SimpleDeletePermission[DigitalSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_delete(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionDeleteGQLModel
    ) -> typing.Optional[DeleteError[DigitalSubmissionGQLModel]]:
        return await Delete[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)    