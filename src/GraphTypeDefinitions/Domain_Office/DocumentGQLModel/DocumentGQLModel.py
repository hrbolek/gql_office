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

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType
from .DocumentInterfaceGQLModel import DocumentInterfaceGQLModel
from .DigitalDocumentGQLModel import DigitalSubmissionGQLModel
from .ElectronicDocumentGQLModel import ElectronicDocumentGQLModel

StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("..StateGQLModel")]
DocumentTypeGQLModel = typing.Annotated["DocumentTypeGQLModel", strawberry.lazy(".DocumentTypeGQLModel")]

@createInputs
@dataclasses.dataclass
class DocumentInputFilter:
    name: str
    name_en: str
    id: IDType
    parent_id: IDType

@strawberry.federation.type(
    keys=["id"],
    description="""Interface for a Document either a DigitalDocument or a PhysicalDocument"""
)
class DocumentGQLModel(BaseGQLModel, DocumentInterfaceGQLModel):

    as_digital: typing.Optional[DigitalSubmissionGQLModel] = strawberry.field(description="Digital document ")
    as_electronic: typing.Optional[ElectronicDocumentGQLModel] = strawberry.field(description="Electronic document ")

    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: IDType):
        from .DigitalDocumentGQLModel import DigitalSubmissionGQLModel
        from .ElectronicDocumentGQLModel import ElectronicDocumentGQLModel

        if id is None: return None

        _id = IDType(id) if isinstance(id, str) else id

        loaders = (DigitalSubmissionGQLModel.load_with_loader, ElectronicDocumentGQLModel.load_with_loader)
        futures = (loader.load(_id) for loader in loaders)
        [as_digital, as_electronic] = await asyncio.gather(*futures)

        one = (as_digital or as_electronic)
                
        return cls(
            name=one.name,
            name_en=one.name_en,
            description=one.description,
            state_id=one.state_id,
            type_id=one.type_id,
            parent_id=one.parent_id,
            as_digital=as_digital,
            as_electronic=as_electronic
        ) if one else None
        
    
    @classmethod
    def resolve_reference(cls, info: strawberry.types.Info, id: IDType, **otherdata):
        return cls.load_with_loader(info=info, id=id)

    # @strawberry.field(description="sub documents")
    # async def children(self, 
    #     info: strawberry.types.Info, 
    #     # skip: typing.Optional[int]=0,
    #     # limit: typing.Optional[int]=0
    # ) -> typing.List["DocumentGQLModel"]:
    #     id = (self.as_digital or self.as_electronic).id
    #     loaders = (DigitalSubmissionGQLModel.getLoader(info=info), ElectronicDocumentGQLModel.getLoader(info=info))
    #     futures = (loader.filter_by(parent_id=id) for loader in loaders)
    #     [c1, c2] = await asyncio.gather(*futures)
    #     result = [
    #         DocumentGQLModel(
    #             name=one.name,
    #             name_en=one.name_en,
    #             description=one.description,
    #             state_id=one.state_id,
    #             type_id=one.type_id,
    #             parent_id=one.parent_id,
    #             as_digital=one
    #         ) for one in c1
    #     ]
    #     result.extend((
    #         DocumentGQLModel(
    #             name=one.name,
    #             name_en=one.name_en,
    #             description=one.description,
    #             state_id=one.state_id,
    #             type_id=one.type_id,
    #             parent_id=one.parent_id,
    #             as_electronic=one
    #         ) for one in c2
    #     ))
    #     return result

    @strawberry.field(description="master document")
    async def parent(self, 
        info: strawberry.types.Info, 
        # skip: typing.Optional[int]=0,
        # limit: typing.Optional[int]=0
    ) -> typing.Optional["DocumentGQLModel"]:
        parent_id = (self.as_digital or self.as_electronic).parent_id
        loaders = (DigitalSubmissionGQLModel.getLoader(info=info), ElectronicDocumentGQLModel.getLoader(info=info))
        futures = (loader.load(parent_id) for loader in loaders)
        [c1, c2] = await asyncio.gather(*futures)
        one = c1 or c2
        return DocumentGQLModel(
            name=one.name,
            name_en=one.name_en,
            description=one.description,
            state_id=one.state_id,
            type_id=one.type_id,
            parent_id=one.parent_id,
            as_electronic=c1,
            as_digital=c2
        )


@strawberry.interface(description="")
class DocumentQuery:

    @strawberry.field(description="returns a document (if exists) regardless it is electronic or digital")
    async def document_id(self, info: strawberry.types.Info, id: IDType) -> typing.Optional[DocumentGQLModel]:
        result = await DocumentGQLModel.load_with_loader(info, id=id)  
        return result
