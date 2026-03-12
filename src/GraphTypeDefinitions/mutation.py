import strawberry

from .EventGQLModel import (
    EventMutation,
    EventTypeMutation,
    EventInvitationMutation
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

@strawberry.type(description="root of mutations")
class Mutation(
    EventMutation,
    EventTypeMutation,
    EventInvitationMutation,
    
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

    # from .FacilityGQLModel import (
    #     facility_insert,
    #     facility_update,
    #     facility_delete,
    # )

    # from .FacilityEventGQLModel import (
    #     facility_reservation_create,
    #     facility_reservation_update,
    #     facility_reservation_delete
    # )

    # from .FacilityTypeGQLModel import (
    #     facility_type_insert,
    #     facility_type_update,
    #     facility_type_delete
    # )
    pass