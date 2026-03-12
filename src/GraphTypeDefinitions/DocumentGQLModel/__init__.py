import strawberry

from .ElectronicDocumentGQLModel import ElectronicDocumentGQLModel, ElectronicDocumentQuery, DocumentMutation
from .DigitalDocumentGQLModel import (
    DigitalFormGQLModel, DigitalFormQuery, DigitalFormMutation,
    DigitalFormSectionGQLModel, DigitalFormSectionQuery, DigitalFormSectionMutation,
    DigitalFormFieldQuery, DigitalFormFieldMutations,
    
    DigitalSubmissionQuery, DigitalSubmissionMutation,
    SubmissionSectionQuery, SubmissionSectionMutation,
    SubmissionFieldQuery, DigitalSubmissionFieldMutation
)
from .DocumentGQLModel import DocumentQuery

from .DocumentTypeGQLModel import DocumentTypeGQLModel


from .DocumentInterfaceGQLModel import DocumentInterfaceGQLModel