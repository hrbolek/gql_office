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
DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy(".DigitalFormGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFormFieldInputFilter:
    name: str
    name_en: str
    description: str
    id: IDType
    parent_id: IDType


@strawberry.federation.type(
    keys=["id"], description="""Represents a field in a digital form.
Defines properties of an individual input, including support for computed values."""
)
class DigitalFormFieldGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormFieldModel

    name: typing.Optional[str] = strawberry.field(
        description="""name for reference, must be unique and must start with a lower letter""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    label: typing.Optional[str] = strawberry.field(
        description="""Digital Form Field label for display""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    label_en: typing.Optional[str] = strawberry.field(
        description="""Digital Form Field label for display in english""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        description="""Digital Form Field placeholder""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_section_id: typing.Optional[IDType] = strawberry.field(
        description="""Digital form section where this field belongs""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_section: typing.Optional["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital form section where this field belongs""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalFormSectionGQLModel"](fkey_field_name="form_section_id")
    )

    form_id: typing.Optional[IDType] = strawberry.field(
        description="""Digital form where this field belongs""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form: typing.Optional["DigitalFormGQLModel"] = strawberry.field(
        description="""Digital form where this field belongs""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalFormGQLModel"](fkey_field_name="form_id")
    )

    required: typing.Optional[bool] = strawberry.field(
        description="Indicates whether this field is mandatory.",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    order: typing.Optional[int] = strawberry.field(
        description="Order index to determine the field's position within its section.",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    computed: typing.Optional[int] = strawberry.field(
        description="""Indicates whether the field's value is computed automatically from other fields.
Probably alias for `formula is not None`""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    formula: typing.Optional[str] = strawberry.field(
        description="""A mathematical formula (as a string) for computing the field's value.
Example: "price * quantity" where "price" and "quantity" reference other fields.""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type_id: typing.Optional[IDType] = strawberry.field(
        description="""Specifies the type of input (e.g., "text", "number", "date", "boolean", "select").""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    backend_formula: typing.Optional[str] = strawberry.field(
        description="""Specifies the backend payload constant(s).""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    flatten_formula: typing.Optional[str] = strawberry.field(
        description="""Specifies the operation on incomming data.""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

@strawberry.type(
    description=""
)
class DigitalFormFieldQuery:
    form_field_by_id: typing.Optional[DigitalFormFieldGQLModel] = strawberry.field(
        description="finds a form field by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalFormFieldGQLModel.load_with_loader
    )

    form_field_page: typing.List[DigitalFormFieldGQLModel] = strawberry.field(
        description="finds form fields by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalFormFieldGQLModel](whereType=DigitalFormFieldInputFilter)
    )
    pass

@strawberry.input(description="DigitalFormField insert parameter description")
class DigitalFormFieldInsertGQLModel:
    type_id: IDType = strawberry.field(description="type id of the field")
    form_section_id: IDType = strawberry.field(description="section id where the field is placed")
    id: typing.Optional[IDType] = strawberry.field(description="client side generated id", default=None)
    
@strawberry.input(description="DigitalFormField insert parameter description")
class DigitalFormFieldUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    type_id: typing.Optional[IDType] = strawberry.field(description="type id of the field", default=None)
    
@strawberry.input(description="DigitalFormField insert parameter description")
class DigitalFormFieldDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


async def digital_form_field_insert_internal(self, info: strawberry.types.Info, form_field: DigitalFormFieldInsertGQLModel):
    return await Insert[DigitalFormFieldGQLModel].DoItSafeWay(info=info, entity=form_field)

@strawberry.type(
    description=""
)
class DigitalFormFieldMutation:
    @strawberry.mutation(
        description="""Insert a DigitalFormField""",
        permission_classes=[
            SimpleInsertPermission[DigitalFormFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_field_insert(
        self,
        info: strawberry.types.Info,
        form_field: DigitalFormFieldInsertGQLModel
    ) -> typing.Union[DigitalFormFieldGQLModel, InsertError[DigitalFormFieldGQLModel]]:
        return await digital_form_field_insert_internal(self, info=info, form_field=form_field)
    
    @strawberry.mutation(
        description="""Update a DigitalFormField""",
        permission_classes=[
            SimpleUpdatePermission[DigitalFormFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_field_update(
        self,
        info: strawberry.types.Info,
        form_field: DigitalFormFieldUpdateGQLModel
    ) -> typing.Union[DigitalFormFieldGQLModel, UpdateError[DigitalFormFieldGQLModel]]:
        return await Update[DigitalFormFieldGQLModel].DoItSafeWay(info=info, entity=form_field)
    
    @strawberry.mutation(
        description="""Delete a DigitalFormField""",
        permission_classes=[
            SimpleDeletePermission[DigitalFormFieldGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_field_delete(
        self,
        info: strawberry.types.Info,
        form_field: DigitalFormFieldDeleteGQLModel
    ) -> typing.Optional[DeleteError[DigitalFormFieldGQLModel]]:
        return await Delete[DigitalFormFieldGQLModel].DoItSafeWay(info=info, entity=form_field)