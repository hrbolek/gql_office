import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def form_submission_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalFormSubmissionInsert2")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def form_submission_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalFormSubmissionUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def form_submission_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalFormSubmissionDelete")
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
async def test_form_submission_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Form",
        "formId": "29617a51-e2d4-4ae1-aae9-8221b624683c"
    }
    result = await form_submission_insert(SchemaExecutor, CreateMutation, insert_data)
    inserted = assert_insert(result)
    result = await form_submission_delete(SchemaExecutor, CreateMutation, inserted)
    deleted = assert_delete

@pytest.mark.asyncio
async def test_form_submission_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Form",
        "formId": "29617a51-e2d4-4ae1-aae9-8221b624683c"
    }
    result = await form_submission_insert(SchemaExecutor, CreateMutation, insert_data)
    form_submission_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **form_submission_inserted
    }
    result = await form_submission_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

@pytest.mark.asyncio
async def test_form_submission_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Form",
        "formId": "29617a51-e2d4-4ae1-aae9-8221b624683c"
    }
    update_data = {
        "name": "Updated Test Form",
    }
    result = await form_submission_insert(SchemaExecutor, CreateMutation, insert_data)
    form_submission_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **form_submission_inserted,
        **update_data
    }
    result = await form_submission_update(SchemaExecutor, CreateMutation, payload)
    form_submission_updated = assert_update(result)
    updated = assert_same(update_data, form_submission_updated)
    result = await form_submission_delete(SchemaExecutor, CreateMutation, updated)
    deleted = assert_delete

