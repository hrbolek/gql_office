import uuid
import strawberry
import asyncio

from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    getUserFromInfo,
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

from .BaseGQLModel import IDType

# from functools import cache
# class ChangeParent:
#     type_arg = None  # Placeholder for the generic type argument

    
#     @classmethod
#     @cache
#     def __class_getitem__(cls, item):
#         # When MyGenericClass[int] is accessed, create a new class with type_arg set
#         new_cls = type(f"{cls.__name__}[{item.__name__}]", (cls,), {"type_arg": item})
#         return new_cls

#     @classmethod
#     async def DoItSafeWay(cls, info, entity):
#         type_arg = cls.type_arg
#         try:
#             loader = type_arg.getLoader(info=info)
#             actinguser = getUserFromInfo(info)
#             id = IDType(actinguser["id"])
#             entity.changedby_id = id

#             row = await loader.update(entity)
#             if row is None:
#                 # _entity = await loader.load(facility.id)
#                 _entity = await type_arg.resolve_reference(info=info, id=entity.id)
#                 return UpdateError[type_arg](_entity=_entity, msg="update failed", _input=entity)
#             else:
#                 return await type_arg.resolve_reference(info=info, id=entity.id)
#         except Exception as e:
#             _entity = await type_arg.resolve_reference(info=info, id=entity.id)
#             return UpdateError[type_arg](_entity=_entity, msg=f"{e}", _input=entity)

def create_tree_parents_resolver(T):
    async def tree_parents_resolver(self, info: strawberry.types.Info):
        loader = T.getLoader(info)
        idstrings = self.path.split("/")
        ids = (IDType(id) for id in idstrings)
        futures = [loader.load(id) for id in ids]
        values = await asyncio.gather(*futures)
        results = [T.from_dataclass(value) for value in values if value is not None]
        return results
    return tree_parents_resolver


@strawberry.input(description="Input type for creating a Tree")
class TreeUpdateParent:
    id: IDType = strawberry.field(
        description="Tree id",
    )
    parent_id: IDType = strawberry.field(
        description="Tree parent id",
    )
    path: strawberry.Private[str] = None


def create_tree_parent_updater(T):
    async def tree_parent_updater(self, info: strawberry.types.Info, tree: TreeUpdateParent):
        loader = T.getLoader(info)
        futures = [loader.load(tree.id), loader.load(tree.parent_id)]
        selfrow, parentrow = await asyncio.gather(*futures)
        if selfrow is None:
            return UpdateError[T](msg="Tree not found", _input=tree, _entity=None)
        if parentrow is None:
            return UpdateError[T](msg="Parent not found", _input=tree, _entity=selfrow)
        tree.path = f"{parentrow.path}/{selfrow.id}"
        
        return Update[T].DoItSafeWay(info=info, entity=tree)
    return tree_parent_updater

