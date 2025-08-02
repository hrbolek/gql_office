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
    
    StrFilter,
    UuidFilter,
    IntFilter,

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

DigitalSubmissionFieldInsertGQLModel = typing.Annotated["DigitalSubmissionFieldInsertGQLModel", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]

DigitalSubmissionInputFilter = typing.Annotated["DigitalSubmissionInputFilter", strawberry.lazy(".DigitalSubmissionGQLModel")]
DigitalSubmissionFieldInputFilter = typing.Annotated["DigitalSubmissionFieldInputFilter", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
DigitalFormSectionInputFilter = typing.Annotated["DigitalFormSectionInputFilter", strawberry.lazy(".DigitalFormSectionGQLModel")]


DigitalSubmissionSectionInputFilter_ = typing.Annotated["DigitalSubmissionSectionInputFilter", strawberry.lazy(".DigitalSubmissionSectionGQLModel")]
# @strawberry.input(description="filter for submission section")
# class DigitalSubmissionSectionInputFilter:
#     # name: str
#     # name_en: str
#     index: typing.Optional[IntFilter] = strawberry.field(description="filter by index = order of section", default=None)
#     id: typing.Optional[UuidFilter] = strawberry.field(description="filter by submission section id", default=None)
#     section_id: typing.Optional[UuidFilter] = strawberry.field(description="filter by parent submission section id", default=None)
#     submission_id: typing.Optional[UuidFilter] = strawberry.field(description="filter by submission id", default=None)

#     child_sections: typing.Optional["DigitalSubmissionSectionInputFilter"] = strawberry.field(description="filter by sections contained by this section", default=None)
#     section: typing.Optional["DigitalSubmissionSectionInputFilter"] = strawberry.field(description="filter by section which owns this section", default=None)
#     submission: typing.Optional[DigitalSubmissionInputFilter] = strawberry.field(description="filter by sections contained by this section", default=None)
#     fields: typing.Optional[DigitalSubmissionFieldInputFilter] = strawberry.field(description="filter by submission fields contained by this section", default=None)
#     form_section: typing.Optional[DigitalFormSectionInputFilter] = strawberry.field(description="filter by form section linked to this section", default=None)

@createInputs
@dataclasses.dataclass
class DigitalSubmissionSectionInputFilter:
    # name: str
    # name_en: str
    index: IntFilter # = strawberry.field(description="filter by index = order of section", default=None)
    id: UuidFilter # = strawberry.field(description="filter by submission section id", default=None)
    section_id: UuidFilter # = strawberry.field(description="filter by parent submission section id", default=None)
    submission_id: UuidFilter # = strawberry.field(description="filter by submission id", default=None)

    child_sections: DigitalSubmissionSectionInputFilter_ # = strawberry.field(description="filter by sections contained by this section", default=None)
    section: DigitalSubmissionSectionInputFilter_ # = strawberry.field(description="filter by section which owns this section", default=None)
    submission: DigitalSubmissionInputFilter # = strawberry.field(description="filter by sections contained by this section", default=None)
    fieldX: DigitalSubmissionFieldInputFilter # = strawberry.field(description="filter by submission fields contained by this section", default=None)
    form_section: DigitalFormSectionInputFilter # = strawberry.field(description="filter by form section linked to this section", default=None)


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

    state_id: typing.Optional[IDType] = strawberry.field(
        description="state of the submission,",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    section_id: typing.Optional[IDType] = strawberry.field(
        description="""Submission section parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_section_id: typing.Optional[IDType] = strawberry.field(
        description="""id of section from form""",
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

    form_section: typing.Optional[DigitalFormSectionGQLModel] = strawberry.field(
        description="the meta info",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[DigitalFormSectionGQLModel](fkey_field_name="form_section_id")
    )

    submission: typing.Optional["DigitalSubmissionGQLModel"] = strawberry.field(
        description="""Submission, represents a full dataset which this section is member""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionGQLModel"](fkey_field_name="submission_id")
    )

    # fieldX: typing.Optional['DigitalSubmissionFieldGQLModel'] = strawberry.field(
    #     description="""Digital submission field associated with this section""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=ScalarResolver["DigitalSubmissionFieldGQLModel"](fkey_field_name="section_id")
    # )

    sections: typing.List["DigitalSubmissionSectionGQLModel"] = strawberry.field(
        description="""Submission sections inside this section""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="section_id", whereType=DigitalSubmissionSectionInputFilter)
    )

    fields: typing.List["DigitalSubmissionFieldGQLModel"] = strawberry.field(
        description="""Fields inside this section""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionFieldGQLModel"](fkey_field_name="section_id", whereType=DigitalSubmissionFieldInputFilter)
    )




@strawberry.federation.type(description="")
class SubmissionSectionQuery:

    digital_submission_section_by_id: typing.Optional[DigitalSubmissionSectionGQLModel] = strawberry.field(
        description="Submission section by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalSubmissionSectionGQLModel.load_with_loader
    )

    digital_submission_section_page: typing.List[DigitalSubmissionSectionGQLModel] = strawberry.field(
        description="return list of Submission sections",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalSubmissionSectionGQLModel](whereType=DigitalSubmissionSectionInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin, TreeInputStructureMixin

@strawberry.input(description="Input definition for SubmissionSection create")
class SubmissionSectionInsertGQLModel(InputModelMixin):
    getLoader = DigitalSubmissionSectionGQLModel.getLoader
    submission_id: typing.Optional[IDType] = strawberry.field(
        description="id of sumbission where new section is being created, regardless of deep",
        default=None
        )
    form_section_id: typing.Optional[IDType] = strawberry.field(
        description="section of the form",
        default=None
        )
    # name: str = strawberry.field(description="name of the section, must start with Capitalized letter")
    # name_en: typing.Optional[str] = strawberry.field(description="eng name of the type", default=None)
    # parent_id: typing.Optional[IDType] = strawberry.field(description="for which type this type belongs", default=None)
    index: typing.Optional[int] = strawberry.field(
        description="if there are more sections, this is index", 
        default=None
        )
    id: typing.Optional[IDType] = strawberry.field(
        description="client generated primary key", 
        default=None
        )
    
    sections: typing.Optional[typing.List["SubmissionSectionInsertGQLModel"]] = strawberry.field(
        description="Optional list of sub sections", 
        default_factory=list
    )

    # from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
    fields: typing.Optional[typing.List["DigitalSubmissionFieldInsertGQLModel"]] = strawberry.field(
        description="Optional list of fields", 
        default_factory=list
    )

    path: strawberry.Private[str] = None
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(description="Input definition for SubmissionSection update")
class SubmissionSectionUpdateGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    # name: typing.Optional[str] = strawberry.field(description="name of the section, must start with Capitalized lettere", default=None)
    # name_en: typing.Optional[str] = strawberry.field(description="eng name ", default=None)
    index: typing.Optional[int] = strawberry.field(description="index for repeatable sections", default=None)

    name: strawberry.Private[str] = None
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(description="Input definition for SubmissionSection delete")
class SubmissionSectionDeleteGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

# from .DigitalSubmissionFieldGQLModel import field_into_dbmodel
# import logging
# def section_into_dbmodel(self, info: strawberry.types.Info, submission_section: SubmissionSectionInsertGQLModel):
#     sectionLoader = DigitalSubmissionSectionGQLModel.getLoader(info=info)
#     sectionDbModel = sectionLoader.getModel()
#     sections = [section_into_dbmodel(self, info, section) for section in submission_section.child_sections]
#     fields = [field_into_dbmodel(self, info, field) for field in submission_section.fields]
   
#     submission_section_dict = strawberry.asdict(submission_section)
#     del submission_section_dict["child_sections"]
#     del submission_section_dict["fields"]
#     # print("section_into_dbmodel", submission_section_dict, flush=True)
#     # result = sectionDbModel(**strawberry.asdict(submission_section))
#     result = sectionDbModel(**submission_section_dict)
#     result.child_sections.extend(sections)
#     result.fields.extend(fields)
#     print("section_into_dbmodel", result, flush=True)
#     print("section_into_dbmodel", strawberry.asdict(result), flush=True)
#     logging.info(f"result.child_sections = {result.child_sections}")
#     logging.info(f"result.fields = {result.fields}")
#     # assert False
#     # result.child_sections = sections
#     # result.fields = fields
#     return result

# async def submission_section_insert_iternal(self, info: strawberry.types.Info, submission_section: SubmissionSectionInsertGQLModel) -> typing.Union[DigitalSubmissionSectionGQLModel, InsertError[DigitalSubmissionSectionGQLModel]]:
#     modelinstance = submission_section.intoModel(info=info)
#     # model = section_into_dbmodel(submission_section)
#     return await Insert[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=modelinstance)

#     # from .DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
#     # from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel
#     # subLoader = DigitalSubmissionGQLModel.getLoader(info=info)
#     # secLoader = DigitalSubmissionSectionGQLModel.getLoader(info=info)
#     # fsecLoader = DigitalFormSectionGQLModel.getLoader(info=info)

#     # if submission_section.parent_id:
#     #     futures = (
#     #         fsecLoader.load(submission_section.form_section_id),
#     #         secLoader.filter_by(id=submission_section.parent_id),
#     #         secLoader.load(submission_section.parent_id)
#     #     )
#     #     [form_section, neibs, parent] = await asyncio.gather(*futures)

#     #     if (form_section.repatable_min < form_section.repatable_max):
#     #         # repeatable, index is mandatory
#     #         indexes = (neib.index for neib in neibs)
#     #         if len(indexes) + 1 >= form_section.repeatable_max:
#     #             return InsertError(msg="too much sections", _input=submission_section)
#     #         if submission_section.index in indexes:
#     #             return InsertError(msg="index already used", _input=submission_section)
#     #         if submission_section.index is None:
#     #             submission_section.index = max(indexes) + 1
#     #         if submission_section.index < 0:
#     #             return InsertError(msg="index has bad value", _input=submission_section)
#     #         submission_section.path = f"{parent.path}.{submission_section.index}"
#     #     else:
#     #         submission_section.path = f"{parent.path}.{form_section.name}"
#     #     if parent is None:
#     #         return InsertError(msg="parent does not exists", _input=submission_section)
        
#     # else:
#     #     futures = (
#     #         fsecLoader.load(submission_section.form_section_id),
#     #         secLoader.filter_by(form_section_id=submission_section.form_section_id)
#     #     )
#     #     [form_section, neibs] = await asyncio.gather(*futures)
#     #     pass
#     # futures = (subLoader.load(submission_section.submission_id), secLoader.load(submission_section.parent_id))
#     # result = await Insert[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=submission_section)
#     result = await Insert[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=model)
#     return result


@strawberry.interface(description="Submission secion mutations")
class SubmissionSectionMutation:

    @strawberry.mutation(
        description="standard insert operation",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[DigitalSubmissionSectionGQLModel](roles=["administrátor"])
        ]
    )
    async def submission_section_insert(self, info: strawberry.types.Info, submission_section: SubmissionSectionInsertGQLModel) -> typing.Union[DigitalSubmissionSectionGQLModel, InsertError[DigitalSubmissionSectionGQLModel]]:
        # from .DigitalSubmissionGQLModel import DigitalSubmissionGQLModel
        # from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel
        # subLoader = DigitalSubmissionGQLModel.getLoader(info=info)
        # secLoader = DigitalSubmissionSectionGQLModel.getLoader(info=info)
        # fsecLoader = DigitalFormSectionGQLModel.getLoader(info=info)

        # if submission_section.parent_id:
        #     futures = (
        #         fsecLoader.load(submission_section.form_section_id),
        #         secLoader.filter_by(id=submission_section.parent_id),
        #         secLoader.load(submission_section.parent_id)
        #     )
        #     [form_section, neibs, parent] = await asyncio.gather(*futures)

        #     if (form_section.repatable_min < form_section.repatable_max):
        #         # repeatable, index is mandatory
        #         indexes = (neib.index for neib in neibs)
        #         if len(indexes) + 1 >= form_section.repeatable_max:
        #             return InsertError(msg="too much sections", _input=submission_section)
        #         if submission_section.index in indexes:
        #             return InsertError(msg="index already used", _input=submission_section)
        #         if submission_section.index is None:
        #             submission_section.index = max(indexes) + 1
        #         if submission_section.index < 0:
        #             return InsertError(msg="index has bad value", _input=submission_section)
        #         submission_section.path = f"{parent.path}.{submission_section.index}"
        #     else:
        #         submission_section.path = f"{parent.path}.{form_section.name}"
        #     if parent is None:
        #         return InsertError(msg="parent does not exists", _input=submission_section)
            
        # else:
        #     futures = (
        #         fsecLoader.load(submission_section.form_section_id),
        #         secLoader.filter_by(form_section_id=submission_section.form_section_id)
        #     )
        #     [form_section, neibs] = await asyncio.gather(*futures)
        #     pass
        futures = (subLoader.load(submission_section.submission_id), secLoader.load(submission_section.parent_id))
        modelinstance = submission_section.intoModel(info=info)
        result = await Insert[DigitalSubmissionSectionGQLModel].DoItSafeWay(info=info, entity=modelinstance)
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