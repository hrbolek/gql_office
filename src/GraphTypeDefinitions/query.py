
import strawberry

from .FacilityGQLModel import (
    FacilityQuery,
    FacilityTypeQuery
)
from .DocumentGQLModel import ElectronicDocumentGQLModel, DocumentQuery
from .DocumentGQLModel import (
    DigitalDocumentGQLModel, DigitalFormQuery,
    DigitalFormSectionGQLModel, DigitalFormSectionQuery, 
    DigitalFormSubmissionQuery, DigitalFormSubmissionMutation
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

    DocumentQuery, 
    DigitalFormQuery,
    DigitalFormSectionQuery,

    DigitalFormSubmissionQuery
):

    pass
