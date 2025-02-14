
import strawberry

from .EventGQLModel import EventGQLModel, EventQueries
from .FacilityGQLModel import FacilityGQLModel, FacilityQueries
from .DocumentGQLModel import DocumentGQLModel, DocumentQueries

@strawberry.type(description="""Type for query root""")
class Query(EventQueries, FacilityQueries, DocumentQueries):

    pass
