import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def event_type_insert(SchemaExecutor, event):
    query = """mutation eventTypeInsert(
	$name: String! # null, 
	$nameEn: String # null, 
	$parentId: UUID # null, 
	$id: UUID # null
) {
  eventTypeInsert(
	eventType: {
	name: $name, 
	nameEn: $nameEn, 
	parentId: $parentId, 
	id: $id}
  ) {
    ... on EventTypeGQLModel { ...EventType }
    ... on EventTypeGQLModelInsertError { ...EventTypeGQLModelInsertError }
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

fragment Event on EventGQLModel {
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
    startdate
    enddate
    duration_raw
    valid
    place
    facilityId
    facility { __typename }
    facilityReservations { __typename }
    mastereventId
    subevents { __typename }
    typeId
    type { __typename }
    userInvitations { __typename }
    # duration
    }

fragment EventType on EventTypeGQLModel {
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
  parentId
  parent { __typename }
  children { __typename }
  events {
  ...Event
}
  }

fragment EventTypeGQLModelInsertError on EventTypeGQLModelInsertError {
  __typename
  Entity {
  ...EventType
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

async def event_type_update(SchemaExecutor, event):
    query = """mutation eventTypeUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null
) {
  eventTypeUpdate(
	eventType: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn}
  ) {
    ... on EventTypeGQLModel { ...EventType }
    ... on EventTypeGQLModelUpdateError { ...Error }
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

fragment Event on EventGQLModel {
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
    startdate
    enddate
    duration_raw
    valid
    place
    facilityId
    facility { __typename }
    facilityReservations { __typename }
    mastereventId
    subevents { __typename }
    typeId
    type { __typename }
    userInvitations { __typename }
    # duration
    }

fragment EventType on EventTypeGQLModel {
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
  parentId
  parent { __typename }
  children { __typename }
  events {
  ...Event
}
  }

fragment Error on EventTypeGQLModelUpdateError {
  __typename
  Entity {
  ...EventType
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

async def event_type_delete(SchemaExecutor, event):
    query = """mutation eventTypeDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  eventTypeDelete(
	eventType: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...EventTypeGQLModelDeleteError
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

fragment Event on EventGQLModel {
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
    startdate
    enddate
    duration_raw
    valid
    place
    facilityId
    facility { __typename }
    facilityReservations { __typename }
    mastereventId
    subevents { __typename }
    typeId
    type { __typename }
    userInvitations { __typename }
    # duration
    }

fragment EventType on EventTypeGQLModel {
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
  parentId
  parent { __typename }
  children { __typename }
  events {
  ...Event
}
  }

fragment EventTypeGQLModelDeleteError on EventTypeGQLModelDeleteError {
__typename
Entity {
  ...EventType
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


@pytest.mark.asyncio
async def test_event_type_insert(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
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

    input = {
        "name": "Test Event",
    }
    result = await event_type_insert(SchemaExecutor, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_event_type_update(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
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

    input = {
        "name": "Test Event",
        "nameEn": "Test Event",
    }
    delta = {
        "name": "Updated Test Event",
        "nameEn": "Updated Test Event",
    }
    result = await event_type_insert(SchemaExecutor, input)
    event_type_inserted = assert_insert(result)
    payload = {
        **input,
        **event_type_inserted,
        **delta
    }
    result = await event_type_update(SchemaExecutor, payload)
    event_type_updated = assert_update(result)
    assert_same(delta, event_type_updated)

@pytest.mark.asyncio
async def test_event_type_delete(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
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

    input = {
        "name": "Test Event",
    }
    result = await event_type_insert(SchemaExecutor, input)
    event_type_inserted = assert_insert(result)
    payload = {
        **input,
        **event_type_inserted
    }
    result = await event_type_delete(SchemaExecutor, payload)
    assert_delete(result)