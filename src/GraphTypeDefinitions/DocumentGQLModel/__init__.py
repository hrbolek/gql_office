import strawberry

from .ElectronicDocumentGQLModel import ElectronicDocumentGQLModel, DocumentQuery, DocumentMutation
from .DigitalDocumentGQLModel import (
    DigitalFormGQLModel, DigitalFormQuery, DigitalFormMutation,
    DigitalFormSectionGQLModel, DigitalFormSectionQuery, DigitalFormSectionMutation,
    DigitalFormSubmissionQuery, DigitalFormSubmissionMutation
)

from .DocumentTypeGQLModel import DocumentTypeGQLModel


from .DocumentGQLModel import DocumentGQLModel