import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def facility_type_insert(SchemaExecutor, facility):
    query = """mutation facilityTypeInsert(
	$name: String # null, 
	$nameEn: String # null, 
	$parentId: UUID # null, 
	$id: UUID # null
) {
  facilityTypeInsert(
	facilityType: {
	name: $name, 
	nameEn: $nameEn, 
	parentId: $parentId, 
	id: $id}
  ) {
    ... on FacilityTypeGQLModel { ...FacilityType }
    ... on FacilityTypeGQLModelInsertError { ...FacilityTypeGQLModelInsertError }
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

fragment FacilityType on FacilityTypeGQLModel {
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
  name
  nameEn
  parent { __typename }
  parentId
  children { __typename }
  }

fragment FacilityTypeGQLModelInsertError on FacilityTypeGQLModelInsertError {
  __typename
  Entity {
  ...FacilityType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**facility}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def facility_type_update(SchemaExecutor, facility):
    query = """mutation facilityTypeUpdate(
	$id: UUID! # null, 
	$lastchange: DateTime! # null, 
	$name: String # null, 
	$nameEn: String # null
) {
  facilityTypeUpdate(
	facilityType: {
	id: $id, 
	lastchange: $lastchange, 
	name: $name, 
	nameEn: $nameEn}
  ) {
    ... on FacilityTypeGQLModel { ...FacilityType }
    ... on FacilityTypeGQLModelUpdateError { ...Error }
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

fragment FacilityType on FacilityTypeGQLModel {
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
  name
  nameEn
  parent { __typename }
  parentId
  children { __typename }
  }

fragment Error on FacilityTypeGQLModelUpdateError {
  __typename
  Entity {
  ...FacilityType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**facility}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def facility_type_delete(SchemaExecutor, facility):
    query = """mutation facilityTypeDelete(
	$id: UUID! # null, 
	$lastchange: DateTime! # null
) {
  facilityTypeDelete(
	facilityType: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...FacilityTypeGQLModelDeleteError
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

fragment FacilityType on FacilityTypeGQLModel {
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
  name
  nameEn
  parent { __typename }
  parentId
  children { __typename }
  }

fragment FacilityTypeGQLModelDeleteError on FacilityTypeGQLModelDeleteError {
__typename
Entity {
  ...FacilityType
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **facility
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result


@pytest.mark.asyncio
async def test_facility_type_insert(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Facility",
    }
    result = await facility_type_insert(SchemaExecutor, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_facility_type_update(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Facility",
        "nameEn": "Test Facility",
    }
    delta = {
        "name": "Updated Test Facility",
        "nameEn": "Updated Test Facility",
    }
    result = await facility_type_insert(SchemaExecutor, input)
    facility_type_inserted = assert_insert(result)
    payload = {
        **input,
        **facility_type_inserted,
        **delta
    }
    result = await facility_type_update(SchemaExecutor, payload)
    facility_type_updated = assert_update(result)
    assert_same(delta, facility_type_updated)

@pytest.mark.asyncio
async def test_facility_type_delete(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Facility",
    }
    result = await facility_type_insert(SchemaExecutor, input)
    facility_type_inserted = assert_insert(result)
    payload = {
        **input,
        **facility_type_inserted
    }
    result = await facility_type_delete(SchemaExecutor, payload)
    assert_delete(result)