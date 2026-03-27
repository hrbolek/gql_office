import asyncio
import uuid
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs2,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType

from src.GraphTypeDefinitions.Domain_UG.StateGQLModel import StateGQLModel
from src.GraphTypeDefinitions.Domain_UG.RoletTypeGQLModel import RoletTypeGQLModel

DigitalFormFieldGQLModel = typing.Annotated["DigitalFormFieldGQLModel", strawberry.lazy(".DigitalFormFieldGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Represents a permission for the field in a digital form."""
)
class DigitalFormFieldPermissionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalFormFieldPermissionModel


    form_field_id: typing.Optional[IDType] = strawberry.field(description="ID of the form field this permission applies to.", default=None)
    state_id: typing.Optional[IDType] = strawberry.field(description="ID of the state this permission applies to.", default=None)
    role_type_id: typing.Optional[IDType] = strawberry.field(description="ID of the role type this permission applies to.", default=None)
    operation_id: typing.Optional[IDType] = strawberry.field(description="ID of the operation this permission allows.", default=None)

    form_field: typing.Optional["DigitalFormFieldGQLModel"] = strawberry.field(
        description="The form field this permission applies to.",       
        resolver=ScalarResolver["DigitalFormFieldGQLModel"](fkey_field_name="form_id")
    )

    state: typing.Optional["StateGQLModel"] = strawberry.field(
        description="The state this permission applies to.",
        resolver=ScalarResolver["StateGQLModel"](fkey_field_name="state_id")
    )

    role_type: typing.Optional["RoletTypeGQLModel"] = strawberry.field(
        description="The role type this permission applies to.",
        resolver=ScalarResolver["RoletTypeGQLModel"](fkey_field_name="role_type_id")
    )