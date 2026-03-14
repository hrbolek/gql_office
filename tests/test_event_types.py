import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def event_type_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_type_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_type_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

@pytest.mark.asyncio
async def test_event_type_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await event_type_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_event_type_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await event_type_insert(SchemaExecutor, CreateMutation, input)
    event_type_inserted = assert_insert(result)
    payload = {
        **input,
        **event_type_inserted,
        **delta
    }
    result = await event_type_update(SchemaExecutor, CreateMutation, payload)
    event_type_updated = assert_update(result)
    assert_same(delta, event_type_updated)

@pytest.mark.asyncio
async def test_event_type_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await event_type_insert(SchemaExecutor, CreateMutation, input)
    event_type_inserted = assert_insert(result)
    payload = {
        **input,
        **event_type_inserted
    }
    result = await event_type_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)