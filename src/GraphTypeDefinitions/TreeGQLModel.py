# import uuid
# import strawberry
# import asyncio
# import typing

# import strawberry.types
# from uoishelpers.resolvers import (
#     getLoadersFromInfo, 
#     getUserFromInfo,
#     createInputs,

#     InsertError, 
#     Insert, 
#     UpdateError, 
#     Update, 
#     DeleteError, 
#     Delete,

#     PageResolver,
#     VectorResolver,
#     ScalarResolver
# )
# from uoishelpers.gqlpermissions import OnlyForAuthentized
# from .BaseGQLModel import IDType, BaseGQLModel

# # from functools import cache
# # class ChangeParent:
# #     type_arg = None  # Placeholder for the generic type argument

    
# #     @classmethod
# #     @cache
# #     def __class_getitem__(cls, item):
# #         # When MyGenericClass[int] is accessed, create a new class with type_arg set
# #         new_cls = type(f"{cls.__name__}[{item.__name__}]", (cls,), {"type_arg": item})
# #         return new_cls

# #     @classmethod
# #     async def DoItSafeWay(cls, info, entity):
# #         type_arg = cls.type_arg
# #         try:
# #             loader = type_arg.getLoader(info=info)
# #             actinguser = getUserFromInfo(info)
# #             id = IDType(actinguser["id"])
# #             entity.changedby_id = id

# #             row = await loader.update(entity)
# #             if row is None:
# #                 # _entity = await loader.load(facility.id)
# #                 _entity = await type_arg.resolve_reference(info=info, id=entity.id)
# #                 return UpdateError[type_arg](_entity=_entity, msg="update failed", _input=entity)
# #             else:
# #                 return await type_arg.resolve_reference(info=info, id=entity.id)
# #         except Exception as e:
# #             _entity = await type_arg.resolve_reference(info=info, id=entity.id)
# #             return UpdateError[type_arg](_entity=_entity, msg=f"{e}", _input=entity)

# def create_tree_parents_resolver(T):
#     async def tree_parents_resolver(self, info: strawberry.types.Info):
#         loader = T.getLoader(info)
#         idstrings = self.path.split("/")
#         ids = (IDType(id) for id in idstrings)
#         futures = [loader.load(id) for id in ids]
#         values = await asyncio.gather(*futures)
#         results = [T.from_dataclass(value) for value in values if value is not None]
#         return results
#     return tree_parents_resolver


# @strawberry.input(description="Input type for creating a Tree")
# class TreeUpdateParent:
#     id: IDType = strawberry.field(
#         description="Tree id",
#     )
#     parent_id: IDType = strawberry.field(
#         description="Tree parent id",
#     )
#     path: strawberry.Private[str] = None


# def create_tree_parent_updater(T):
#     async def tree_parent_updater(self, info: strawberry.types.Info, tree: TreeUpdateParent):
#         loader = T.getLoader(info)
#         futures = [loader.load(tree.id), loader.load(tree.parent_id)]
#         selfrow, parentrow = await asyncio.gather(*futures)
#         if selfrow is None:
#             return UpdateError[T](msg="Tree not found", _input=tree, _entity=None)
#         if parentrow is None:
#             return UpdateError[T](msg="Parent not found", _input=tree, _entity=selfrow)
#         tree.path = f"{parentrow.path}/{selfrow.id}"
        
#         return Update[T].DoItSafeWay(info=info, entity=tree)
#     return tree_parent_updater


# def parent_resolver(T, parent_id_field="parent_id"):
#     @strawberry.field(description="Parent of this entity")
#     async def parent(self, info: strawberry.types.Info) -> typing.Optional[T]:
#         data = await self.load_with_loader(info=info, id=getattr(self, parent_id_field))
#         return T.from_dataclass(data) if data else None
#     return parent

