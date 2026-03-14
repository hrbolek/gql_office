
import strawberry

from .FacilityGQLModel import (
    FacilityQuery,
    FacilityTypeQuery
)
from .DocumentGQLModel import ElectronicDocumentGQLModel, ElectronicDocumentQuery
from .DocumentGQLModel import (
    DigitalDocumentGQLModel, DigitalFormQuery,
    DigitalFormSectionGQLModel, DigitalFormSectionQuery, 
    DigitalFormFieldQuery,
    DigitalSubmissionQuery, DigitalSubmissionMutation,
    SubmissionSectionQuery,
    SubmissionFieldQuery,
    DocumentQuery
)

from .EventGQLModel import (
    EventQuery,
    EventTypeQuery,
    EventInvitationQuery,
    EventFacilityReservationQuery
)

from .RequestGQLModel import RequestQueries, RequestTypeQueries, HistoryQueries

@strawberry.type(description="""Type for query root""")
class Query(
    EventQuery, 
    EventTypeQuery,
    EventInvitationQuery,
    EventFacilityReservationQuery,

    FacilityQuery, 
    FacilityTypeQuery,

    ElectronicDocumentQuery, 
    DigitalFormQuery,
    DigitalFormSectionQuery,
    DigitalFormFieldQuery,

    DigitalSubmissionQuery,
    
    SubmissionSectionQuery,
    SubmissionFieldQuery,

    DocumentQuery,

    RequestQueries, 
    RequestTypeQueries, 
    HistoryQueries
):

    pass
