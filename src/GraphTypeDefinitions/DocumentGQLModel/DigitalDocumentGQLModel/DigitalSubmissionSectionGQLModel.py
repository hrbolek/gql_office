import asyncio
import dataclasses
import datetime
import typing
import strawberry

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

DigitalFormSectionGQLModel = typing.Annotated["DigitalFormSectionGQLModel", strawberry.lazy(".DigitalFormSectionGQLModel")]
DigitalSubmissionFieldGQLModel = typing.Annotated["DigitalSubmissionFieldGQLModel", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
DigitalSubmissionGQLModel = typing.Annotated["DigitalSubmissionGQLModel", strawberry.lazy(".DigitalSubmissionGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalSubmissionSectionInputFilter:
    name: str
    name_en: str
    id: IDType
    parent_id: IDType


@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Submission section"""
)
class DigitalSubmissionSectionGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalSubmissionSectionModel

    path: typing.Optional[str] = strawberry.field(
        description="aka materialized path",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    index: typing.Optional[int] = strawberry.field(
        description="index / order of section",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    section_id: typing.Optional[IDType] = strawberry.field(
        description="""Submission section parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    submission_id: typing.Optional[IDType] = strawberry.field(
        description="""Submission id, represents a full dataset which this section is member""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    section: typing.Optional["DigitalSubmissionSectionGQLModel"] = strawberry.field(
        description="""Submission section parent""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="section_id")
    )

    submission: typing.Optional["DigitalSubmissionGQLModel"] = strawberry.field(
        description="""Submission, represents a full dataset which this section is member""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionGQLModel"](fkey_field_name="submission_id")
    )

    # @strawberry.field(
    #     description="""Submission section parent""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ]
    # )
    # async def parent(self, info: strawberry.types.Info) -> typing.Union["DigitalSubmissionSectionGQLModel", DigitalSubmissionGQLModel]:
    #     from .DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
    #     loads = [DigitalSubmissionGQLModel.load_with_loader, DigitalSubmissionSectionGQLModel.load_with_loader]
    #     futures = [load(self.parent_id) for load in loads]
    #     [submission, section] = await asyncio.gather(*futures)
    #     return submission or section

    fields: typing.Optional['DigitalSubmissionFieldGQLModel'] = strawberry.field(
        description="""Digital Field""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionFieldGQLModel"](fkey_field_name="section_id")
    )

    sections: typing.List["DigitalSubmissionSectionGQLModel"] = strawberry.field(
        description="""Submission section children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="parent_id", whereType=DigitalSubmissionSectionInputFilter)
    )


@strawberry.federation.type(description="")
class SubmissionSectionQuery:

    submission_section_by_id: typing.Optional[DigitalSubmissionSectionGQLModel] = strawberry.field(
        description="Submission section by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalSubmissionSectionGQLModel.load_with_loader
    )

    submission_section_page: typing.List[DigitalSubmissionSectionGQLModel] = strawberry.field(
        description="return list of Submission sections",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalSubmissionSectionGQLModel](whereType=DigitalSubmissionSectionInputFilter)
    )

@strawberry.input(description="Input definition for SubmissionSection create")
class SubmissionSectionInsertGQLModel:
    submission_id: IDType = strawberry.field(description="id of sumbission where new section is being created, regardless of deep")
    index: int = strawberry.field(description="if there are more sections, this is index")
    form_section_id: IDType = strawberry.field(description="section of the form")
    # name: str = strawberry.field(description="name of the section, must start with Capitalized letter")
    # name_en: typing.Optional[str] = strawberry.field(description="eng name of the type", default=None)
    parent_id: typing.Optional[IDType] = strawberry.field(description="for which type this type belongs", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="client generated primary key", default=None)
    createdby_id: strawberry.Private[IDType]
    path: strawberry.Private[str]

@strawberry.input(description="Input definition for SubmissionSection update")
class SubmissionSectionUpdateGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the section, must start with Capitalized lettere", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="eng name ", default=None)
    changedby_id: strawberry.Private[IDType]

@strawberry.input(description="Input definition for SubmissionSection delete")
class SubmissionSectionDeleteGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

@strawberry.federation.type(description="")
class SubmissionSectionMutation:

    @strawberry.mutation(
        description="standard insert operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[DigitalSubmissionSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def submission_section_insert(self, info: strawberry.types.Info, submission_section: SubmissionSectionInsertGQLModel) -> typing.Union[DigitalSubmissionSectionGQLModel, InsertError[DigitalSubmissionSectionGQLModel]]:
        from .DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
        from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel
        subLoader = DigitalSubmissionGQLModel.getLoader(info=info)
        secLoader = DigitalSubmissionSectionGQLModel.getLoader(info=info)
        fsecLoader = DigitalFormSectionGQLModel.getLoader(info=info)

        if submission_section.parent_id:
            futures = (
                fsecLoader.load(submission_section.form_section_id),
                secLoader.filter_by(id=submission_section.parent_id),
                secLoader.load(submission_section.parent_id)
            )
            [form_section, neibs, parent] = await asyncio.gather(*futures)

            if (form_section.repatable_min < form_section.repatable_max):
                # repeatable, index is mandatory
                indexes = (neib.index for neib in neibs)
                if len(indexes) + 1 >= form_section.repeatable_max:
                    return InsertError(msg="too much sections", _input=submission_section)
                if submission_section.index in indexes:
                    return InsertError(msg="index already used", _input=submission_section)
                if submission_section.index is None:
                    submission_section.index = max(indexes) + 1
                if submission_section.index < 0:
                    return InsertError(msg="index has bad value", _input=submission_section)
                submission_section.path = f"{parent.path}.{submission_section.index}"
            else:
                submission_section.path = f"{parent.path}.{form_section.name}"
            if parent is None:
                return InsertError(msg="parent does not exists", _input=submission_section)
            
        else:
            futures = (
                fsecLoader.load(submission_section.form_section_id),
                secLoader.filter_by(form_section_id=submission_section.form_section_id)
            )
            [form_section, neibs] = await asyncio.gather(*futures)
            pass
        futures = (subLoader.load(submission_section.submission_id), secLoader.load(submission_section.parent_id))
        result = await Insert[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=submission_section)
        return result
    
    @strawberry.mutation(
        description="standard insert operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[DigitalSubmissionSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def submission_section_update(self, info: strawberry.types.Info, submission_section: SubmissionSectionUpdateGQLModel) -> typing.Union[DigitalSubmissionSectionGQLModel, UpdateError[DigitalSubmissionSectionGQLModel]]:
        result = await Update[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=submission_section)
        return result


    @strawberry.mutation(
        description="standard insert operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[DigitalSubmissionSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def submission_section_delete(self, info: strawberry.types.Info, submission_section: SubmissionSectionDeleteGQLModel) -> typing.Optional[DeleteError[DigitalSubmissionSectionGQLModel]]:
        result = await Delete[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=submission_section)
        return result        