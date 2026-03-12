import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same


async def facility_type_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("facilityTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def facility_type_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("facilityTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def facility_type_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("facilityTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_facility_type_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await facility_type_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_facility_type_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await facility_type_insert(SchemaExecutor, CreateMutation, input)
    facility_type_inserted = assert_insert(result)
    payload = {
        **input,
        **facility_type_inserted,
        **delta
    }
    result = await facility_type_update(SchemaExecutor, CreateMutation, payload)
    facility_type_updated = assert_update(result)
    assert_same(delta, facility_type_updated)

@pytest.mark.asyncio
async def test_facility_type_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await facility_type_insert(SchemaExecutor, CreateMutation, input)
    facility_type_inserted = assert_insert(result)
    payload = {
        **input,
        **facility_type_inserted
    }
    result = await facility_type_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

# @pytest.mark.asyncio
# async def test_facility_query(CreateMutation):
#     query = CreateMutation("facilityInsert")
#     logging.info(f"{query}")
#     assert False