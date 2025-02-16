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

DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy(".DigitalFormGQLModel")]
DigitalFormFieldGQLModel = typing.Annotated["DigitalFormFieldGQLModel", strawberry.lazy(".DigitalFormFieldGQLModel")]
DigitalFormFieldInputFilter = typing.Annotated["DigitalFormFieldInputFilter", strawberry.lazy(".DigitalFormFieldGQLModel")]

@createInputs
@dataclasses.dataclass
class DigitalFormSectionInputFilter:
    id: IDType
    label: str
    name: str
    label_en: str
    description: str
    parent_id: IDType

@strawberry.federation.type(description="""Represents a section (group) of a digital form.
Supports nested sections and repetition.""")
class DigitalFormSectionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormSectionModel

    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Label for display""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""name for reference, must be unique and must start with a capitalized letter""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    label_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Label for display in english""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Explanation of the form section""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Digital document form section parent id which this section belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    # parent: typing.Optional["DigitalFormSectionGQLModel"] = strawberry.field(
    #     description="""Digital document form section parent which this section belongs to""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=ScalarResolver["DigitalFormSectionGQLModel"](fkey_field_name="parent_id")
    # )

    @strawberry.field(
        description=""""form section or document """,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def parent(self, info: strawberry.types.Info) -> typing.Union["DigitalFormSectionGQLModel", DigitalFormGQLModel]:
        from .DigitalFormGQLModel import DigitalFormGQLModel

        futures = [DigitalFormGQLModel.load_with_loader(self.parent_id), DigitalFormSectionGQLModel.load_with_loader(self.parent_id)]
        [document, section] = await asyncio.gather(*futures)
        return document or section
    

    sections: typing.List["DigitalFormSectionGQLModel"] = strawberry.field(
        description="""Digital document form section children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormSectionGQLModel"](fkey_field_name="parent_id", whereType=DigitalFormSectionInputFilter)
    )

    fields: typing.List["DigitalFormFieldGQLModel"] = strawberry.field(
        description="""Digital document form section fields""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalFormFieldGQLModel"](fkey_field_name="form_section_id", whereType=DigitalFormFieldInputFilter)
    )

    order: int = strawberry.field(
        description="""Order of the section""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repatable_min: int = strawberry.field(
        description="""Minimum number of repetitions""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repatable_max: int = strawberry.field(
        description="""Maximum number of repetitions""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    repeatable: bool = strawberry.field(
        description="""Is section repeatable""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )