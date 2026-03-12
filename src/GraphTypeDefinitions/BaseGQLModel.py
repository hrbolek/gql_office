import sys
import uuid
import datetime
import typing
import strawberry
import dataclasses
from typing import get_origin, get_args


from strawberry.utils.typing import eval_type

from uoishelpers.gqlpermissions import OnlyForAuthentized, RBACObjectGQLModel

IDType = uuid.UUID
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]



from strawberry.federation.schema_directive import schema_directive, Location
from strawberry.directive import DirectiveLocation
@schema_directive(
    repeatable=True,
    compose=True,
    description="Description for foreign keys",
    locations=[Location.INPUT_FIELD_DEFINITION, Location.FIELD_DEFINITION, DirectiveLocation.FIELD],
)
class Relation:
    """
    @relation(to: Typ, field: 'id')
    říká, že pole inputu je cizí klíč na zadaný typ.
    """
    to: str
    field: str = "id"

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: IDType, **otherData):
    _id = IDType(id) if isinstance(id, str) else id
    return None if id is None else cls(id=_id, **otherData)

from collections.abc import Iterable

def _as_list(x):
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return list(x)
    return [x]

def _iter_selected_fields(selections):
    """
    Vrátí "plochý" iterátor SelectedFieldů na dané úrovni:
    - SelectedField vrátí přímo
    - FragmentSpread / InlineFragment rozbalí a vrátí jejich selections
    """
    for sel in _as_list(selections):
        # SelectedField
        if hasattr(sel, "name") and hasattr(sel, "selections"):
            yield sel
            continue

        # FragmentSpread nebo InlineFragment (oba mají .selections)
        if hasattr(sel, "selections"):
            yield from _iter_selected_fields(sel.selections)
            continue

        # něco jiného -> ignoruj

def selection_has(path, selected_fields):
    def walk(selections, idx):
        # print(f"walk: idx={idx}, path={path}, selections={[f.name for f in _iter_selected_fields(selections)]}", flush=True)
        if idx == len(path):
            return True

        name = path[idx]

        for f in _iter_selected_fields(selections):
            if f.name == name:
                return walk(f.selections, idx + 1)
            
        for f in _iter_selected_fields(selections):
            if isinstance(f, (strawberry.types.nodes.FragmentSpread, strawberry.types.nodes.InlineFragment)):
                if walk(f.selections, idx):
                    return True

        return False

    return walk(selected_fields, 0)

# def private_list_field(*, item_type: typing.Callable[[], type], cache_key=None, loader=None):
#     return dataclasses.field(
#         default=strawberry.UNSET,
#         repr=False,
#         metadata={"hydrate": {"kind":"list", "item_type": item_type, "cache_key": cache_key, "loader": loader}},
#     )

# NoneType = type(None)

# def resolve_field_type(cls, field_name: str):
#     ann = getattr(cls, "__annotations__", {}).get(field_name, None)
#     if ann is None:
#         return None

#     # už je to reálný typ, ne string
#     if not isinstance(ann, str) and not isinstance(ann, typing.ForwardRef):
#         return ann

#     mod = sys.modules[cls.__module__]
#     globalns = mod.__dict__
#     # omezené localns výrazně snižuje riziko cyklů
#     localns = {cls.__name__: cls}

#     try:
#         # eval stringu / ForwardRefu
#         if isinstance(ann, str):
#             return eval(ann, globalns, localns)
#         else:
#             # ForwardRef
#             return typing._eval_type(ann, globalns, localns)  # OK v praxi, interní API
#     except RecursionError:
#         # fallback: nech to jako string/ForwardRef, typovou inferenci pro listy pak neřeš
#         return ann
#     except Exception:
#         return ann
    
# def _get_type_hints(cls):
#     # vyřeší ForwardRef/"..."
#     mod = sys.modules[cls.__module__]
#     return typing.get_type_hints(cls, globalns=mod.__dict__, localns=mod.__dict__, include_extras=True)

# def _unwrap_annotated(tp):
#     if typing.get_origin(tp) is typing.Annotated:
#         return typing.get_args(tp)[0]
#     return tp

# def _unwrap_private(tp):
#     # strawberry.Private[T] -> T
#     origin = typing.get_origin(tp)
#     if origin is not None and getattr(origin, "__name__", None) == "Private":
#         args = typing.get_args(tp)
#         if args:
#             return args[0]
#     return tp

