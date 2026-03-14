import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def digital_form_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalFormInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def digital_form_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalFormUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def digital_form_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalFormDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


default_user = {
    "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
    "roles": [{
        "roletype": {"name": "superadmin"}
    }]
}
default_roles = {
    "result": [
        {
            "roletype": {
                "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                "name": "procesní administrátor"
            }
        }
    ]
}

@pytest.mark.asyncio
async def test_digital_form_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Digital",
    }
    result = await digital_form_insert(SchemaExecutor, CreateMutation, insert_data)
    inserted = assert_insert(result)
    result = await digital_form_delete(SchemaExecutor, CreateMutation, inserted)
    deleted = assert_delete

@pytest.mark.asyncio
async def test_digital_form_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Digital",
    }
    result = await digital_form_insert(SchemaExecutor, CreateMutation, insert_data)
    digital_form_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **digital_form_inserted
    }
    result = await digital_form_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

@pytest.mark.asyncio
async def test_digital_form_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Digital",
    }
    update_data = {
        "name": "Updated Test Digital",
    }
    result = await digital_form_insert(SchemaExecutor, CreateMutation, insert_data)
    digital_form_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **digital_form_inserted,
        **update_data
    }
    result = await digital_form_update(SchemaExecutor, CreateMutation, payload)
    digital_form_updated = assert_update(result)
    updated = assert_same(update_data, digital_form_updated)
    result = await digital_form_delete(SchemaExecutor, CreateMutation, updated)
    deleted = assert_delete

