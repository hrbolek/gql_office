# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseModel
from ..DBDefinitions import (
    DigitalFormFieldModel,
    DigitalFormModel,
    DigitalFormSectionModel,
    DigitalSubmissionFieldModel,
    DigitalSubmissionSectionModel,
    DigitalSubmissionModel,
    DocumentModel,
    DocumentTypeModel,
    ElectronicDocumentModel,
    EventModel,
    EventTypeModel,
    FacilityModel,
    FacilityTypeModel,
    EventFacilityReservationModel,
    EventInvitationModel,
    HistoryModel,
    RequestModel,
    RequestTypeModel
)

# def createLoaders(asyncSessionMaker):

#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)

#     attrs = {}

#     for DBModel in BaseModel.registry.mappers:
#         cls = DBModel.class_
#         attrs[cls.__tablename__] = property(cache(createLambda(asyncSessionMaker, cls)))
#         attrs[cls.__name__] = attrs[cls.__tablename__]
#     # attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

# def createLoadersContext(asyncSessionMaker):
#     return {
#         "loaders": createLoaders(asyncSessionMaker)
#     }

from uoishelpers.dataloaders import createIdLoader
from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
from functools import cache
import src.DBDefinitions

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel

    DigitalFormFieldModel: IDLoader[src.DBDefinitions.DigitalFormFieldModel] = None
    DigitalFormModel: IDLoader[src.DBDefinitions.DigitalFormModel] = None
    DigitalFormSectionModel: IDLoader[src.DBDefinitions.DigitalFormSectionModel] = None
    DigitalSubmissionFieldModel: IDLoader[src.DBDefinitions.DigitalSubmissionFieldModel] = None
    DigitalSubmissionSectionModel: IDLoader[src.DBDefinitions.DigitalSubmissionSectionModel] = None
    DigitalSubmissionModel: IDLoader[src.DBDefinitions.DigitalSubmissionModel] = None
    DocumentModel: IDLoader[src.DBDefinitions.DocumentModel] = None
    DocumentTypeModel: IDLoader[src.DBDefinitions.DocumentTypeModel] = None
    ElectronicDocumentModel: IDLoader[src.DBDefinitions.ElectronicDocumentModel] = None
    EventModel: IDLoader[src.DBDefinitions.EventModel] = None
    EventTypeModel: IDLoader[src.DBDefinitions.EventTypeModel] = None
    FacilityModel: IDLoader[src.DBDefinitions.FacilityModel] = None
    FacilityTypeModel: IDLoader[src.DBDefinitions.FacilityTypeModel] = None
    EventFacilityReservationModel: IDLoader[src.DBDefinitions.EventFacilityReservationModel] = None
    EventInvitationModel: IDLoader[src.DBDefinitions.EventInvitationModel] = None
    HistoryModel: IDLoader[src.DBDefinitions.HistoryModel] = None
    RequestModel: IDLoader[src.DBDefinitions.RequestModel] = None
    RequestTypeModel: IDLoader[src.DBDefinitions.RequestTypeModel] = None


    def __init__(self, session):
        super().__init__(session)

        self.DigitalFormFieldModel = self.get(DigitalFormFieldModel)
        self.DigitalFormModel = self.get(DigitalFormModel)
        self.DigitalFormSectionModel = self.get(DigitalFormSectionModel)
        self.DigitalSubmissionFieldModel = self.get(DigitalSubmissionFieldModel)
        self.DigitalSubmissionSectionModel = self.get(DigitalSubmissionSectionModel)
        self.DigitalSubmissionModel = self.get(DigitalSubmissionModel)
        self.DocumentModel = self.get(DocumentModel)
        self.DocumentTypeModel = self.get(DocumentTypeModel)
        self.ElectronicDocumentModel = self.get(ElectronicDocumentModel)
        self.EventModel = self.get(EventModel)
        self.EventTypeModel = self.get(EventTypeModel)
        self.FacilityModel = self.get(FacilityModel)
        self.FacilityTypeModel = self.get(FacilityTypeModel)
        self.EventFacilityReservationModel = self.get(EventFacilityReservationModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.HistoryModel = self.get(HistoryModel)
        self.RequestModel = self.get(RequestModel)
        self.RequestTypeModel = self.get(RequestTypeModel)

        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
