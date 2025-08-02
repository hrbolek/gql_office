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

DigitalSubmissionInputFilter_ = typing.Annotated["DigitalSubmissionInputFilter", strawberry.lazy(".DigitalSubmissionGQLModel")]
@createInputs
@dataclasses.dataclass
class DigitalSubmissionFieldInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    state_id: IDType
    field_id: IDType
    section_id: IDType
    submission_id: IDType

    from .DigitalFormFieldGQLModel import DigitalFormFieldInputFilter
    form_field: DigitalFormFieldInputFilter
    from .DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionInputFilter
    submission_section: DigitalSubmissionSectionInputFilter
    # from .DigitalSubmissionGQLModel import DigitalSubmissionInputFilter
    # # submission: DigitalSubmissionInputFilter_
    # submission: DigitalSubmissionInputFilter



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

    submission_id: typing.Optional[IDType] = strawberry.field(
        description="""Submission id for this field""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    section_id: typing.Optional[IDType] = strawberry.field(
        description="""Digital Submission Section id which is this field is associated to""",
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
        description="""Digital Submission Section which is this field is associated to""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="section_id")
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""State id of this field""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state: typing.Optional['StateGQLModel'] = strawberry.field(
        description="""State of this field""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StateGQLModel"](fkey_field_name="state_id")
    )

@strawberry.federation.type(description="")
class SubmissionFieldQuery:

    digital_submission_field_by_id: typing.Optional[DigitalSubmissionFieldGQLModel] = strawberry.field(
        description="Submission field by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalSubmissionFieldGQLModel.load_with_loader
    )

    digital_submission_field_page: typing.List[DigitalSubmissionFieldGQLModel] = strawberry.field(
        description="return list of Submission fields",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalSubmissionFieldGQLModel](whereType=DigitalSubmissionFieldInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin, TreeInputStructureMixin

@strawberry.input(description="DigitalFormField insert parameter description")
class DigitalSubmissionFieldInsertGQLModel(InputModelMixin):
    getLoader = DigitalSubmissionFieldGQLModel.getLoader
    field_id: typing.Optional[IDType] = strawberry.field(
        description="link to the form field",
        default=None
        )
    section_id: typing.Optional[IDType] = strawberry.field(
        description="section id where the field is placed",
        default=None
        )
    submission_id: typing.Optional[IDType] = strawberry.field(
        description="submission id where the field is placed",
        default=None
        )
    id: typing.Optional[IDType] = strawberry.field(
        description="client side generated id", 
        default=None
        )
    value: typing.Optional[str] = strawberry.field(
        description="value of the field", 
        default=None
        )
    state_id: typing.Optional[IDType] = strawberry.field(
        description="client side generated id", 
        default=None
        )
    value: typing.Optional[str] = strawberry.field(
        description="field value", 
        default=None
        )
    path: strawberry.Private[str] = None
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None
    
@strawberry.input(description="DigitalSubmissionField update parameter description")
class DigitalSubmissionFieldUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    value: typing.Optional[str] = strawberry.field(description="value of the field", default=None)
    type_id: typing.Optional[IDType] = strawberry.field(description="type id of the field", default=None)
    
@strawberry.input(description="DigitalSubmissionField insert parameter description")
class DigitalSubmissionFieldDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

# def field_into_dbmodel(self, info: strawberry.types.Info, submission_field: DigitalSubmissionFieldInsertGQLModel):
#     loader = DigitalSubmissionFieldGQLModel.getLoader(info)
#     Model = loader.getModel()
#     submission_field_dict = strawberry.asdict(submission_field)
#     result = Model(**submission_field_dict)
#     return result


# async def digital_submission_field_insert_internal(self, info: strawberry.types.Info, submission_field: DigitalSubmissionFieldInsertGQLModel):
#     return await Insert[DigitalSubmissionFieldGQLModel].DoItSafeWay(info=info, entity=submission_field)

@strawberry.interface(
    description="Digital submission mutations"
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
        submission_field: typing.Annotated[DigitalSubmissionFieldInsertGQLModel, strawberry.argument(description="submission field attributes, to be inserted")]
    ) -> typing.Union[DigitalSubmissionFieldGQLModel, InsertError[DigitalSubmissionFieldGQLModel]]:
        return await Insert[DigitalSubmissionFieldGQLModel].DoItSafeWay(info=info, entity=submission_field)
    
    @strawberry.mutation(
        description="""Update a DigitalSubmissionField""",
        permission_classes=[
            SimpleUpdatePermission[DigitalSubmissionFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_submission_field_update(
        self,
        info: strawberry.types.Info,
        submission_field: typing.Annotated[DigitalSubmissionFieldInsertGQLModel, strawberry.argument(description="submission field attributes, to be updated")]
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
        submission_field: typing.Annotated[DigitalSubmissionFieldDeleteGQLModel, strawberry.argument(description="id and lastchange of submission field, to be deleted")]
    ) -> typing.Optional[DeleteError[DigitalSubmissionFieldGQLModel]]:
        return await Delete[DigitalSubmissionFieldGQLModel].DoItSafeWay(info=info, entity=submission_field)