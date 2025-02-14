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


@createInputs
@dataclasses.dataclass
class DocumentInputFilter:
    name: str
    name_en: str
    description: str
    content: str
    mimetype: str
    parent_id: IDType


@strawberry.type(
    description="""Entity representing a Document"""
)
class DocumentGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DocumentModel

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

    parent: typing.Optional["DocumentGQLModel"] = strawberry.field(
        description="""Document parent""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["DocumentGQLModel"] = strawberry.field(
        description="""Document children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DocumentGQLModel"](fkey_field_name="parent_id", whereType=DocumentInputFilter)
    )

    group_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Document group id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    group: typing.Optional["DocumentGQLModel"] = strawberry.field(
        description="""Document group""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentGQLModel"](fkey_field_name="group_id")
    )


@strawberry.interface(
    description="""Queries for Document"""
)
class DocumentQueries:
    document_by_id: typing.Optional[DocumentGQLModel] = strawberry.field(
        description="""Get a Document by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DocumentGQLModel.load_with_loader
    )

    document_page: typing.List[DocumentGQLModel] = strawberry.field(
        description="""Get a page of Documents""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DocumentGQLModel](whereType=DocumentInputFilter)
    )

@strawberry.input(
    description="""Document insert mutation"""
)
class DocumentInsertGQLModel:
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
class DocumentUpdateGQLModel:
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
class DocumentDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Document id""",
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Document mutations"""
)
class DocumentMutations:
    @strawberry.mutation(
        description="""Insert a Document""",
        permission_classes=[
            SimpleInsertPermission
        ]
    )
    async def document_insert(
        document: DocumentInsertGQLModel
    ) -> typing.Union[DocumentGQLModel, InsertError]:
        return await Insert[DocumentGQLModel].DoItSafeWay(document)

    @strawberry.mutation(
        description="""Update a Document""",
        permission_classes=[
            SimpleUpdatePermission
        ]
    )
    async def document_update(
        document: DocumentUpdateGQLModel
    ) -> typing.Union[DocumentGQLModel, UpdateError[DocumentGQLModel]]:
        return await Update[DocumentGQLModel].DoItSafeWay(document)

    @strawberry.mutation(
        description="""Delete a Document""",
        permission_classes=[
            SimpleDeletePermission
        ]
    )
    async def document_delete(
        document: DocumentDeleteGQLModel
    ) -> typing.Optional[DeleteError[DocumentGQLModel]]:
        return await Delete[DocumentGQLModel].DoItSafeWay(document)
    
