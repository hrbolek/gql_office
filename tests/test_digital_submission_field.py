import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def submission_field_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalSubmissionFieldInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def submission_field_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalSubmissionFieldUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def submission_field_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("digitalSubmissionFieldDelete")
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
async def test_submission_field_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Submission",
        "submissionId": "b0f1a7da-9f58-4e9d-bdc1-19d94770b20b",
        "sectionId": "dc4eb08a-7a80-4834-9021-c759c94a5d50",
        "fieldId": "bba1f6b1-2175-4106-a602-8e878fd48245"
    }
    result = await submission_field_insert(SchemaExecutor, CreateMutation, insert_data)
    inserted = assert_insert(result)
    result = await submission_field_delete(SchemaExecutor, CreateMutation, inserted)
    deleted = assert_delete

@pytest.mark.asyncio
async def test_submission_field_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Submission",
        "submissionId": "b0f1a7da-9f58-4e9d-bdc1-19d94770b20b",
        "sectionId": "dc4eb08a-7a80-4834-9021-c759c94a5d50",
        "fieldId": "bba1f6b1-2175-4106-a602-8e878fd48245"
    }
    result = await submission_field_insert(SchemaExecutor, CreateMutation, insert_data)
    submission_field_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **submission_field_inserted
    }
    result = await submission_field_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

@pytest.mark.asyncio
async def test_submission_field_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Submission",
        "submissionId": "b0f1a7da-9f58-4e9d-bdc1-19d94770b20b",
        "sectionId": "dc4eb08a-7a80-4834-9021-c759c94a5d50",
        "fieldId": "bba1f6b1-2175-4106-a602-8e878fd48245",
        "value": "LL"
    }
    update_data = {
        "value": "LLC"
    }
    result = await submission_field_insert(SchemaExecutor, CreateMutation, insert_data)
    submission_field_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **submission_field_inserted,
        **update_data
    }
    result = await submission_field_update(SchemaExecutor, CreateMutation, payload)
    submission_field_updated = assert_update(result)
    updated = assert_same(update_data, submission_field_updated)
    result = await submission_field_delete(SchemaExecutor, CreateMutation, updated)
    deleted = assert_delete

