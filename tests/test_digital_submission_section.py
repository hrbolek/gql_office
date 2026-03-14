import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def submission_section_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("submissionSectionInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def submission_section_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("submissionSectionUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def submission_section_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("submissionSectionDelete")
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
async def test_submission_section_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Submission",
        "submissionId": "b0f1a7da-9f58-4e9d-bdc1-19d94770b20b",
        "sectionId": "dc4eb08a-7a80-4834-9021-c759c94a5d50",
        "formSectionId": "e8c28ee1-3504-4bd5-90c6-0d0f1b7fc3ef"
    }
    result = await submission_section_insert(SchemaExecutor, CreateMutation, insert_data)
    inserted = assert_insert(result)
    result = await submission_section_delete(SchemaExecutor, CreateMutation, inserted)
    deleted = assert_delete

@pytest.mark.asyncio
async def test_submission_section_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Submission",
        "submissionId": "b0f1a7da-9f58-4e9d-bdc1-19d94770b20b",
        "sectionId": "dc4eb08a-7a80-4834-9021-c759c94a5d50",
        "formSectionId": "e8c28ee1-3504-4bd5-90c6-0d0f1b7fc3ef"
    }
    result = await submission_section_insert(SchemaExecutor, CreateMutation, insert_data)
    submission_section_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **submission_section_inserted
    }
    result = await submission_section_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

@pytest.mark.asyncio
async def test_submission_section_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    insert_data = {
        "name": "Test Submission",
        "submissionId": "b0f1a7da-9f58-4e9d-bdc1-19d94770b20b",
        "sectionId": "dc4eb08a-7a80-4834-9021-c759c94a5d50",
        "formSectionId": "e8c28ee1-3504-4bd5-90c6-0d0f1b7fc3ef",
        "index": 0
    }
    update_data = {
        "index": 1
    }
    result = await submission_section_insert(SchemaExecutor, CreateMutation, insert_data)
    submission_section_inserted = assert_insert(result)
    payload = {
        **insert_data,
        **submission_section_inserted,
        **update_data
    }
    result = await submission_section_update(SchemaExecutor, CreateMutation, payload)
    submission_section_updated = assert_update(result)
    updated = assert_same(update_data, submission_section_updated)
    result = await submission_section_delete(SchemaExecutor, CreateMutation, updated)
    deleted = assert_delete

