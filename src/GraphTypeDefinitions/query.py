
import strawberry

from .EventGQLModel import EventGQLModel, EventQueries
from .FacilityGQLModel import FacilityGQLModel, FacilityQueries


@strawberry.type(description="""Type for query root""")
class Query(EventQueries, FacilityQueries):

    pass
