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

from ..BaseGQLModel import BaseGQLModel, IDType

@strawberry.input(
    description="""Input type for filtering DocumentTypeGQLModel"""
)
@dataclasses.dataclass
class DocumentTypeInputFilter:
    name: str
    name_en: str
    id: IDType

@strawberry.federation.type(
    description="""Entity representing a Document"""
)
class DocumentTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DocumentTypeModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent document id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["DocumentTypeGQLModel"] = strawberry.field(
        description="""Parent document""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentTypeGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["DocumentTypeGQLModel"] = strawberry.field(
        description="""Children documents""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DocumentTypeGQLModel"](fkey_field_name="parent_id", whereType=DocumentTypeInputFilter)
    )