import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def request_type_insert(SchemaExecutor, request):
    query = """mutation requesttypeInsert(
	$mastergroupId: UUID! # Full description of initial requesttype attributes, 
	$id: UUID # Full description of initial requesttype attributes, 
	$name: String # Full description of initial requesttype attributes, 
	$initialForm: DigitalFormInsertGQLModel # Full description of initial requesttype attributes
) {
  requesttypeInsert(
	requestType: {
	mastergroupId: $mastergroupId, 
	id: $id, 
	name: $name, 
	initialForm: $initialForm}
  ) {
    ... on RequestTypeGQLModelInsertError { ...RequestTypeGQLModelInsertError }
    ... on RequestTypeGQLModel { ...RequestType }
  }
}

fragment RequestType on RequestTypeGQLModel {
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
    statemachineId
    stateId
    initialFormId
    statemachine { __typename }
    state { __typename }
    initialForm { __typename }
    }

fragment RequestTypeGQLModelInsertError on RequestTypeGQLModelInsertError {
  __typename
  Entity {
  ...RequestType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**request}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def request_type_update(SchemaExecutor, request):
    query = """mutation requesttypeUpdate(
	$id: UUID! # Full description of requesttype attributes to be updated, 
	$lastchange: DateTime! # Full description of requesttype attributes to be updated
) {
  requesttypeUpdate(
	requestType: {
	id: $id, 
	lastchange: $lastchange}
  ) {
    ... on RequestTypeGQLModelUpdateError { ...Error }
    ... on RequestTypeGQLModel { ...RequestType }
  }
}

fragment RequestType on RequestTypeGQLModel {
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
    statemachineId
    stateId
    initialFormId
    statemachine { __typename }
    state { __typename }
    initialForm { __typename }
    }

fragment Error on RequestTypeGQLModelUpdateError {
  __typename
  Entity {
  ...RequestType
}
  msg
  failed
  code
  location
  input
  }

"""
    variable_values = {**request}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def request_type_delete(SchemaExecutor, request):
    query = """mutation requesttypeDelete(
	$id: UUID! # Identification of the requesttype record to be removed from db, 
	$lastchange: DateTime! # Identification of the requesttype record to be removed from db
) {
  requesttypeDelete(
	requestType: {
	id: $id, 
	lastchange: $lastchange}
  ) {
  ...RequestTypeGQLModelDeleteError
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

fragment StateMachine on StateMachineGQLModel {
    __typename
    id
    }

fragment State on StateGQLModel {
    __typename
    id
    }

fragment DigitalForm on DigitalFormGQLModel {
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
    description
    stateId
    state { __typename }
    parentId
    typeId
    type { __typename }
    allSections { __typename }
    submissions { __typename }
    sections { __typename }
    }

fragment RequestType on RequestTypeGQLModel {
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
  statemachineId
  stateId
  initialFormId
  statemachine {
  ...StateMachine
}
  state {
  ...State
}
  initialForm {
  ...DigitalForm
}
  }

fragment RequestTypeGQLModelDeleteError on RequestTypeGQLModelDeleteError {
__typename
Entity {
  ...RequestType
}
msg
code
failed
location
input
}

"""
    variable_values = {
        **request
    }
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result


@pytest.mark.asyncio
async def test_request_type_insert(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Request",
    }
    result = await request_type_insert(SchemaExecutor, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_request_type_update(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Request",
        "nameEn": "Test Request",
    }
    delta = {
        "name": "Updated Test Request",
        "nameEn": "Updated Test Request",
    }
    result = await request_type_insert(SchemaExecutor, input)
    request_type_inserted = assert_insert(result)
    payload = {
        **input,
        **request_type_inserted,
        **delta
    }
    result = await request_type_update(SchemaExecutor, payload)
    request_type_updated = assert_update(result)
    assert_same(delta, request_type_updated)

@pytest.mark.asyncio
async def test_request_type_delete(SchemaExecutor, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Request",
    }
    result = await request_type_insert(SchemaExecutor, input)
    request_type_inserted = assert_insert(result)
    payload = {
        **input,
        **request_type_inserted
    }
    result = await request_type_delete(SchemaExecutor, payload)
    assert_delete(result)