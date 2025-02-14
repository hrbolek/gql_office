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

@strawberry.type(
    description="""Entity representing a Facility category"""
)
class FacilityCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).FacilityCategoryModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

@createInputs
@dataclasses.dataclass
class FacilityCategoryInputFilter:
    name: str
    name_en: str
    id: IDType


@strawberry.interface(
    description=""""""
)
class FacilityCategoryQuery():
    facility_category_by_id: typing.Optional[FacilityCategoryGQLModel] = strawberry.field(
        description="""get a facility category by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=FacilityCategoryGQLModel.load_with_loader
    )

    facility_category_page: typing.List[FacilityCategoryGQLModel] = strawberry.field(
        description="""get a page of facility categories""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[FacilityCategoryGQLModel](whereType=FacilityCategoryInputFilter)
    )


@strawberry.input(
    description="""Input type for creating a FacilityCategory"""
)
class FacilityCategoryCreateInput:
    id: typing.Optional[IDType] = strawberry.field(
        description="""Facility category id""",
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Facility category name assigned by an administrator""",
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Facility category eng name assigned by an administrator""",
    )

    createdby_id: strawberry.Private[IDType] = None


    

@strawberry.input(
    description="""Input type for updating a FacilityCategory"""
)
class FacilityCategoryUpdateInput:
    id: IDType = strawberry.field(
        description="""Facility category id""",
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Facility category name assigned by an administrator""",
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""Facility category eng name assigned by an administrator""",
    )

    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a FacilityCategory"""
)
class FacilityCategoryDeleteInput:
    id: IDType = strawberry.field(
        description="""Facility category id""",
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Mutation to create a FacilityCategory"""
)
class FacilityCategoryMutations:
    @strawberry.mutation(
        description="""Create a FacilityCategory""",
        permission_classes=[SimpleInsertPermission]
    )
    async def facility_category_create(
        self,
        info: strawberry.Info,
        facility_category: FacilityCategoryCreateInput
    ) -> typing.Union[FacilityCategoryGQLModel, InsertError]:
        return await Insert[FacilityCategoryGQLModel].DoItSafeWay(info=info, entity=facility_category)
    
    @strawberry.mutation(
        description="""Update a FacilityCategory""",
        permission_classes=[SimpleUpdatePermission]
    )
    async def facility_category_update(
        self,
        info: strawberry.Info,
        facility_category: FacilityCategoryUpdateInput
    ) -> typing.Union[FacilityCategoryGQLModel, UpdateError[FacilityCategoryGQLModel]]:
        return await Update[FacilityCategoryGQLModel].DoItSafeWay(info=info, entity=facility_category)
    
    @strawberry.mutation(
        description="""Delete a FacilityCategory""",
        permission_classes=[SimpleDeletePermission]
    )
    async def facility_category_delete(
        self,
        info: strawberry.Info,
        facility_category: FacilityCategoryDeleteInput
    ) -> typing.Optional[DeleteError[FacilityCategoryGQLModel]]:
        return await Delete[FacilityCategoryGQLModel].DoItSafeWay(info=info, entity=facility_category)

    