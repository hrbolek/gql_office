import logging
import pytest
from src.GraphTypeDefinitions import schema

from .utils_sdl_2 import createTests

# logging.info("starting tests")
tests  = createTests(schema)
# logging.info(f"{tests.keys()}")
# logging.info("tests finished")

import sys
module = sys.modules[__name__]

for funcname, func in tests.items():
    setattr(module, funcname, func)    

@pytest.mark.asyncio
async def test_connection_string():
    from src.DBDefinitions import ComposeConnectionString
    connectionstring = ComposeConnectionString()
    assert connectionstring is not None, "Connection string is None"

@pytest.mark.asyncio
async def test_engine():
    connectionstring = "sqlite+aiosqlite:///:memory:"
    from src.DBDefinitions import startEngine
    sessionMaker = await startEngine(connectionstring, makeDrop=True, makeUp=True)
    assert sessionMaker is not None, "SessionMaker is None"
    
