import asyncio
import uuid
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

from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from ..BaseGQLModel import BaseGQLModel, IDType
# from ..TreeGQLModel import create_tree_parents_resolver, create_tree_parent_updater

FacilityTypeGQLModel = typing.Annotated["FacilityTypeGQLModel", strawberry.lazy(".FacilityTypeGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("..GroupGQLModel")]
EventFacilityReservationGQLModel = typing.Annotated["EventFacilityReservationGQLModel", strawberry.lazy("..EventGQLModel.EventFacilityReservationGQLModel")]
EventFacilityReservationInputFilter = typing.Annotated["EventFacilityReservationInputFilter", strawberry.lazy("..EventGQLModel.EventFacilityReservationGQLModel")]


# region FacilityGQLModel
@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Facility"""
)
class FacilityGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).FacilityModel
 
    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path .""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

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
        
    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility full name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
        )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Facility datetime """,
        permission_classes=[
            OnlyForAuthentized
        ]
        )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Facility datetime """,
        permission_classes=[
            OnlyForAuthentized
        ]
        )

    # address
    address: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility address""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    # valid
    valid: typing.Optional[bool] = strawberry.field(
        default=None,
        description="""is the facility still valid""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    capacity: typing.Optional[int] = strawberry.field(
        default=None,
        description="""Facility's capacity""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    # manager_id

    # address
    geometry: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility geometry (SVG)""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    geolocation: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Facility geo address (WGS84+zoom)""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    reservations: typing.List[EventFacilityReservationGQLModel] = strawberry.field(
        description="reservations for this event",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[EventFacilityReservationGQLModel](fkey_field_name="facility_id", whereType=EventFacilityReservationInputFilter)
    )

    group_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Facility geo address (WGS84+zoom)""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    facilitytype_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Facility geo address (WGS84+zoom)""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    master_facility_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Facility geo address (WGS84+zoom)""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    type_: typing.Optional["FacilityTypeGQLModel"] = strawberry.field(
        name="type",
        description="""Facility type""",
        permission_classes=[
            OnlyForAuthentized
            ],
        resolver=ScalarResolver["FacilityTypeGQLModel"](fkey_field_name="facilitytype_id")
    )

    master_facility: typing.Optional["FacilityGQLModel"] = strawberry.field(
        description="""Facility above this""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["FacilityGQLModel"](fkey_field_name="master_facility_id")
    )

    master_facilities: typing.List["FacilityGQLModel"] = strawberry.field(
        default_factory=list,
        description="""Facilities above this""",
        permission_classes=[
            OnlyForAuthentized
        ],
        # resolver=create_tree_parents_resolver(FacilityGQLModel)
    )

    sub_facilities: typing.List["FacilityGQLModel"] = strawberry.field(
        description="""Facilities inside facility (like buildings in an areal)""",
        permission_classes=[
            OnlyForAuthentized
            ],
        resolver=VectorResolver["FacilityGQLModel"](fkey_field_name="master_facility_id", whereType=None)
    )

    group: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="""Group""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="group_id")
    )   

@createInputs
@dataclasses.dataclass
class FacilityInputFilter:
    name: str
    name_en: str
    valid: bool
    label: str
    capacity: int
    group_id: IDType
    master_facility_id: IDType
    facilitytype_id: IDType
    address: str

@strawberry.federation.interface(
    description="""Facility queries"""
)
class FacilityQuery:
    
    facility_by_id: typing.Optional[FacilityGQLModel] = strawberry.field(
        description="Get a facility by id",
        permission_classes=[OnlyForAuthentized],
        resolver=FacilityGQLModel.load_with_loader
    )

    facility_page: typing.List[FacilityGQLModel] = strawberry.field(
        description="Get a page of facilities",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[FacilityGQLModel](whereType=FacilityInputFilter)
    )

@strawberry.input(description="initial attributes for facility insert")
class FacilityInsertGQLModel:
    master_facility_id: IDType = strawberry.field(description="to which facility this facility belongs", default=None)
    name: str = strawberry.field(description="name of the new facility")
    facilitytype_id: typing.Optional[IDType] = strawberry.field(description="facility type", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="primary key (UUID), could be client generated", default=None)

    name_en: typing.Optional[str] = strawberry.field(description="english name of facility", default="")
    label: typing.Optional[str] = strawberry.field(description="full name (including masterfacility)", default="")
    address: typing.Optional[str] = strawberry.field(description="postal address", default="")
    valid: typing.Optional[bool] = strawberry.field(description="if facility exists", default=True)
    capacity: typing.Optional[int] = strawberry.field(description="facility capacity", default=0)
    geometry: typing.Optional[str] = strawberry.field(description="SVG overlay for leaflet", default="")
    geolocation: typing.Optional[str] = strawberry.field(description="WSGBLX;WGSBLY;ZOOM", default="")

    group_id: typing.Optional[IDType] = strawberry.field(description="group which is responsible for management of this facility", default=None)
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(description="initial attributes for facility insert")
class FacilityInsertMasterGQLModel:
    # rbacobject_id: IDType = strawberry.field(description="Rbac object id for master facility, it defines access rights to the facility")
    name: str = strawberry.field(description="name of the new facility")
    facilitytype_id: typing.Optional[IDType] = strawberry.field(description="facility type", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="primary key (UUID), could be client generated", default=None)

    name_en: typing.Optional[str] = strawberry.field(description="english name of facility", default="")
    label: typing.Optional[str] = strawberry.field(description="full name (including masterfacility)", default="")
    address: typing.Optional[str] = strawberry.field(description="postal address", default="")
    valid: typing.Optional[bool] = strawberry.field(description="if facility exists", default=True)
    capacity: typing.Optional[int] = strawberry.field(description="facility capacity", default=0)
    geometry: typing.Optional[str] = strawberry.field(description="SVG overlay for leaflet", default="")
    geolocation: typing.Optional[str] = strawberry.field(description="WSGBLX;WGSBLY;ZOOM", default="")

    group_id: typing.Optional[IDType] = strawberry.field(description="group which is responsible for management of this facility", default=None)
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(description="Input definition for facility update")
class FacilityUpdateGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the type", default=strawberry.UNSET)
    name_en: typing.Optional[str] = strawberry.field(description="english name of facility", default=strawberry.UNSET)
    label: typing.Optional[str] = strawberry.field(description="full name (including masterfacility)", default=strawberry.UNSET)
    address: typing.Optional[str] = strawberry.field(description="postal address", default=strawberry.UNSET)
    valid: typing.Optional[bool] = strawberry.field(description="if facility exists", default=strawberry.UNSET)
    capacity: typing.Optional[int] = strawberry.field(description="facility capacity", default=strawberry.UNSET)
    geometry: typing.Optional[str] = strawberry.field(description="SVG overlay for leaflet", default=strawberry.UNSET)
    geolocation: typing.Optional[str] = strawberry.field(description="WSGBLX;WGSBLY;ZOOM", default=strawberry.UNSET)
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(description="Input definition for facility master change")
class FacilityMoveGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    master_facility_id: IDType = strawberry.field(description="to which facility this facility belongs")

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(description="Input definition for facility delete")
class FacilityDeleteGQLModel:
    id: IDType = strawberry.field(description="client generated primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

@strawberry.federation.type(
    description="""Facility mutations"""
)
class FacilityMutation:

    @strawberry.field(
        description="Insert a facility under master facility.",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, FacilityGQLModel](
                roles=[
                    "nemovitostní administrátor", 
                ]
            ),
            UserRoleProviderExtension[InsertError, FacilityGQLModel](),
            RbacProviderExtension[InsertError, FacilityGQLModel](),
            LoadDataExtension[InsertError, FacilityGQLModel](
                getLoader=FacilityGQLModel.getLoader,
                primary_key_name="master_facility_id"
            )
        ]
    )
    async def facility_insert(
        self, 
        info: strawberry.types.Info, 
        facility: FacilityInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FacilityGQLModel, InsertError[FacilityGQLModel]]:
        # TODO create rbacobject_id for the new facility based on provided master_facility_id and rbacobject_id of the master facility, then set it to the new facility, so the new facility is properly connected to RBAC hierarchy and permissions are properly applied to it without need to reload the whole tree of facilities
        return await Insert[FacilityGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.field(
        description="Insert a facility without master facility. ",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, FacilityGQLModel](roles=["superadmin"]),
        ]
    )
    async def facility_master_insert(
        self, 
        info: strawberry.types.Info, 
        facility: FacilityInsertMasterGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[FacilityGQLModel, InsertError[FacilityGQLModel]]:
        # TODO check facility.group_id exists
        facility.rbacobject_id = facility.group_id
        return await Insert[FacilityGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.field(
        description="Update a facility",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, FacilityGQLModel](
                roles=[
                    "nemovitostní administrátor", 
                ]
            ),
            UserRoleProviderExtension[UpdateError, FacilityGQLModel](),
            RbacProviderExtension[UpdateError, FacilityGQLModel](),
            LoadDataExtension[UpdateError, FacilityGQLModel]()
        ],
    )
    async def facility_update(
        self, 
        info: strawberry.types.Info, 
        facility: FacilityUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FacilityGQLModel, UpdateError[FacilityGQLModel]]:
        return await Update[FacilityGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.field(
        description="Delete a facility",
        permission_classes=[
            OnlyForAuthentized,
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, FacilityGQLModel](
                roles=[
                    "nemovitostní administrátor", 
                ]
            ),
            UserRoleProviderExtension[DeleteError, FacilityGQLModel](),
            RbacProviderExtension[DeleteError, FacilityGQLModel](),
            LoadDataExtension[DeleteError, FacilityGQLModel]()
        ],
    )
    async def facility_delete(
        self, 
        info: strawberry.types.Info, 
        facility: FacilityDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[FacilityGQLModel]]:
        return await Delete[FacilityGQLModel].DoItSafeWay(info=info, entity=facility)
    
    @strawberry.field(
        description="Move a facility aka changes master facility of a facility",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, FacilityGQLModel](
                roles=[
                    "nemovitostní administrátor", 
                ]
            ),
            UserRoleProviderExtension[UpdateError, FacilityGQLModel](),
            RbacProviderExtension[UpdateError, FacilityGQLModel](),
            LoadDataExtension[UpdateError, FacilityGQLModel]()
        ],
    )
    async def facility_move(
        self, 
        info: strawberry.types.Info, 
        facility: FacilityMoveGQLModel
    ) -> typing.Union[FacilityGQLModel, UpdateError[FacilityGQLModel]]:
        return await Update[FacilityGQLModel].DoItSafeWay(info=info, entity=facility)