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
class DocumentTypeInputFilter:
    name: str
    name_en: str
    id: IDType

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Document type"""
)
class DocumentTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DocumentTypeModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document type name""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document eng name """,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document type description""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent document type id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["DocumentTypeGQLModel"] = strawberry.field(
        description="""Parent document type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentTypeGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["DocumentTypeGQLModel"] = strawberry.field(
        description="""Children document types""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DocumentTypeGQLModel"](fkey_field_name="parent_id", whereType=DocumentTypeInputFilter)
    )

@strawberry.type(
    description="")
class DocumentTypeQuery:

    document_type_by_id: typing.Optional[DocumentTypeGQLModel] = strawberry.field(
        description="gets document type",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DocumentTypeGQLModel.load_with_loader
    )

    document_type_page: typing.List[DocumentTypeGQLModel] = strawberry.field(
        description="gets list of document types filtered",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DocumentTypeGQLModel](whereType=DocumentTypeInputFilter)
    )
    
    
@strawberry.input(
    description="""DocumentType insert mutation"""
)
class DocumentTypeInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="""DocumentType name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DocumentType eng name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""DocumentType master id""",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""client generated id""",
        default=None
    )

@strawberry.input(
    description="""DocumentType update mutation"""
)
class DocumentTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""primary key""",
        default=None
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""timestamp""",
        default=None
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DocumentType name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DocumentType eng name""",
        default=None
    )

@strawberry.input(
    description="""DocumentType delete mutation"""
)
class DocumentTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""DocumentType id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DocumentType lastchange"""
    )


@strawberry.type(
    description="""DocumentType mutation"""
)
class DocumentTypeMutation:
    @strawberry.mutation(
        description="""Insert a DocumentType""",
        permission_classes=[
            SimpleInsertPermission[DocumentTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def document_type_insert(
        self,
        info: strawberry.types.Info,
        facility: DocumentTypeInsertGQLModel
    ) -> typing.Union[DocumentTypeGQLModel, InsertError[DocumentTypeGQLModel]]:
        return await Insert[DocumentTypeGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.mutation(
        description="""Update a DocumentType""",
        permission_classes=[
            SimpleUpdatePermission[DocumentTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def document_type_update(
        self,
        info: strawberry.types.Info,
        facility: DocumentTypeUpdateGQLModel
    ) -> typing.Union[DocumentTypeGQLModel, UpdateError[DocumentTypeGQLModel]]:
        return await Update[DocumentTypeGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.mutation(
        description="""Delete a DocumentType""",
        permission_classes=[
            SimpleDeletePermission[DocumentTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def document_type_delete(
        self,
        info: strawberry.types.Info,
        facility: DocumentTypeDeleteGQLModel
    ) -> typing.Optional[DeleteError[DocumentTypeGQLModel]]:
        return await Delete[DocumentTypeGQLModel].DoItSafeWay(info=info, entity=facility)    