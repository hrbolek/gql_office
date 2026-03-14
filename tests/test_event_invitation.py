import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same


async def event_invitation_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventInvitationInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_invitation_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventInvitationUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_invitation_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventInvitationDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_invitation_accept_decline(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventInvitationAcceptDecline")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

from .test_events import event_insert, event_delete

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
                "name": "plánovací administrátor"
            }
        }
    ]
}

async def Event(SchemaExecutor, CreateMutation, item={"name": "test"}):
    result = await event_insert(SchemaExecutor, CreateMutation, item)
    event = assert_insert(result)
    yield event
    result = await event_delete(SchemaExecutor, CreateMutation, event)
    assert_delete(result)

async def Event_Invitation(SchemaExecutor, CreateMutation):
    async with Event(SchemaExecutor, CreateMutation) as event:
        result = await event_invitation_insert(SchemaExecutor, CreateMutation, {"eventId": event["id"]})
        event_invitation = assert_insert(result)
        yield event_invitation
        result = await event_invitation_delete(SchemaExecutor, CreateMutation, event_invitation)
        assert_delete(result)
    pass

@pytest.mark.asyncio
async def test_event_invitation_insert(
    SchemaExecutor, 
    CreateMutation, 
    WhoAmIExtensionOverride, 
    RolePermissionSchemaExtensionOverride
):
    
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    input = {
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "userId": default_user["id"],
        "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0" # organizer
    }
    result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)
    inserted = assert_insert(result)


    result = await event_invitation_delete(SchemaExecutor, CreateMutation, inserted)
    assert_delete(result)

# @pytest.mark.asyncio
# async def test_event_invitation_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
#     WhoAmIExtensionOverride.set_user(default_user)
#     RolePermissionSchemaExtensionOverride.set_response(default_roles)
#     # user is organizer
#     input = {
#         "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
#         "userId": default_user["id"],
#         "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0" # organizer
#     }
#     delta = {
#         "stateId": "7d6766f5-0ddb-4fce-92ca-db82a5311bdb"
#     }

#     result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)

#     # another invitation
#     input = {
#         "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
#         "userId": "ccb397ad-0de7-46e7-bff0-42452f11dd5e",
#         "stateId": "1b890c48-dd22-4a9c-a012-7075dbbb1926"
#     }
    
#     result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)
#     event_invitation_inserted = assert_insert(result)
    
#     # change state of another invitation
#     delta = {
#         "stateId": "7d6766f5-0ddb-4fce-92ca-db82a5311bdb"
#     }
#     payload = {
#         **input,
#         **event_invitation_inserted,
#         **delta
#     }
#     result = await event_invitation_update(SchemaExecutor, CreateMutation, payload)
#     event_invitation_updated = assert_update(result)
#     updated = assert_same(delta, event_invitation_updated)
#     result = await event_invitation_delete(SchemaExecutor, CreateMutation, updated)
#     assert_delete(result)    

@pytest.mark.asyncio
async def test_event_invitation_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)
    # user is organizer
    input = {
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "userId": default_user["id"],
        "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0"
    }
    delta = {
        "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0"
    }

    result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)
    event_invitation_inserted = assert_insert(result)
   
    payload = {
        **input,
        **event_invitation_inserted,
        **delta
    }
    result = await event_invitation_update(SchemaExecutor, CreateMutation, payload)
    event_invitation_updated = assert_update(result)
    assert_same(delta, event_invitation_updated)

    result = await event_invitation_delete(SchemaExecutor, CreateMutation, event_invitation_updated)
    assert_delete(result)


@pytest.mark.asyncio
async def test_event_invitation_accept(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)
    # user is organizer
    input = {
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "userId": default_user["id"],
        "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0"
    }
    result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)
    event_invitation_inserted_organizer = assert_insert(result)
    # organizer inserted

    # invitation
    invited_user_id = "ef22149f-8041-4de0-bcbb-cf1c952fba30"
    input = {
        "eventId": "d3f68d57-90f8-43a8-a29f-327eb18231bf",
        "userId": invited_user_id,
        "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0"
    }
    result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)
    event_invitation_inserted_invited = assert_insert(result)

    WhoAmIExtensionOverride.set_user({
        **default_user,
        "id": invited_user_id
    })

    # invitation accept
    delta_accept = {
        "stateId": "7d2ef223-b60e-4e6d-b7d5-5fdc1f8e2ec2"
    }
    payload = {
        **input,
        **event_invitation_inserted_invited,
        **delta_accept
    }
    result = await event_invitation_accept_decline(SchemaExecutor, CreateMutation, payload)
    event_invitation_updated = assert_update(result)
    assert_same(delta_accept, event_invitation_updated)

    WhoAmIExtensionOverride.set_user(default_user)
    # odstranit invitation
    result = await event_invitation_delete(SchemaExecutor, CreateMutation, event_invitation_updated)
    assert_delete(result)

    # odstranit organizer
    result = await event_invitation_delete(SchemaExecutor, CreateMutation, event_invitation_inserted_organizer)
    assert_delete(result)


@pytest.mark.asyncio
async def test_event_invitation_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(default_user)
    RolePermissionSchemaExtensionOverride.set_response(default_roles)

    input = {
        "eventId": "e75568c8-3bcc-43f1-afd0-5c785cc40c9f",
        "userId": default_user["id"],
        "stateId": "3265a488-bbfa-4c59-946c-7a7b059ee4f0"
    }
    result = await event_invitation_insert(SchemaExecutor, CreateMutation, input)
    event_invitation_inserted = assert_insert(result)
    payload = {
        **input,
        **event_invitation_inserted
    }
    result = await event_invitation_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)

# @pytest.mark.asyncio
# async def test_event_query(CreateMutation):
#     query = CreateMutation("eventInsert")
#     logging.info(f"{query}")
#     assert False