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
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType

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
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).FacilityTypeModel
    
    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path .""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

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
        resolver=PageResolver[FacilityTypeGQLModel](whereType=FacilityTypeInputFilter)
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
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""FacilityType master id""",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="""FacilityType id client generated""",
        default=None
    )
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""FacilityType update mutation"""
)
class FacilityTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""FacilityType id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""FacilityType lastchange"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""FacilityType name""",
        default=strawberry.UNSET
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""FacilityType eng name""",
        default=strawberry.UNSET
    )
    changedby_id: strawberry.Private[IDType] = None

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


@strawberry.type(
    description="""FacilityType mutation"""
)
class FacilityTypeMutation:
    @strawberry.mutation(
        description="""Insert a FacilityType""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, FacilityTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )
    async def facility_type_insert(
        self,
        info: strawberry.types.Info,
        facility_type: FacilityTypeInsertGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[FacilityTypeGQLModel, InsertError[FacilityTypeGQLModel]]:
        return await Insert[FacilityTypeGQLModel].DoItSafeWay(info=info, entity=facility_type)
    
    @strawberry.mutation(
        description="""Update a FacilityType""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, FacilityTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )
    async def facility_type_update(
        self,
        info: strawberry.types.Info,
        facility_type: FacilityTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[FacilityTypeGQLModel, UpdateError[FacilityTypeGQLModel]]:
        return await Update[FacilityTypeGQLModel].DoItSafeWay(info=info, entity=facility_type)
    
    @strawberry.mutation(
        description="""Delete a FacilityType""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, FacilityTypeGQLModel](
                roles=["superadmin"]
            )
        ],
    )
    async def facility_type_delete(
        self,
        info: strawberry.types.Info,
        facility_type: FacilityTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[FacilityTypeGQLModel]]:
        return await Delete[FacilityTypeGQLModel].DoItSafeWay(info=info, entity=facility_type)