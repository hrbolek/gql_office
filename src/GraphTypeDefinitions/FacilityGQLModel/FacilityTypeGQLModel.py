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

# FacilityCategoryGQLModel = typing.Annotated["FacilityCategoryGQLModel", strawberry.lazy(".FacilityCategoryGQLModel")]

@createInputs
@dataclasses.dataclass
class FacilityTypeInputFilter:
    name: str
    name_en: str
    id: IDType


@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Facility type tree"""
)
class FacilityTypeGQLModel(BaseGQLModel):
    async def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).FacilityTypeModel
    
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility type name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility type eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["FacilityTypeGQLModel"] = strawberry.field(
        description="""Facility type parent""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FacilityTypeGQLModel"](fkey_field_name="parent_id")
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Facility type parent id""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    children: typing.List["FacilityTypeGQLModel"] = strawberry.field(
        description="""Facility type children""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["FacilityTypeGQLModel"](fkey_field_name="parent_id", whereType=FacilityTypeInputFilter)
    )

@strawberry.interface(
    description=""""""
)
class FacilityTypeQuery:
    facility_type_by_id: typing.Optional[FacilityTypeGQLModel] = strawberry.field(
        description="""Get a FacilityType by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=FacilityTypeGQLModel.load_with_loader
    )

    facility_type_page: typing.List[FacilityTypeGQLModel] = strawberry.field(
        description="""Get a page of FacilityTypes""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[FacilityTypeInputFilter](whereType=FacilityTypeInputFilter)
    )

    
@strawberry.input(
    description="""FacilityType insert mutation"""
)
class FacilityTypeInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="""FacilityType name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""FacilityType eng name""",
        default=None
    )
    category_id: IDType = strawberry.field(
        description="""FacilityType category id"""
    )

@strawberry.input(
    description="""FacilityType update mutation"""
)
class FacilityTypeUpdateGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="""FacilityType name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""FacilityType eng name""",
        default=None
    )
    category_id: typing.Optional[IDType] = strawberry.field(
        description="""FacilityType category id""",
        default=None
    )

@strawberry.input(
    description="""FacilityType delete mutation"""
)
class FacilityTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""FacilityType id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""FacilityType lastchange"""
    )


@strawberry.interface(
    description="""FacilityType mutation"""
)
class FacilityTypeMutation:
    @strawberry.field(
        description="""Insert a FacilityType""",
        permission_classes=[
            SimpleInsertPermission
        ]
    )
    async def facility_type_insert(
        self,
        info: strawberry.types.Info,
        facility: FacilityTypeInsertGQLModel
    ) -> typing.Union[FacilityTypeGQLModel, InsertError[FacilityTypeGQLModel]]:
        return await Insert[FacilityTypeGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.field(
        description="""Update a FacilityType""",
        permission_classes=[
            SimpleUpdatePermission
        ]
    )
    async def facility_type_update(
        self,
        info: strawberry.types.Info,
        facility: FacilityTypeUpdateGQLModel
    ) -> typing.Union[FacilityTypeGQLModel, UpdateError[FacilityTypeGQLModel]]:
        return await Update[FacilityTypeGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.field(
        description="""Delete a FacilityType""",
        permission_classes=[
            SimpleDeletePermission
        ]
    )
    async def facility_type_delete(
        self,
        info: strawberry.types.Info,
        facility: FacilityTypeDeleteGQLModel
    ) -> typing.Optional[DeleteError[FacilityTypeGQLModel]]:
        return await Delete[FacilityTypeGQLModel].DoItSafeWay(info=info, entity=facility)