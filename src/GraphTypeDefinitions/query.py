
import strawberry

from .EventGQLModel import EventGQLModel, EventQuery
from .FacilityGQLModel import FacilityGQLModel, FacilityQuery
from .DocumentGQLModel import ElectronicDocumentGQLModel, DocumentQuery
from .DocumentGQLModel import DigitalDocumentGQLModel, DigitalFormQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, FacilityQuery, DocumentQuery, DigitalFormQuery):

    pass
