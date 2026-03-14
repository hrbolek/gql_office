import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

async def facility_insert(SchemaExecutor, CreateMutation, facility):
    query = CreateMutation("facilityInsert")
    variable_values = {**facility}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def facility_update(SchemaExecutor, CreateMutation, facility):
    query = CreateMutation("facilityUpdate")
    variable_values = {**facility}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result

async def facility_delete(SchemaExecutor, CreateMutation, facility):
    query = CreateMutation("facilityDelete")
    variable_values = {**facility}
    result = await SchemaExecutor(query=query, variable_values=variable_values)
    return result


@pytest.mark.asyncio
async def test_facility_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
                        "name": "nemovitostní administrátor"
                    }
                }
            ]
        }
    )

    facility = {
        "masterFacilityId": "d5f66675-11DB-4c65-9f11-bfe4e3cc25e2",
        "name": "Test Facility",
    }
    result = await facility_insert(SchemaExecutor, CreateMutation, facility)
    assert_insert(result)

@pytest.mark.asyncio
async def test_facility_update(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    RolePermissionSchemaExtensionOverride.set_response(
        {
            "result": [
                {
                    "roletype": {
                        "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                        "name": "nemovitostní administrátor"
                    }
                }
            ]
        }
    )

    facility = {
        # "id": "63902412-1443-4038-8619-6b9c32ebb7c3",
        "masterFacilityId": "d5f66675-11DB-4c65-9f11-bfe4e3cc25e2",
        "name": "Test Facility",
    }
    delta = {
        "name": "Updated Test Facility",
    }
    result = await facility_insert(SchemaExecutor, CreateMutation, facility)
    facility_inserted = assert_insert(result)
    payload = {
        **facility,
        **facility_inserted,
        **delta
    }
    result = await facility_update(SchemaExecutor, CreateMutation, payload)
    facility_updated = assert_update(result)
    assert_same(delta, facility_updated)

@pytest.mark.asyncio
async def test_facility_delete(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    RolePermissionSchemaExtensionOverride.set_response(
        {
            "result": [
                {
                    "roletype": {
                        "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                        "name": "nemovitostní administrátor"
                    }
                }
            ]
        }
    )

    facility = {
        "masterFacilityId": "d5f66675-11DB-4c65-9f11-bfe4e3cc25e2",
        "name": "Test Facility",
    }
    result = await facility_insert(SchemaExecutor, CreateMutation, facility)
    facility_inserted = assert_insert(result)
    payload = {
        **facility,
        **facility_inserted
    }
    result = await facility_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)