# def children_resolver(T):
#     @strawberry.field(description="Children of this entity")
#     async def children(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, orderby: typing.Optional[str] = None, where: typing.Optional[typing.Any] = None) -> typing.List[T]:
#         loader = T.getLoader(info=info)
#         where = None if where is None else strawberry.asdict(where)
#         results = await loader.page(skip=skip, limit=limit, orderby=orderby, where=where, extendedfilter={"parent_id": self.id})
#         return [T.from_dataclass(result) for result in results]
#     return children

# def parents_resolver(T):
#     @strawberry.field(description="All parents of this entity")
#     async def parents(self, info: strawberry.types.Info) -> typing.List[T]:
#         loader = T.getLoader(info=info)
#         idstrings = self.path.split("/")
#         ids = (IDType(id) for id in idstrings)
#         futures = [loader.load(id) for id in ids]
#         values = await asyncio.gather(*futures)
#         results = [T.from_dataclass(value) for value in values if value is not None]
#         return results
#     return parents

# # Filter = typing.TypeVar("Filter")
# # Self = typing.TypeVar("Self", bound="TreeGQLModel")
# @strawberry.federation.interface()
# class TreeGQLModel():
    
#     type_arg = None  # Placeholder for the generic type argument
#     def __class_getitem__(cls, type_arg):
#         # If someone has already specialized this exact class, reuse it
#         existing = getattr(cls, "_specializations", {})
#         if type_arg in existing:
#             return existing[type_arg]

#         # Otherwise build a new subclass
#         name = f"{cls.__name__}[{type_arg}]"
#         new_cls = type(
#             name,
#             (cls,),                              # inherit everything
#             {"type_arg": type_arg}              # stash the type arg
#         )

#         # store it so repeated lookups reuse the same class
#         cls._specializations = {**existing, type_arg: new_cls}
#         return new_cls
    

#     path: typing.Optional[str] = strawberry.field(
#         description="Path to this entity",
#         default=None,
#         permission_classes=[OnlyForAuthentized]
#     )

#     parent_id: typing.Optional[IDType] = strawberry.field(
#         description="Parent id",
#         default=None,
#         permission_classes=[OnlyForAuthentized],
#         # resolver=lambda self, info: self.masterevent_id
#     )

#     parent: typing.Optional["TreeGQLModel"] = strawberry.field(
#         description="Parent of this entity",
#         permission_classes=[OnlyForAuthentized],
#         resolver=parent_resolver("TreeGQLModel")
#     )

#     # @strawberry.field(
#     #     description="Closest parent of this entity",
#     #     permission_classes=[OnlyForAuthentized]
#     # )
#     # async def parent(self, info: strawberry.types.Info) -> typing.Optional["TreeGQLModel"]:
#     #     result = await type(self).load_with_loader(info=info, id=self.parent_id)
#     #     return result

#     @strawberry.field(
#         # graphql_type="TreeGQLModel"
#     )
#     # async def parent(self, info) -> "TreeGQLModel[self.__class__.type_arg]":
#     async def parent(self, info) -> typing.Optional["TreeGQLModel"]:
#         data = await self.load_with_loader(info=info, id=self.parent_id)
#         return type(self).from_dataclass(data) if data else None

#     # children: typing.List["TreeGQLModel"] = strawberry.field(
#     #     description="Children of this entity",
#     #     permission_classes=[OnlyForAuthentized],
#     #     resolver=VectorResolver["TreeGQLModel"](
#     #         fkey_field_name="parent_id",
#     #         whereType=Filter
#     #     )
#     # )

#     # @strawberry.field(
#     #     description="Children of this entity",
#     #     permission_classes=[OnlyForAuthentized]
#     # )
#     # async def children(self: Self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, orderby: typing.Optional[str] = None, where: typing.Optional[Filter] = None) -> typing.List[Self]:
#     #     loader = self.getLoader(info=info)
#     #     where = None if where is None else strawberry.asdict(where)
#     #     results = await loader.page(skip=skip, limit=limit, orderby=orderby, where=where, extendedfilter={"parent_id": self.id})
#     #     return (self.from_dataclass(result) for result in results)
    