# def _unwrap_optional(tp):
#     # Optional[T] / Union[T, None] -> (T, True)
#     # print(f"_unwrap_optional: tp={tp}, {tp.__class__}", flush=True)
#     if tp.__class__.__name__ == "StrawberryOptional":
#         print(f"_unwrap_optional: StrawberryOptional detected, tp={tp}, {tp.of_type}", flush=True)
#         return tp.of_type, True

#     origin = typing.get_origin(tp)
#     if origin is typing.Union:
#         args = typing.get_args(tp)
#         if NoneType in args:
#             non_none = [a for a in args if a is not NoneType]
#             if len(non_none) == 1:
#                 return non_none[0], True
#             # Union bez None necháme jako Union (zatím nepodporujeme)
#             return tp, True
#     return tp, False

# def _is_list_origin(origin):
#     return origin in (
#         list,
#         tuple,
#         set,
#         frozenset,
#         typing.List,
#         typing.Sequence,
#         typing.Collection,
#     )
# import functools

# @functools.lru_cache(maxsize=1024)
# def resolve_field_return_type(tp, name=None):
#     """
#     Vrátí (item_type, is_list, is_optional, origin_container_type)
#     - item_type: typ položky (pro list) nebo typ samotné hodnoty
#     - origin_container_type: např. list/tuple/set (kvůli rekonstrukci)
#     """
    
#     tp0 = tp
#     tp = _unwrap_annotated(tp)
#     tp = _unwrap_private(tp)

#     tp, is_optional = _unwrap_optional(tp)

#     origin = typing.get_origin(tp)
    
#     if _is_list_origin(origin):
#         args = typing.get_args(tp)
#         item_type = args[0] if args else typing.Any
#         # print(f"resolve_field_return_type: name={name}, tp={tp}, tp0={tp0}, item_type={item_type}", flush=True)
#         return item_type, True, is_optional, origin or list

#     # print(f"resolve_field_return_type: name={name}, tp={tp}, tp0={tp0}, origin={origin}", flush=True)
#     # dict můžeš přidat podobně, teď necháme scalar/object
#     return tp, False, is_optional, None

@strawberry.federation.interface(
    description="""Entity representing an interface"""
)
class BaseGQLModel:
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        raise NotImplementedError()
    
    @classmethod
    def from_dataclass(cls, db_row):

        if isinstance(db_row, dict):
            db_row_dict = dict(db_row)
        else:
            if not dataclasses.is_dataclass(db_row):
                raise TypeError(f"unsupported type for from_dataclass: {type(db_row)}")
            db_row_dict = dataclasses.asdict(db_row)
        return cls(**db_row_dict)
        

    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: uuid.UUID):
        if id is None: return None

        _id = IDType(id) if isinstance(id, str) else id
        loader = cls.getLoader(info=info)
        db_row = await loader.load(_id)
        
        return cls(id=id) if db_row is None else cls.from_dataclass(db_row=db_row)
    
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID, **otherdata):
        return await cls.load_with_loader(info=info, id=id)
       
    id: IDType = strawberry.field(
        description="primary key", 
        permission_classes=[OnlyForAuthentized]
        )
    lastchange: typing.Optional[datetime.datetime] = strawberry.field(
        description="timestamp", 
        default=None,
        permission_classes=[OnlyForAuthentized]
        )
    created: typing.Optional[datetime.datetime] = strawberry.field(
        description="date & time of unit born", 
        default=None,
        permission_classes=[OnlyForAuthentized]
        )
    createdby_id: typing.Optional[IDType] = strawberry.field(
        description="who created this entity", 
        default=None,
        permission_classes=[OnlyForAuthentized]
        )
    changedby_id: typing.Optional[IDType] = strawberry.field(
        description="who changed this entity", 
        default=None,
        permission_classes=[OnlyForAuthentized]
        )
    rbacobject_id: typing.Optional[IDType] = strawberry.field(
        description="rbac ruling object", 
        default=None,
        permission_classes=[OnlyForAuthentized]
        )

    @strawberry.field(
        description="who created this entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def createdby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.createdby_id is None else UserGQLModel(id=self.createdby_id)

    @strawberry.field(
        description="who changed this entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def changedby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.changedby_id is None else UserGQLModel(id=self.changedby_id)

    @strawberry.field(
        description="rbac ruling object",
        permission_classes=[OnlyForAuthentized]
        )
    async def rbacobject(self) -> typing.Optional["RBACObjectGQLModel"]:
        return None if self.rbacobject_id is None else RBACObjectGQLModel(id=self.rbacobject_id)
