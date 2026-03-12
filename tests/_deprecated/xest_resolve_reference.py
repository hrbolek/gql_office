from .utils import createResolveTest
from src.GraphTypeDefinitions import schema

test_resolve_reference = createResolveTest(
    schema=schema,
    types={
        "StateGQLModel": [
            "5d36bb38-b29d-44e8-893d-b5e5a3b2591f"   
        ]
    })