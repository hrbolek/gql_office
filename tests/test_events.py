import pytest
import logging

async def event_insert(SchemaExecutor, event):
    query = """mutation eventInsert(
	$mastereventId: UUID! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$description: String # null, 
	$startDate: DateTime # null, 
	$endDate: DateTime # null, 
	$id: UUID # null, 
	$subevents: [EventInsertGQLModel!] # null
) {
  eventInsert(
	event: {
	mastereventId: $mastereventId, 
	name: $name, 
	nameEn: $nameEn, 
	description: $description, 
	startDate: $startDate, 
	endDate: $endDate, 
	id: $id, 
	subevents: $subevents}
  ) {
    ... on EventGQLModel { ...Event }
    ... on EventGQLModelInsertError { ...EventGQLModelInsertError }
  }
}

fragment User on UserGQLModel {
    __typename
    id
    }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
    }

fragment Facility on FacilityGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    name
    nameEn
    label
    startdate
    enddate
    address
    valid
    capacity
    geometry
    geolocation
    reservations { __typename }
    groupId
    facilitytypeId
    masterFacilityId
    type { __typename }
    masterFacility { __typename }
    masterFacilities { __typename }
    subFacilities { __typename }
    group { __typename }
    }

fragment EventFacilityReservation on EventFacilityReservationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    eventId
    event { __typename }
    facilityId
    facility { __typename }
    stateId
    state { __typename }
    }

fragment EventType on EventTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    path
    name
    nameEn
    description
    parentId
    parent { __typename }
    children { __typename }
    events { __typename }
    }

fragment EventInvitation on EventInvitationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    eventId
    userId
    stateId
    event { __typename }
    user { __typename }
    state { __typename }
    }

fragment Event on EventGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby {
  ...User
}
  changedby {
  ...User
}
  rbacobject {
  ...RBACObject
}
  path
  name
  nameEn
  description
  startdate
  enddate
  duration_raw
  valid
  place
  facilityId
  facility {
  ...Facility
}
  facilityReservations {
  ...EventFacilityReservation
}
  mastereventId
  subevents { __typename }
  typeId
  type {
  ...EventType
}
  userInvitations {
  ...EventInvitation
}
  # duration
  }

fragment EventGQLModelInsertError on EventGQLModelInsertError {
  __typename
  Entity {
  ...Event
}
  msg
  failed
  code
  location
  input
  }
"""
    variable_values = {**event}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def event_update(SchemaExecutor, event):
    query = """mutation eventUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null, 
	$description: String # null, 
	$startdate: DateTime # null, 
	$enddate: DateTime # null
) {
  eventUpdate(
	event: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn, 
	description: $description, 
	startdate: $startdate, 
	enddate: $enddate}
  ) {
    ... on EventGQLModel { ...Event }
    ... on EventGQLModelUpdateError { ...Error }
  }
}

fragment User on UserGQLModel {
    __typename
    id
    }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
    }

fragment Facility on FacilityGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    name
    nameEn
    label
    startdate
    enddate
    address
    valid
    capacity
    geometry
    geolocation
    reservations { __typename }
    groupId
    facilitytypeId
    masterFacilityId
    type { __typename }
    masterFacility { __typename }
    masterFacilities { __typename }
    subFacilities { __typename }
    group { __typename }
    }

fragment EventFacilityReservation on EventFacilityReservationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    eventId
    event { __typename }
    facilityId
    facility { __typename }
    stateId
    state { __typename }
    }

fragment EventType on EventTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    path
    name
    nameEn
    description
    parentId
    parent { __typename }
    children { __typename }
    events { __typename }
    }

fragment EventInvitation on EventInvitationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    eventId
    userId
    stateId
    event { __typename }
    user { __typename }
    state { __typename }
    }

fragment Event on EventGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby {
  ...User
}
  changedby {
  ...User
}
  rbacobject {
  ...RBACObject
}
  path
  name
  nameEn
  description
  startdate
  enddate
  duration_raw
  valid
  place
  facilityId
  facility {
  ...Facility
}
  facilityReservations {
  ...EventFacilityReservation
}
  mastereventId
  subevents { __typename }
  typeId
  type {
  ...EventType
}
  userInvitations {
  ...EventInvitation
}
  # duration
  }

fragment Error on EventGQLModelUpdateError {
  __typename
  Entity {
  ...Event
}
  msg
  failed
  code
  location
  input
  }
"""
    variable_values = {**event}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def event_delete(SchemaExecutor, event):
    query = """mutation eventDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  eventDelete(
	event: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...EventGQLModelDeleteError
}
}

fragment User on UserGQLModel {
    __typename
    id
    }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
    }

fragment Facility on FacilityGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    name
    nameEn
    label
    startdate
    enddate
    address
    valid
    capacity
    geometry
    geolocation
    reservations { __typename }
    groupId
    facilitytypeId
    masterFacilityId
    type { __typename }
    masterFacility { __typename }
    masterFacilities { __typename }
    subFacilities { __typename }
    group { __typename }
    }

fragment EventFacilityReservation on EventFacilityReservationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    eventId
    event { __typename }
    facilityId
    facility { __typename }
    stateId
    state { __typename }
    }

fragment EventType on EventTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    path
    name
    nameEn
    description
    parentId
    parent { __typename }
    children { __typename }
    events { __typename }
    }

fragment EventInvitation on EventInvitationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { __typename }
    changedby { __typename }
    rbacobject { __typename }
    eventId
    userId
    stateId
    event { __typename }
    user { __typename }
    state { __typename }
    }

fragment Event on EventGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby {
  ...User
}
  changedby {
  ...User
}
  rbacobject {
  ...RBACObject
}
  path
  name
  nameEn
  description
  startdate
  enddate
  duration_raw
  valid
  place
  facilityId
  facility {
  ...Facility
}
  facilityReservations {
  ...EventFacilityReservation
}
  mastereventId
  subevents { __typename }
  typeId
  type {
  ...EventType
}
  userInvitations {
  ...EventInvitation
}
  # duration
  }

fragment EventGQLModelDeleteError on EventGQLModelDeleteError {
__typename
Entity {
  ...Event
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **event
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

def assert_same(major, minor):
    for key in major:
        assert key in minor, f"Expected key '{key}' not found in minor result"
        assert major[key] == minor[key], f"Expected value for key '{key}' to be the same, but got {major[key]} and {minor[key]}"
    

def assert_insert(result):

    errors = result.get("errors", None)
    assert errors is None, f"Unexpected errors: {errors}"
    data = result.get("data", None)
    assert data is not None, "Data must be present in the result"
    
    for key, value in data.items():
        assert value is not None, f"{key} must not be null"
        break

    assert "__typename" in value, f"Expected __typename field not found: {value}"
    assert "lastchange" in value, f"Expected lastchange field not found: {value}"
    assert "id" in value, f"Expected id field not found: {value}"
    return value

def assert_update(result):

    errors = result.get("errors", None)
    assert errors is None, f"Unexpected errors: {errors}"
    data = result.get("data", None)
    assert data is not None, "Data must be present in the result"
    for key, value in data.items():
        assert value is not None, f"{key} must not be null"
        break

    assert "__typename" in value, f"Expected __typename field not found: {value}"
    assert "lastchange" in value, f"Expected lastchange field not found: {value}"
    assert "id" in value, f"Expected id field not found: {value}"
    if "Error" in value["__typename"]:
        assert "msg" in value, f"Expected msg field not found in error: {value}"
        assert "code" in value, f"Expected code field not found in error: {value}"
        assert False, f"Update failed with error: {value['msg']} (code: {value['code']})"

    return value

def assert_delete(result):

    errors = result.get("errors", None)
    assert errors is None, f"Unexpected errors: {errors}"
    
    assert "data" in result, "Data must be present in the result"
    data = result.get("data", None)
    for key, value in data.items():
        break

    assert value is None, f"Delete failed: {value}"

@pytest.mark.asyncio
async def test_event_insert(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    # WhoAmIExtensionOverride.set_user(
    #     {
    #         "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
    #         "roles": [{
    #             "roletype": {"name": "plánovací administrátor"}
    #         }]
    #     }
    # )
    RolePermissionSchemaExtensionOverride.set_response(
        {
            "result": [
                {
                    "roletype": {
                        "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                        "name": "plánovací administrátor"
                    }
                }
            ]
        }
    )

    event = {
        "mastereventId": "a64871f8-2308-48ff-adb2-33fb0b0741f1",
        "name": "Test Event",
    }
    result = await event_insert(SchemaExecutor, event)
    assert_insert(result)

@pytest.mark.asyncio
async def test_event_update(SchemaExecutor, RolePermissionSchemaExtensionOverride):
    RolePermissionSchemaExtensionOverride.set_response(
        {
            "result": [
                {
                    "roletype": {
                        "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                        "name": "plánovací administrátor"
                    }
                }
            ]
        }
    )

    event = {
        "mastereventId": "a64871f8-2308-48ff-adb2-33fb0b0741f1",
        "name": "Test Event",
    }
    delta = {
        "name": "Updated Test Event",
    }
    result = await event_insert(SchemaExecutor, event)
    event_inserted = assert_insert(result)
    payload = {
        **event,
        **event_inserted,
        **delta
    }
    result = await event_update(SchemaExecutor, payload)
    event_updated = assert_update(result)
    assert_same(delta, event_updated)

@pytest.mark.asyncio
async def test_event_delete(SchemaExecutor, RolePermissionSchemaExtensionOverride):
    RolePermissionSchemaExtensionOverride.set_response(
        {
            "result": [
                {
                    "roletype": {
                        "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                        "name": "plánovací administrátor"
                    }
                }
            ]
        }
    )

    event = {
        "mastereventId": "a64871f8-2308-48ff-adb2-33fb0b0741f1",
        "name": "Test Event",
    }
    result = await event_insert(SchemaExecutor, event)
    event_inserted = assert_insert(result)
    payload = {
        **event,
        **event_inserted
    }
    result = await event_delete(SchemaExecutor, payload)
    assert_delete(result)