import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same


async def event_facility_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventFacilityInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_facility_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventFacilityUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_facility_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventFacilityDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_event_facility_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
                        "name": "nemovitostní administrátor"
                    }
                }
            ]
        }
    )

    input = {
        "name": "Test Event",
        "facilityId": "d5f66675-11db-4c65-9f11-bfe4e3cc25e2",
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "stateId": "1b890c48-dd22-4a9c-a012-7075dbbb1926"
    }
    result = await event_facility_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_event_facility_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
                        "name": "nemovitostní administrátor"
                    }
                }
            ]
        }
    )

    input = {
        "name": "Test Event",
        "facilityId": "d5f66675-11db-4c65-9f11-bfe4e3cc25e2",
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "stateId": "1b890c48-dd22-4a9c-a012-7075dbbb1926"
    }
    delta = {
        "stateId": "7d6766f5-0ddb-4fce-92ca-db82a5311bdb"
    }
    result = await event_facility_insert(SchemaExecutor, CreateMutation, input)
    event_facility_inserted = assert_insert(result)
    payload = {
        **input,
        **event_facility_inserted,
        **delta
    }
    result = await event_facility_update(SchemaExecutor, CreateMutation, payload)
    event_facility_updated = assert_update(result)
    assert_same(delta, event_facility_updated)

@pytest.mark.asyncio
async def test_event_facility_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
                        "name": "nemovitostní administrátor"
                    }
                }
            ]
        }
    )

    input = {
        "name": "Test Event",
        "facilityId": "d5f66675-11db-4c65-9f11-bfe4e3cc25e2",
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "stateId": "1b890c48-dd22-4a9c-a012-7075dbbb1926"
    }
    result = await event_facility_insert(SchemaExecutor, CreateMutation, input)
    event_facility_inserted = assert_insert(result)
    payload = {
        **input,
        **event_facility_inserted
    }
    result = await event_facility_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

# @pytest.mark.asyncio
# async def test_event_query(CreateMutation):
#     query = CreateMutation("eventInsert")
#     logging.info(f"{query}")
#     assert False