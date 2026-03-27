import datetime
import strawberry

import strawberry.extensions
from strawberry.schema.config import StrawberryConfig
from uoishelpers.gqlpermissions import RBACObjectGQLModel
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .BaseGQLModel import BaseGQLModel
from .Domain_UG.UserGQLModel import UserGQLModel
from .Domain_UG.GroupGQLModel import GroupGQLModel
from .Domain_UG.StateGQLModel import StateGQLModel


###########################################################################################################################
# 
# Custom scalar
# https://strawberry.rocks/docs/types/scalars#custom-scalars
# 
###########################################################################################################################

# timedelta = strawberry.scalar(
#     # NewType("TimeDelta", float),
#     datetime.timedelta,
#     name="timedelta",
#     serialize=lambda v: v.total_seconds() / 60,
#     parse_value=lambda v: datetime.timedelta(minutes=v),
# )

# @strawberry.scalar(
#     name="timedelta",
#     serialize=lambda v: v.total_seconds() / 60,
#     parse_value=lambda v: datetime.timedelta(minutes=v),
# )
# class TimeDelta:
#     pass

from .BaseGQLModel import Relation
# from .query import Query
# from .mutation import Mutation

from .Domain_Office import Query_Domain_Office, Mutation_Domain_Office
@strawberry.type(description="""Type for query root""")
class Query(
    Query_Domain_Office
):
    pass

@strawberry.type(description="""Type for query root""")
class Mutation(
    Mutation_Domain_Office
):
    pass

schema = strawberry.federation.Schema(
    query=Query, 
    mutation=Mutation, 
    types=(UserGQLModel, GroupGQLModel, RBACObjectGQLModel, BaseGQLModel, StateGQLModel), 
    config=StrawberryConfig(
        scalar_map={
            datetime.timedelta: strawberry.scalar(
                name="timedelta",
                serialize=lambda v: v.total_seconds() / 60,
                parse_value=lambda v: datetime.timedelta(minutes=v),
            ),
        }
    ),

    extensions=[],
    schema_directives=[Relation]
)

from uoishelpers.schema import WhoAmIExtension, ProfilingExtension, PrometheusExtension
schema.extensions.append(WhoAmIExtension)
# schema.extensions.append(ProfilingExtension())        
# schema.extensions.append(PyInstrument())
# schema.extensions.append(PrometheusExtension(prefix="gql_facilities"))

from uoishelpers.gqlpermissions.RolePermissionSchemaExtension import RolePermissionSchemaExtension, GraphQLBatchLoader
schema.extensions.append(RolePermissionSchemaExtension)

from strawberry.extensions import ParserCache, ValidationCache

# from uoishelpers.schema.PyInstrumentHtmlExtension import PyInstrumentHtmlExtension
# schema.extensions.append(PyInstrumentHtmlExtension(enabled=True))
schema.extensions.append(ParserCache(1000))
schema.extensions.append(ValidationCache(1000))

# from aiodataloader import DataLoader
# import uuid


# def getCacheKey(struct):
#     return struct["id"]

# class RBACLoader(DataLoader):
#     def __init__(self, gqlclient):
#         self.index = {}
#         self.gqlclient = gqlclient
#         super().__init__(
#             get_cache_key=getCacheKey
#         )

#     async def batch_load_fn(self, structlist):
#         index = {
#             f'h{uuid.uuid4().hex}': item
#             for item in structlist
#         }
#         lines = [
#             f'{key}: rbacById(id: "{value["id"]}")'
#             '{'
#             f'judgement: userCanWithoutState(rolesNeeded: {value["roles"]})'
#             '}'
#             for key, value in index
#         ]
#         query = '{' + "\n".join(lines) + '}'
#         gqlclient = self.gqlclient
#         response = await gqlclient(query=query)
#         assert "data" in response, f"get bad response while asking for RBAC {response}"
#         responsedata = response["data"]
#         result = [
#             responsedata[key]["judgement"]
#             for key in index.keys()
#         ]
#         return result

# class RBACExtension(WhoAmIExtension):
#     async def on_execute(self):
#         self.execution_context.context["RBACLoader"] = RBACLoader(gqlclient=self.ug_query)

#         # print("->on_execute", self.execution_context.query, flush=True)
#         yield
#         # print("on_execute->", whoami, flush=True)
