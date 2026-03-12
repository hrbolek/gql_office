import asyncio
import logging
import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def ContextBase():
    # async_session_maker
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    from src.DBDefinitions import BaseModel
    from uoishelpers.dataloaders.IDLoader import set_GLOBAL_ASYNCIO_LOCK
    GLOBAL_ASYNCIO_LOCK = asyncio.Lock()
    set_GLOBAL_ASYNCIO_LOCK(GLOBAL_ASYNCIO_LOCK)
    from uoishelpers.dataloaders.IDLoader import GLOBAL_ASYNCIO_LOCK as lock
    assert lock == GLOBAL_ASYNCIO_LOCK, "GLOBAL_ASYNCIO_LOCK is not the same as lock in IDLoader"

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    # fill data
    # patch DEMODATA to True
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("DEMODATA", "True")

    from src.DBFeeder import initDB
    await initDB(asyncSessionMaker=async_session_maker, filename="./systemdata.test.json")
    # context
    from src.Dataloaders import createLoadersContext
    
    class Request:
        @property
        def cookies(self):
            return {}
        @property
        def headers(self):
            return {}
    async with async_session_maker() as session:
        loadersContext = createLoadersContext(session=session)
        logging.info(f"ContextBase created with session: {session}")
        yield {
            **loadersContext, 
            "request": Request(),
        }
        await session.commit()
        logging.info(f"ContextBase teardown with session: {session}")
    await asyncEngine.dispose()

@pytest.fixture
def UserPatch():
    local_roles = [
        {"roletype": {"name": "administrátor"}, "valid": True},
        {"roletype": {"name": "editor"}, "valid": True},
    ]
    def exec(roles: list = None):
        nonlocal local_roles
        local_roles = roles or []
    
    
    class PseudoLoader:
        async def load(self, params):
            # mock response for user roles query
            # logging.info(f"userRolesForRBACQuery_loader called with params: {params}")
            return {
                "result": local_roles
            }    
    return exec, PseudoLoader()

@pytest_asyncio.fixture
async def FullContext(ContextBase, UserPatch):
    
    loadersContext = ContextBase
    userRolesForRBACQuery_patch, userRolesForRBACQuery_loader = UserPatch
    context_ = {
        **loadersContext,
        "userRolesForRBACQuery_loader": userRolesForRBACQuery_loader,
        "userRolesForRBACQuery_patch": userRolesForRBACQuery_patch
    }
    return context_

@pytest.fixture
def WhoAmIExtensionOverride(FullContext):
    from uoishelpers.schema import WhoAmIExtension
    class WhoAmIExtension_Debug(WhoAmIExtension):
        user = None
        async def on_execute(self):
            user = self.__class__.user or {
                "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
                "roles": [{
                    "roletype": {"name": "superadmin"}
                }]
            }

            self.execution_context.context["user"] = user
            yield

        @classmethod
        def set_user(cls, user):
            cls.user = user

        
    return WhoAmIExtension_Debug


@pytest.fixture
def RolePermissionSchemaExtensionOverride(FullContext):
    from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import RolePermissionSchemaExtension
    class RolePermissionSchemaExtension_Debug(RolePermissionSchemaExtension):
        response_override = None

        async def load(self, key):
            response = self.__class__.response_override
            if response is None:
                response = {
                    "result": self.execution_context.context["user"].get("roles", [])
                }
            return response

        async def on_execute(self):
            self.execution_context.context["userRolesForRBACQuery_loader"] = self
            yield

        @classmethod
        def set_response(cls, response):
            cls.response_override = response

    return RolePermissionSchemaExtension_Debug

@pytest.fixture
def SchemaExecutor(
    FullContext,
    WhoAmIExtensionOverride,
    RolePermissionSchemaExtensionOverride
):
    # GQLUG_ENDPOINT_URL
    # monkeypatch = pytest.MonkeyPatch()
    # monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8125/gql")

    from uoishelpers.schema import WhoAmIExtension
    # schema.extensions.append(WhoAmIExtension)
    from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import RolePermissionSchemaExtension


    from src.GraphTypeDefinitions import schema
    schema.extensions = list(
        filter(lambda ex: ex not in [WhoAmIExtension, RolePermissionSchemaExtension], schema.extensions)
    )
    
    schema.extensions.append(WhoAmIExtensionOverride)
    schema.extensions.append(RolePermissionSchemaExtensionOverride)

    for ext in schema.extensions:
        logging.info(f"Schema extension: {ext}")
    FullContext["user"] = {
        "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
        "roles": [{
            "roletype": {"name": "superadmin"}
        }]
    }
    async def Execute(query, variable_values={}):
        result = await schema.execute(query=query, variable_values=variable_values, context_value=FullContext)
        value = {"data": result.data} 
        if result.errors:
            value["errors"] = result.errors
        return value
    return Execute