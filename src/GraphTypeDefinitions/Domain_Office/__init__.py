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

from .EventGQLModel import (
    EventMutation,
    EventTypeMutation,
    EventInvitationMutation,
    EventFacilityReservationMutation
)

from .FacilityGQLModel import (
    FacilityMutation,
    FacilityTypeMutation
)

from .DocumentGQLModel import (
    DocumentMutation,
    DigitalFormMutation,
    DigitalFormSectionMutation,
    DigitalFormFieldMutations,

    DigitalSubmissionMutation,
    SubmissionSectionMutation,
    DigitalSubmissionFieldMutation
)

from .RequestGQLModel import RequestMutations, RequestTypeMutations, HistoryMutations

@strawberry.interface(
    description="Domain Office Queries"
)
class Query_Domain_Office(
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

@strawberry.interface(
    description="Domain Office Mutations"
)
class Mutation_Domain_Office(
    EventMutation,
    EventTypeMutation,
    EventInvitationMutation,
    EventFacilityReservationMutation,
    
    FacilityMutation,
    FacilityTypeMutation,

    # DocumentMutation,
    DigitalFormMutation,
    DigitalFormSectionMutation,
    DigitalFormFieldMutations,
    DigitalSubmissionMutation,
    DigitalSubmissionFieldMutation,
    SubmissionSectionMutation,

    RequestMutations, 
    RequestTypeMutations, 
    HistoryMutations
):
    pass