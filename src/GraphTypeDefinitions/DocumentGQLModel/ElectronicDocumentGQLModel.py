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

DocumentTypeGQLModel = typing.Annotated["DocumentTypeGQLModel", strawberry.lazy(".DocumentTypeGQLModel")]

@createInputs
@dataclasses.dataclass
class ElectronicDocumentInputFilter:
    name: str
    name_en: str
    description: str
    mimetype: str
    parent_id: IDType


@strawberry.federation.type(
    description="""Represents a digital form used to capture user input.
Defines the overall structure of the form and stores its submissions."""
)
class ElectronicDocumentGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ElectronicDocumentModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""The title of the digital form.""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""The eng title of the digital form.""",
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

    content: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document content""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    
    mimetype: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document mimetype""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Document parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["ElectronicDocumentGQLModel"] = strawberry.field(
        description="""Document parent""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ElectronicDocumentGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["ElectronicDocumentGQLModel"] = strawberry.field(
        description="""Document children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["ElectronicDocumentGQLModel"](fkey_field_name="parent_id", whereType=ElectronicDocumentInputFilter)
    )

    type_id: typing.Optional[IDType] = strawberry.field(
        description="""Document type id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type: typing.Optional["DocumentTypeGQLModel"] = strawberry.field(
        name="type",
        description="""Document type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentTypeGQLModel"](fkey_field_name="type_id")
    )


@strawberry.interface(
    description="""Queries for Document"""
)
class DocumentQuery:
    document_by_id: typing.Optional[ElectronicDocumentGQLModel] = strawberry.field(
        description="""Get a Document by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ElectronicDocumentGQLModel.load_with_loader
    )

    document_page: typing.List[ElectronicDocumentGQLModel] = strawberry.field(
        description="""Get a page of Documents""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[ElectronicDocumentGQLModel](whereType=ElectronicDocumentInputFilter)
    )

@strawberry.input(
    description="""Document insert mutation"""
)
class ElectronicDocumentInsertGQLModel:
    id: typing.Optional[IDType] = strawberry.field(
        description="""Document id""",
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Document name""",
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Document eng name""",
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Document description""",
    )
    content: typing.Optional[str] = strawberry.field(
        description="""Document content""",
    )
    mimetype: typing.Optional[str] = strawberry.field(
        description="""Document mimetype""",
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Document parent id""",
    )
    group_id: typing.Optional[IDType] = strawberry.field(
        description="""Document group id""",
    )

@strawberry.input(
    description="""Document update mutation"""
)
class ElectronicDocumentUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Document id""",
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Document name""",
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Document eng name""",
    )
    description: typing.Optional[str] = strawberry.field(
        description="""Document description""",
    )
    content: typing.Optional[str] = strawberry.field(
        description="""Document content""",
    )
    mimetype: typing.Optional[str] = strawberry.field(
        description="""Document mimetype""",
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Document parent id""",
    )
    group_id: typing.Optional[IDType] = strawberry.field(
        description="""Document group id""",
    )


@strawberry.input(
    description="""Document delete mutation"""
)
class ElectronicDocumentDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Document id""",
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Document mutations"""
)
class DocumentMutation:
    @strawberry.mutation(
        description="""Insert a Document""",
        permission_classes=[
            SimpleInsertPermission[ElectronicDocumentGQLModel](roles=["administrátor"])
        ]
    )
    async def document_insert(
        document: ElectronicDocumentInsertGQLModel
    ) -> typing.Union[ElectronicDocumentGQLModel, InsertError]:
        return await Insert[ElectronicDocumentGQLModel].DoItSafeWay(document)

    @strawberry.mutation(
        description="""Update a Document""",
        permission_classes=[
            SimpleUpdatePermission[ElectronicDocumentGQLModel](roles=["administrátor"])
        ]
    )
    async def document_update(
        document: ElectronicDocumentUpdateGQLModel
    ) -> typing.Union[ElectronicDocumentGQLModel, UpdateError[ElectronicDocumentGQLModel]]:
        return await Update[ElectronicDocumentGQLModel].DoItSafeWay(document)

    @strawberry.mutation(
        description="""Delete a Document""",
        permission_classes=[
            SimpleDeletePermission[ElectronicDocumentGQLModel](roles=["administrátor"])
        ]
    )
    async def document_delete(
        document: ElectronicDocumentDeleteGQLModel
    ) -> typing.Optional[DeleteError[ElectronicDocumentGQLModel]]:
        return await Delete[ElectronicDocumentGQLModel].DoItSafeWay(document)
    