#     # @strawberry.field(
#     #     description="All parents of this entity",
#     #     permission_classes=[OnlyForAuthentized]
#     # )
#     # async def parents(self: Self, info: strawberry.types.Info) -> typing.List[Self]:
#     #     loader = self.getLoader(info=info)
#     #     idstrings = self.path.split("/")
#     #     ids = (IDType(id) for id in idstrings)
#     #     futures = [loader.load(id) for id in ids]
#     #     values = await asyncio.gather(*futures)
#     #     results = [self.from_dataclass(value) for value in values if value is not None]
#     #     return results    
    
# @strawberry.input(description="Input type for updating a Tree")
# class TreeUpdateParentInput:
#     id: IDType = strawberry.field(
#         description="Tree id",
#     )
#     parent_id: IDType = strawberry.field(
#         description="Tree parent id",
#     )
#     changedby_id: strawberry.Private[IDType]

# T = typing.TypeVar("T", bound=TreeGQLModel)
# InputType = typing.TypeVar("InputType")

# class TreeMutationResolver(typing.Generic[T, InputType]):
#     def __init__(
#         self,
#         model_cls: typing.Type[T],
#         input_type: typing.Type[InputType]
#     ):
#         self.model_cls = model_cls
#         self.input_type = input_type

#     async def __call__(
#         self,
#         info: strawberry.types.Info,
#         input: InputType
#     ) -> typing.Union[T, UpdateError[T]]:
#         loader = self.model_cls.getLoader(info=info)
#         actinguser = getUserFromInfo(info)
#         id = IDType(actinguser["id"])
#         input.changedby_id = id

#         # 1) Načíst entitu, kterou měníme
#         entity = await loader.load(input.id)
#         if entity is None:
#             return UpdateError[T](message=f"Entity {input.id} nenalezena", _input=input, _entity=None)

#         old_path = entity.path        

#         # 2) Zjistit nový parent a jeho path
#         new_parent = None
#         new_parent_path = ""
#         if input.parent_id is not None:
#             new_parent = await loader.load(input.parent_id)
#             if new_parent is None:
#                 return UpdateError[T](message=f"Parent {input.parent_id} nenalezen", _entity=entity, _input=input)
#             new_parent_path = new_parent.path


#         # 3) Zjistit všechny potomky
#         dbModel = loader.getDBModel()
#         stmt = loader.mainstmt.where(dbModel.path.like(f"{old_path}/%"))
#         descendants = await loader.execute_select(stmt)

#         asyncSessionMaker = loader.getSessionMaker()

#         # 4) Změnit path potomků
#         try:
#             async with asyncSessionMaker() as session:
#                 # A) Zahájíme transakci
#                 async with session.begin():
#                     # B) Pro každého potomka jen přepište path
#                     if new_parent is not None:
#                         new_path = f"{new_parent_path}/{input.id}"
#                         for desc in descendants:
#                             desc.path = desc.path.replace(old_path, new_path)
#                             session.merge(desc)          # nebo session.merge(desc)
#                     else:
#                         for desc in descendants:
#                             desc.path = desc.path.replace(old_path, str(input.id))
#                             session.merge(desc)

#                     # C) A nakonec entitu samotnou
#                     entity.path = (
#                         f"{new_parent_path}/{entity.id}"
#                         if new_parent is not None
#                         else str(entity.id)
#                     )
#                     session.merge(entity)

#                     # D) Po skončení `session.begin()` se automaticky commitne.
#                     # E) Pokud dojde k chybě, transakce se automaticky rollbackne.
#                     # await session.commit()                
#         except Exception as e:
#             return UpdateError[T](message=f"Chyba při aktualizaci: {e}", _input=input, _entity=entity)
        
#         return self.model_cls.from_dataclass(entity)