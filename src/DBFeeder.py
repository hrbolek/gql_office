import os

from functools import cache
from uoishelpers.feeders import ImportModels
from uoishelpers.dataloaders import readJsonFile

from src.DBDefinitions import (
    EventModel, 
    EventTypeModel, 
    DigitalFormFieldModel,
    DigitalFormModel,
    DigitalFormSectionModel,
    DigitalSubmissionFieldModel,
    DigitalSubmissionSectionModel,
    DigitalSubmissionModel,
    DocumentModel,
    DocumentTypeModel,
    ElectronicDocumentModel,
    FacilityModel,
    FacilityTypeModel,
    EventFacilityReservationModel,
    EventInvitationModel    
)

get_demodata = lambda :readJsonFile(jsonFileName="./systemdata.json")
async def initDB(asyncSessionMaker, filename="./systemdata.json"):

    isDemo = os.environ.get("DEMODATA", None) in ["True", "true"]
    if isDemo:
        print("Demo mode", flush=True)
        dbModels = [
            EventTypeModel, 
            EventModel, 

            DocumentTypeModel,
            FacilityTypeModel,

            DigitalFormModel,
            DigitalFormFieldModel,
            DigitalFormSectionModel,

            DigitalSubmissionModel,
            DigitalSubmissionSectionModel,
            DigitalSubmissionFieldModel,

            ElectronicDocumentModel,

            FacilityModel,
            EventFacilityReservationModel,
            EventInvitationModel    
        ]
    else:

        print("No Demo mode", flush=True)
        dbModels = [
            EventTypeModel, 

            DocumentTypeModel,
            FacilityTypeModel,

        ]

    jsonData = readJsonFile(filename)
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    
    print("Data initialized", flush=True)