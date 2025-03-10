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

StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("..StateGQLModel")]
DocumentTypeGQLModel = typing.Annotated["DocumentTypeGQLModel", strawberry.lazy(".DocumentTypeGQLModel")]

@createInputs
@dataclasses.dataclass
class DocumentInputFilter:
    name: str
    name_en: str
    id: IDType
    parent_id: IDType

@strawberry.interface(
    description="""Interface for a Document either a DigitalDocument or a PhysicalDocument"""
)
class DocumentInterfaceGQLModel:

    name: typing.Optional[str] = strawberry.field(
        description="""Document name""",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="""Document eng name""",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    description: typing.Optional[str] = strawberry.field(   
        description="""Document description""",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""State id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    state: typing.Optional["StateGQLModel"] = strawberry.field(
        description="""State""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StateGQLModel"](fkey_field_name="state_id")
    )

    parent_id: typing.Optional[IDType] = strawberry.field(  
        description="""id of the parent document""",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    type_id: typing.Optional[IDType] = strawberry.field(  
        description="""Type id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    type_: typing.Optional["DocumentTypeGQLModel"] = strawberry.field(
        name="type",
        description="""Type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentTypeGQLModel"](fkey_field_name="type_id")
    )          