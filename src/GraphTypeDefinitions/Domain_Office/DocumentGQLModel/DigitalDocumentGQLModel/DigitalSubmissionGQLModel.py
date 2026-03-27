import uuid
import asyncio
import collections
import dataclasses
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

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

from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType, selection_has
from ..DocumentInterfaceGQLModel import DocumentInterfaceGQLModel

DigitalSubmissionFieldGQLModel = typing.Annotated["DigitalSubmissionFieldGQLModel", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
DigitalSubmissionFieldInputFilter = typing.Annotated["DigitalSubmissionFieldInputFilter", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
DigitalSubmissionSectionGQLModel = typing.Annotated["DigitalSubmissionSectionGQLModel", strawberry.lazy(".DigitalSubmissionSectionGQLModel")]
DigitalSubmissionSectionInputFilter = typing.Annotated["DigitalSubmissionSectionInputFilter", strawberry.lazy(".DigitalSubmissionSectionGQLModel")]
DigitalFormGQLModel = typing.Annotated["DigitalFormGQLModel", strawberry.lazy(".DigitalFormGQLModel")]

# DigitalSubmissionFieldInputFilter = typing.Annotated["DigitalSubmissionFieldInputFilter", strawberry.lazy(".DigitalSubmissionFieldGQLModel")]
@createInputs
@dataclasses.dataclass
class DigitalSubmissionInputFilter:
    name: str
    name_en: str
    # description: str
    id: IDType
    parent_id: IDType

    # parent: "DigitalSubmissionInputFilter"
    # from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInputFilter
    submitted_fields: DigitalSubmissionFieldInputFilter
    # from .DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionInputFilter
    submitted_sections: DigitalSubmissionSectionInputFilter
    from .DigitalFormGQLModel import DigitalFormInputFilter
    form: DigitalFormInputFilter


@strawberry.federation.type(
    keys=["id"], description="""Represents a submission of a digital form filled out by a user.
Aggregates responses for all the fields defined in the form."""
)
class DigitalSubmissionGQLModel(BaseGQLModel): #, DocumentInterfaceGQLModel
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DigitalSubmissionModel
    
    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: uuid.UUID):
        if id is None: return None
        

        _id = IDType(id) if isinstance(id, str) else id
        loader = cls.getLoader(info=info)

        # is_complex = selection_has(["sections", "fields"], info.selected_fields[0].selections)
        # if is_complex:
        #     print("value: complex =", is_complex, flush=True)

        db_row = await loader.load(_id)
        db_row_dict = dataclasses.asdict(db_row) if db_row is not None else None
        # db_row_dict["sections"] = []
        
        return cls(id=id) if db_row is None else cls.from_dataclass(db_row=db_row_dict)    

    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: IDType, **otherdata):
    #     is_complex = selection_has(["sections", "fields"], info.selected_fields[0].selections)
    #     # else:
    #     #     print("value: simple =", info.selected_fields, flush=True)
    #     result = await super().resolve_reference(info=info, id=id, **otherdata)

    #     if is_complex:
    #         print("value: complex =", is_complex, flush=True)
    #         # TODO make hydration of sections and fields
    #     return result

    name: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="state of the submission,",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    form_id: typing.Optional[IDType] = strawberry.field(
        description="Form which is associated to this submission.",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        description="This is id of submission which owns this submission (recursive tree). Submission can contain submissions.",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )    

    # section_id: typing.Optional[IDType] = strawberry.field(
    #     description="this is id of section which owns this section (recursive tree)",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     default=None
    # )    

    form: typing.Optional[DigitalFormGQLModel] = strawberry.field(
        description="form which is associated to this submission",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[DigitalFormGQLModel](fkey_field_name="form_id")
    )

    parent: typing.Optional["DigitalSubmissionGQLModel"] = strawberry.field(
        description="This is submission which owns this submission (recursive tree). Submission can contain submissions. It is like a folder",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DigitalSubmissionGQLModel"](fkey_field_name="parent_id")
    )

    @strawberry.field(
        description="all sumbitted sections on all levels, thanks to materialized path",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def submitted_sections_all(self, info: strawberry.types.Info) -> typing.List[DigitalSubmissionSectionGQLModel]:
        return []
    
    sections: typing.List["DigitalSubmissionSectionGQLModel"] = strawberry.field(
        description="""Digital Submission sections.""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="submission_id", whereType=DigitalSubmissionFieldInputFilter)
    )

    # sections: typing.Optional[typing.List["DigitalSubmissionSectionGQLModel"]] = dataclasses.field(default=None)

    # sections_resolver = VectorResolver["DigitalSubmissionSectionGQLModel"](fkey_field_name="submission_id", whereType=DigitalSubmissionFieldInputFilter)
    # @strawberry.field(
    #     name="sections",
    #     description="sections",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    # )
    # async def sections_(self, info: strawberry.types.Info) -> typing.List["DigitalSubmissionSectionGQLModel"]:
    #     if self.sections is not None:
    #         return self.sections
    #     # result = await self.sections_resolver(self, info)
    #     result = await self.sections_resolver(info)
    #     return result
    
    # @strawberry.field(
    #     description="""Digital Submission sections.""",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    # )
    # async def submitted_sections(self, info: strawberry.types.Info) -> typing.List["DigitalSubmissionSectionGQLModel"]:
    #     from .DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionGQLModel
    #     loader = DigitalSubmissionSectionGQLModel.getLoader(info)
    #     rows = await loader.filter_by(submission_id=self.id)
    #     # for row in rows:
    #     #     print("submitted_sections", dir(row), flush=True)
    #     #     print("submitted_sections", strawberry.asdict(row), flush=True)
    #     # assert False
    #     result = [DigitalSubmissionSectionGQLModel.from_dataclass(row) for row in rows]
    #     return result

    fields: typing.List["DigitalSubmissionFieldGQLModel"] = strawberry.field(
        description="""Digital Submission fields.""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["DigitalSubmissionFieldGQLModel"](fkey_field_name="submission_id", whereType=DigitalSubmissionFieldInputFilter)
    )

    @strawberry.field(
        description="calculate the form value from its sections and fields and return it in json form"
    )
    async def value(self, info: strawberry.types.Info) -> typing.Optional[strawberry.scalars.JSON]:

        from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldGQLModel
        from .DigitalSubmissionSectionGQLModel import DigitalSubmissionSectionGQLModel
        from .DigitalFormFieldGQLModel import DigitalFormFieldGQLModel
        from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel

        submission_field_loader = DigitalSubmissionFieldGQLModel.getLoader(info=info)
        submission_section_loader = DigitalSubmissionSectionGQLModel.getLoader(info=info)
        form_field_loader = DigitalFormFieldGQLModel.getLoader(info=info)
        form_section_loader = DigitalFormSectionGQLModel.getLoader(info=info)

        submission_sections, submission_fields, form_fields, form_sections = (
            await asyncio.gather(
                submission_section_loader.filter_by(submission_id=self.id),
                submission_field_loader.filter_by(submission_id=self.id),
                form_field_loader.filter_by(form_id=self.form_id),
                form_section_loader.filter_by(form_id=self.form_id)
            )
        )

        if not submission_sections and not submission_fields:
            return None

        # --- indexy ---
        form_section_by_id = {s.id: s for s in form_sections}
        form_field_by_id = {f.id: f for f in form_fields}

        # submission fields podle submission_section_id
        subfields_by_section_id: dict = collections.defaultdict(list)
        for sf in submission_fields:
            subfields_by_section_id[getattr(sf, "section_id")].append(sf)


        # strom submission sekcí podle parent submission section
        subs_by_id = {s.id: s for s in submission_sections}
        children_by_parent: dict = collections.defaultdict(list)
        roots: list = []
        for s in subs_by_id.values():
            parent_id = getattr(s, "section_id", None)  # parent submission section id
            if parent_id is None:
                roots.append(s)
            else:
                children_by_parent[parent_id].append(s)

        # seřazení (pokud existuje order na form sekci/field)
        def sec_sort_key(sub_sec):
            fs = form_section_by_id.get(sub_sec.form_section_id)
            return ((getattr(fs, "order", 0) or 0), fs.id if fs else 0)

        def field_sort_key(sub_field):
            ff = form_field_by_id.get(sub_field.field_id)
            return (getattr(ff, "order", 0) or 0, ff.id if ff else 0)

        for k in children_by_parent:
            children_by_parent[k].sort(key=sec_sort_key)
        roots.sort(key=sec_sort_key)
        for sid in subfields_by_section_id:
            subfields_by_section_id[sid].sort(key=field_sort_key)

        # --- rekonstrukce hodnot ---

        def build_section_payload(sub_sec) -> dict:
            """Vrátí dict s hodnotami jedné submission sekce."""
            fs = form_section_by_id.get(sub_sec.form_section_id)
            result: dict = {}

            # 1) hodnoty polí (podle jména form fieldu)
            for sf in subfields_by_section_id.get(sub_sec.id, ()):
                ff = form_field_by_id.get(sf.field_id)
                if not ff or ff.name is None:
                    continue
                # Předpoklad: sf.value je JSON serializovatelná hodnota
                result[ff.name] = getattr(sf, "value", None)

            # 2) subsekce – seskupit podle jména form sekce
            group: dict[str, dict] = {}  # name -> {"repeatable": bool, "items": []}
            for child in children_by_parent.get(sub_sec.id, ()):
                fchild = form_section_by_id.get(child.form_section_id)
                if not fchild or fchild.name is None:
                    # bezejmenné sekce můžeš buď přeskočit, nebo klíčovat idčkem
                    # result[str(fchild.id)] = build_section_payload(child); continue
                    continue
                entry = group.setdefault(
                    fchild.name,
                    {
                        "repeatable": bool(getattr(fchild, "repeatable", False)), 
                        "repeatable_min": int(getattr(fchild, "repeatable_min", 0)), 
                        "repeatable_max": int(getattr(fchild, "repeatable_max", 1)), 
                        "items": []
                    },
                )
                entry["items"].append(build_section_payload(child))


            def shape_items(items, rep_min: int, rep_max: int):
                """
                rep_max:
                - 0 => unlimited (často se tak značí)
                - 1 => 0..1 nebo 1..1 => single
                - >1 => list
                """
                if not items:
                    return None

                unlimited = (rep_max == 0)

                # musí to být pole, když:
                # - max dovoluje víc než 1, nebo je neomezený
                # - min říká, že jich může/má být víc než 1
                # - nebo reálně přišlo víc než 1 (fallback proti datům)
                if unlimited or rep_max > 1 or rep_min > 1 or len(items) > 1:
                    return items

                # jinak single object
                return items[0]


            # 3) převod skupin na list/dict podle repeatable
            for name, info in group.items():
                items = info["items"]
                shaped = shape_items(items, info["repeatable_min"], info["repeatable_max"])
                if shaped is None:
                    continue
                result[name] = shaped
            return result

        # top-level – může existovat víc kořenových sekcí
        output: dict = {}
        for root in roots:
            fs = form_section_by_id.get(root.form_section_id)
            if not fs or fs.name is None:
                # bezejmenné kořeny můžeš řešit dle potřeby
                # output[str(fs.id)] = build_section_payload(root)
                continue

            payload = build_section_payload(root)
            if bool(getattr(fs, "repeatable", False)):
                output.setdefault(fs.name, []).append(payload)
            else:
                output[fs.name] = payload

        return output or None

@strawberry.interface(
    description=""""""
)
class DigitalSubmissionQuery:
    digital_form_submission_by_id: typing.Optional[DigitalSubmissionGQLModel] = strawberry.field(
        description="""Get a DigitalSubmission by id""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DigitalSubmissionGQLModel.load_with_loader
    )

    digital_form_submission_page: typing.List[DigitalSubmissionGQLModel] = strawberry.field(
        description="""Get a page of DigitalSubmissions""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[DigitalSubmissionInputFilter](whereType=DigitalSubmissionInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin, TreeInputStructureMixin

@strawberry.input(
    description="""DigitalSubmission insert mutation"""
)
class DigitalSubmissionInsertGQLModel(InputModelMixin):
    getLoader = DigitalSubmissionGQLModel.getLoader
    form_id: IDType = strawberry.field(
        description="[form](#digitalformgqlmodel) for this submission",
        default=None
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission eng name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission master id""",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission id client generated""",
        default=None
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission id client generated""",
        default=None
    )

    from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel

    sections: typing.Optional[typing.List[SubmissionSectionInsertGQLModel]] = strawberry.field(
        description="sctions which are part of this submission", 
        # default_factory=list,
        default_factory=list
    )

    from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
    fields: typing.Optional[typing.List[DigitalSubmissionFieldInsertGQLModel]] = strawberry.field(
        description="fields of submission",
        default_factory=list
    )
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""DigitalSubmission insert mutation"""
)
class DigitalSubmissionInsertGQLModel2(InputModelMixin):
    getLoader = DigitalSubmissionGQLModel.getLoader
    form_id: IDType = strawberry.field(
        description="[form](#digitalformgqlmodel) for this submission",
        default=None
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission eng name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission master id""",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""DigitalSubmission id client generated""",
        default=None
    )

    from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
    sections: strawberry.Private[typing.List[SubmissionSectionInsertGQLModel]] = dataclasses.field(default_factory=list)
    # strawberry.field(
    #     description="sctions which are part of this submission", 
    #     # default_factory=list,
    #     default_factory=list
    # )

    from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
    fields: strawberry.Private[typing.List[DigitalSubmissionFieldInsertGQLModel]] = dataclasses.field(default_factory=list)
    # strawberry.field(
    #     description="fields of submission",
    #     default_factory=list
    # )

    state_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None    

@strawberry.input(
    description="""DigitalSubmission update mutation"""
)
class DigitalSubmissionUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalSubmission id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalSubmission lastchange"""
    )

    name: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission name""",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="""DigitalSubmission eng name""",
        default=None
    )

@strawberry.input(
    description="""DigitalSubmission delete mutation"""
)
class DigitalSubmissionDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""DigitalSubmission id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""DigitalSubmission lastchange"""
    )

# from .DigitalSubmissionSectionGQLModel import section_into_dbmodel
# import logging
# async def digital_form_submission_insert_internal(
#     self,
#     info: strawberry.types.Info,
#     digital_form_submission: DigitalSubmissionInsertGQLModel
# ) -> typing.Union[DigitalSubmissionGQLModel, InsertError[DigitalSubmissionGQLModel]]:

#     loader = DigitalSubmissionGQLModel.getLoader(info=info)
#     DBModel = loader.getModel()
#     # digital_form_submission.id = digital_form_submission.id if digital_form_submission.id is not None else uuid.uuid4()
#     # for section in (digital_form_submission.sections or []):
#     #     section.submission_id = digital_form_submission.id

#     sections = [section_into_dbmodel(self, info, section) for section in (digital_form_submission.sections or [])]
#     digital_form_submission_as_dict = strawberry.asdict(digital_form_submission)
#     del digital_form_submission_as_dict["sections"]
#     model = DBModel(**digital_form_submission_as_dict)
#     model.submitted_sections.extend(sections)

#     return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=model)

# async def 





@strawberry.interface(
    description="""DigitalSubmission mutation"""
)
class DigitalSubmissionMutation:
    @strawberry.mutation(
        description="""Insert a DigitalSubmission""",
        permission_classes=[
            SimpleInsertPermission[DigitalSubmissionGQLModel](roles=["administrátor"])
        ]
    )
    async def digital_form_submission_insert(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionInsertGQLModel
    ) -> typing.Union[DigitalSubmissionGQLModel, InsertError[DigitalSubmissionGQLModel]]:
        modelinstance = digital_form_submission.intoModel(info=info)
        return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=modelinstance)
        # return await digital_form_submission_insert_internal(self, info, digital_form_submission)
        # return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    
    from .DigitalFormGQLModel import DigitalFormGQLModel
    @strawberry.mutation(
        description="""Insert a DigitalSubmission""",
        permission_classes=[
            # SimpleInsertPermission[DigitalSubmissionGQLModel](roles=["administrátor"])
            OnlyForAuthentized
        ],
        extensions=[
            # TODO redefine roles for Submission initialization
            # 
            UserAccessControlExtension[InsertError, DigitalSubmissionGQLModel](
                roles=[
                    "procesní administrátor", 
                    "inicializátor"
                ]
            ),
            UserRoleProviderExtension[UpdateError, DigitalSubmissionGQLModel](),
            RbacProviderExtension[UpdateError, DigitalSubmissionGQLModel](),
            LoadDataExtension[UpdateError, DigitalSubmissionGQLModel](
                primary_key_name="form_id",
                getLoader=DigitalFormGQLModel.getLoader
            )
        ]
    )
    async def digital_form_submission_insert2(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionInsertGQLModel2,
        user_roles: typing.List[typing.Any],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[DigitalSubmissionGQLModel, InsertError[DigitalSubmissionGQLModel]]:
        # TODO create RBACObject Child
        digital_form_submission.rbacobject_id = rbacobject_id
        from .DigitalFormFieldGQLModel import DigitalFormFieldGQLModel
        from .DigitalFormSectionGQLModel import DigitalFormSectionGQLModel

        from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
        from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel

        from .helpers import create_SubmissionSectionInsertGQLModel

        fieldLoader = DigitalFormFieldGQLModel.getLoader(info=info)
        sectionLoader = DigitalFormSectionGQLModel.getLoader(info=info)
        
        # ziskat data z tabulek, vsechny sekce a polozky/fieldy, ktere patri k formulari
        form_fields, form_sections = await asyncio.gather(
            fieldLoader.filter_by(form_id=digital_form_submission.form_id),
            sectionLoader.filter_by(form_id=digital_form_submission.form_id)
        )

        # rekonstruujeme strukturu
        form_section_map = {
            section.id: {
                "section": dataclasses.asdict(section),
                "name": section.name,
                "sections": [],
                "fields": []
            } for section in form_sections
        }

        for section in form_section_map.values():
            parent_id = section["section"]["section_id"]
            if parent_id is None:
                continue
            form_section_map[parent_id]["sections"].append(
                section
            )
        
        form_field_map = {
            field.id: {
                "field": dataclasses.asdict(field),
                "name": field.name,
                "section": form_section_map[field.form_section_id]
            }
            for field in form_fields
        }

        for field in form_field_map.values():
            form_section_id = field["field"]["form_section_id"]
            form_section_map[form_section_id]["fields"].append(field)

        # struktura rekonstruovana
        submission_id = digital_form_submission.id or uuid.uuid4()
        submission = DigitalSubmissionInsertGQLModel(
            id=submission_id,
            form_id=digital_form_submission.form_id,
            sections=[], # SubmissionSectionInsertGQLModel()]
            fields=[] # DigitalSubmissionFieldInsertGQLModel()
        )
        
        
        # def create_DigitalSubmissionFieldInsertGQLModel(form_field, section_id, submission_id, index=0):
        #     params = {
        #         "field_id": form_field["field"]["id"],
        #         "section_id": section_id,
        #         "submission_id": submission_id,
        #         # "index": index # nepouziva se
        #         "value": ""
        #     }

        #     result = DigitalSubmissionFieldInsertGQLModel(**params)
        #     return result
            

        # def create_SubmissionSectionInsertGQLModel(form_section, submission_id=None, submission_section_id=None, index=0):    
        #     id = uuid.uuid4()
        #     params = {
        #         "submission_id": submission_id,
        #         # "section_id": submission_section_id, # nepouziva se dovodi se jinde
        #         "form_section_id": form_section["section"]["id"],
        #         "index": index,
        #         "id": id,
        #         "sections": [],
        #         "fields": [],
        #     }
            
        #     form_section_sections = form_section["sections"]
        #     form_section_fields = form_section["fields"]
        #     result = SubmissionSectionInsertGQLModel(**params)
        #     result.fields = [
        #         create_DigitalSubmissionFieldInsertGQLModel(
        #             form_field=form_field,
        #             section_id=id,
        #             submission_id=submission_id,
        #             index=index
        #         )
        #         for (index, form_field) in enumerate(form_section_fields)]
        #     result_sections = []
        #     for form_sub_section in form_section_sections:
        #         repeatable_min = form_sub_section["section"]["repeatable_min"] or 0
        #         repeatable_max = form_sub_section["section"]["repeatable_max"] or 1
        #         if repeatable_max < repeatable_min:
        #             repeatable_max = repeatable_min
        #         if repeatable_max == 0:
        #             repeatable_max = 1
        #         desired = max(1, repeatable_min)
        #         desired = min(desired, repeatable_max)
        #         for index in range(desired):
        #             submission_sub_section = create_SubmissionSectionInsertGQLModel(
        #                 form_section=form_sub_section,
        #                 submission_id=submission_id,
        #                 submission_section_id=id,
        #                 index=index
        #             )
        #             result_sections.append(submission_sub_section)
        #     result.sections = result_sections
        #     return result
        
        submission.sections = [
            create_SubmissionSectionInsertGQLModel(
                section,
                submission_id=submission_id, # nepouziva se dovodi se jinde
                submission_section_id=None,
                index=index
            )
            for (index, section) in enumerate(form_section_map.values()) if section["section"]["section_id"] is None
        ]

        # def create_repeateble_section(section_from_map, data: list):
        #     form_section = section_from_map["section"]
        #     repatable_min = form_section.repeatable_min
        #     repatable_max = form_section.repeatable_max
        #     repeatable = form_section.repeatable

        #     if not repeatable:
        #         raise ValueError(f"Section '{form_section.name}' není repeatable, ale dostal jsem list hodnot.")

        #     if repatable_min is not None and len(data) < repatable_min:
        #         raise ValueError(f"Section '{form_section.name}' vyžaduje min {repatable_min} opakování, dostal jsem {len(data)}.")

        #     if repatable_max is not None and len(data) > repatable_max:
        #         raise ValueError(f"Section '{form_section.name}' povoluje max {repatable_max} opakování, dostal jsem {len(data)}.")

            
        #     from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
            
        #     result = []
        #     for item in data:
        #         result_item = SubmissionSectionInsertGQLModel(
        #             form_section_id=form_section.id
        #         )
        #         fill_submission_section(result_item, item)
        #         result.append(result_item)
        #     return result
        
        # def create_single_section(section_from_map, data: dict):
        #     form_section = section_from_map["section"]
        #     # repatable_min = form_section.repatable_min
        #     # repatable_max = form_section.repatable_max

        #     from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
            

        #     result = SubmissionSectionInsertGQLModel(
        #         form_section_id=form_section.id
        #     )
        #     fill_submission_section(result, data)
        #     return result
            
        # def fill_submission_section(submission_section, data: dict):
        #     from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
        #     form_section_id = submission_section.form_section_id
        #     form_section = form_section_map[form_section_id]
        #     form_section_subsections = form_section["sections"]
        #     form_section_fields = form_section["fields"]

        #     # Indexy pro rychlé hledání podle name
        #     subsections_by_name = {
        #         s["name"]: s for s in form_section_subsections if s.get("name") is not None
        #     }
        #     fields_by_name = {
        #         f["name"]: f for f in form_section_fields if f.get("name") is not None
        #     }

        #     for key, value in data.items():
        #         is_list = isinstance(value, list)
        #         is_dict = isinstance(value, dict)

        #         # 1) Zkusíme nejdřív pole (skalár)
        #         if not is_list and not is_dict and key in fields_by_name:
        #             form_field = fields_by_name[key]
        #             submission_field = DigitalSubmissionFieldInsertGQLModel(
        #                 field_id=form_field["field"].id,
        #                 section_id=submission_section.id,
        #                 value=value
        #             )
        #             submission_section.fields.append(submission_field)
        #             continue

        #         # 2) Jinak hledáme sekci podle name
        #         subsection_from_map = subsections_by_name.get(key)
        #         if subsection_from_map is None:
        #             # Klíč neodpovídá poli ani sekci – můžeš logovat / vyhodit chybu / ignorovat
        #             # raise KeyError(f"Neznámý klíč '{key}' pro sekci '{form_section['name']}'")
        #             continue
                
        #         # 2a) List => repeatable subsekce
        #         if is_list:
        #             created = create_repeateble_section(subsection_from_map, value)
        #             # připojit všechny vytvořené subsekce
        #             submission_section.sections.extend(created)
        #             continue

        #         # 2b) Dict => single subsekce
        #         if is_dict:
        #             created = create_single_section(subsection_from_map, value)
        #             submission_section.sections.append(created)
        #             continue

        #     used_subsections = {
        #         sub_section.form_section_id: sub_section
        #         for sub_section in submission_section.sections
        #     }
        #     for form_subsection in form_section_subsections:
        #         if form_subsection.id in used_subsections:
        #             continue
        #         submission_subsection = create_single_section(
        #             form_section_map[form_subsection.id], data={}
        #         )
        #         submission_section.sections.append(submission_subsection)

        #     # for subsection in form_section_subsections:

        # def create_submission_section(section_from_map, data):
        #     from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
        #     result = SubmissionSectionInsertGQLModel(
        #         form_section_id=section_from_map["section"].id
        #     )
        #     for key, value in data.items():
        #         if isinstance(value, list):
        #             # vytvorime pole sekci, form_section musi mit atribut opakovatelnosti
        #             # repatable_min: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
        #             # repatable_max: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
        #             # repeatable: Mapped[Optional[bool]] = mapped_column(Boolean, default=None, nullable=True)
                    
        #             for v in value:

        #                 pass
        #         elif isinstance(value, dict):
        #             # dict, musi mu odpovidat form_section
        #             # vytvorime jedinou submission_section
        #             pass
        #         else:
        #             # trivialni typ, musi mu odpovidat field
        #             pass


        # def name_section(id, parent_name):
        #     section = form_section_map[id]
        #     name = parent_name + "." + section["section"].name
        #     section["name"] = name
        #     sections = section["sections"]
        #     for s in sections:
        #         name_section(s["section"].id, name)




        # def clamp(n, lo, hi):
        #     if hi is None:
        #         return max(lo, n)
        #     return max(lo, min(hi, n))

        # def build_submission_section_instances(form_section_node, parent_sub_section_id):
        #     """
        #     form_section_node je tvoje struktura z form_section_map: {"section": <FormSection>, "sections": [...], "fields": [...]}
        #     parent_sub_section_id je ID submission section rodiče (None pro root)
        #     """
        #     def_section = form_section_node["section"]

        #     # repeatable nastavení (uprav podle polí ve tvém modelu)
        #     repeatable = getattr(def_section, "repeatable", False)
        #     rmin = getattr(def_section, "repeatable_min", 1 if not repeatable else 1)
        #     rmax = getattr(def_section, "repeatable_max", 1 if not repeatable else 1)

        #     # existující instance pro (parent, def)
        #     existing = sub_sections_by_parent_and_def[(parent_sub_section_id, def_section.id)]

        #     # kolik instancí chceme držet
        #     if repeatable:
        #         desired = clamp(len(existing) or rmin or 0, rmin or 0, rmax)
        #     else:
        #         desired = 1

        #     # vezmi existující a doplň chybějící
        #     instances = list(existing[:desired])
        #     while len(instances) < desired:
        #         # vytvoř novou submission section instanci
        #         # názvy atributů uprav podle svého modelu
        #         ss = DigitalFormSubmissionSectionGQLModel(
        #             id=new_id(),
        #             submission_id=digital_form_submission.id,
        #             section_id=parent_sub_section_id,      # parent submission section id
        #             form_section_id=def_section.id,        # definice
        #         )
        #         instances.append(ss)

        #     # pro každou instanci doplň fields + children
        #     out = []
        #     for ss in instances:
        #         # fields podle definice
        #         fields_out = []
        #         for f in form_section_node["fields"]:
        #             def_field = f["field"]
        #             key = (ss.id, def_field.id)
        #             existing_sf = sub_fields_by_section_and_field.get(key)
        #             if existing_sf is None:
        #                 existing_sf = DigitalFormSubmissionFieldGQLModel(
        #                     id=new_id(),
        #                     submission_id=digital_form_submission.id,
        #                     section_id=ss.id,
        #                     form_field_id=def_field.id,
        #                     value="",  # nebo None
        #                 )
        #             fields_out.append(existing_sf)

        #         # children sekce rekurzivně
        #         child_sections_out = []
        #         for child_def_node in form_section_node["sections"]:
        #             child_sections_out.extend(build_submission_section_instances(child_def_node, ss.id))

        #         out.append({
        #             "section": ss,
        #             "fields": fields_out,
        #             "sections": child_sections_out
        #         })

        #     return out







        # section_map_names = {
        #     section.name: section for section in form_sections 
        # }

        # for section in form_section_map.values():
        #     if section.form_section_id:
        #         parent_section = form_section_map[section.form_section_id]
        #         parent_section.sections
        # def section_name(section):
        #     result = section.name
        #     if form_section_id:=section.form_section_id:
        #         result = section_name(form_section_id) + "." + result
        #     return result
        
        # section_map_2 = {
        #     section.id: section_name(section.id) for section in form_section_map.values()
        # }

        # form_field_map = {
        #     field.id: field for field in form_fields
        # }

        # modelinstance = digital_form_submission.intoModel(info=info)
        model = await submission.intoModel(info=info)
        print("*" * 30)
        print("model", model)
        print("model.sections", model.sections)
        print("*" * 30)

        return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=submission)
        # return await digital_form_submission_insert_internal(self, info, digital_form_submission)
        # return await Insert[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    

    @strawberry.mutation(
        description="""Update a DigitalSubmission""",
        permission_classes=[
            # SimpleInsertPermission[DigitalSubmissionGQLModel](roles=["administrátor"])
            OnlyForAuthentized
        ],
        extensions=[
            # TODO redefine roles for Submission initialization
            # 
            UserAccessControlExtension[InsertError, DigitalSubmissionGQLModel](
                roles=[
                    "procesní administrátor", 
                    "autor"
                ]
            ),
            UserRoleProviderExtension[UpdateError, DigitalSubmissionGQLModel](),
            RbacProviderExtension[UpdateError, DigitalSubmissionGQLModel](),
            LoadDataExtension[UpdateError, DigitalSubmissionGQLModel]()
        ]
    )
    async def digital_form_submission_update(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[DigitalSubmissionGQLModel, UpdateError[DigitalSubmissionGQLModel]]:
        return await Update[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)
    
    @strawberry.mutation(
        description="""Delete a DigitalSubmission""",
        permission_classes=[
            # SimpleInsertPermission[DigitalSubmissionGQLModel](roles=["administrátor"])
            OnlyForAuthentized
        ],
        extensions=[
            # TODO redefine roles for Submission delete
            # 
            UserAccessControlExtension[DeleteError, DigitalSubmissionGQLModel](
                roles=[
                    "procesní administrátor"
                ]
            ),
            UserRoleProviderExtension[DeleteError, DigitalSubmissionGQLModel](),
            RbacProviderExtension[DeleteError, DigitalSubmissionGQLModel](),
            LoadDataExtension[DeleteError, DigitalSubmissionGQLModel]()
        ]
    )
    async def digital_form_submission_delete(
        self,
        info: strawberry.types.Info,
        digital_form_submission: DigitalSubmissionDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[DigitalSubmissionGQLModel]]:
        return await Delete[DigitalSubmissionGQLModel].DoItSafeWay(info=info, entity=digital_form_submission)    