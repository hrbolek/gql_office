
import strawberry

from .FacilityGQLModel import (
    FacilityQuery,
    FacilityTypeQuery
)
from .DocumentGQLModel import ElectronicDocumentGQLModel, ElectronicDocumentQuery
from .DocumentGQLModel import (
    DigitalDocumentGQLModel, DigitalFormQuery,
    DigitalFormSectionGQLModel, DigitalFormSectionQuery, 
    DigitalSubmissionQuery, DigitalSubmissionMutation,
    DocumentQuery
)

from .EventGQLModel import (
    EventQuery,
    EventTypeQuery,
    EventInvitationQuery
)

@strawberry.type(description="""Type for query root""")
class Query(
    EventQuery, 
    EventTypeQuery,
    EventInvitationQuery,

    FacilityQuery, 
    FacilityTypeQuery,

    ElectronicDocumentQuery, 
    DigitalFormQuery,
    DigitalFormSectionQuery,

    DigitalSubmissionQuery,
    DocumentQuery
):

    pass
