import pytest
import logging
import typing
import uuid
import strawberry
import typing

def unwrap_type(type_):
    """
    Unwraps NON_NULL and LIST wrappers to get the base type
    """
    t = type_
    while t["kind"] in ('NON_NULL', 'LIST'):
        t = t["ofType"]
    return t


def get_read_scalar_value(schema: dict) -> dict:
    """
    Map of single‑ID query return types.

    Given a GraphQL introspection schema (as nested dictionaries/lists),
    returns a dict mapping each OBJECT return type name to the
    corresponding query field name that takes a single NON_NULL id arg.
    """
    result = {}

    # Find the Query type definition
    query_type_name = schema["queryType"]["name"]
    query_type = next(
        (t for t in schema["types"] if t["name"] == query_type_name),
        None
    )
    if not query_type:
        return result

    # Inspect each field on the Query type
    for field in query_type.get("fields", []):
        args = field.get("args", [])
        # Must have exactly one argument named "id" which is NON_NULL
        if (
            len(args) == 1
            and args[0]["name"] == "id"
            and args[0]["type"]["kind"] == "NON_NULL"
        ):
            ret_type = field.get("type", {})
            # If the return type is an OBJECT, record it
            if ret_type.get("kind") == "OBJECT":
                obj_name = ret_type["name"]
                result[obj_name] = field["name"]

    return result

def get_read_vector_value(schema: dict) -> dict:
    """
    Map of nonNull list of nonNull object queries:
    vrací slovník {Typ: názevQueryFieldu}
    """
    result = {}
    # najdi Query typ
    qtype = next((t for t in schema["types"]
                  if t["name"] == schema["queryType"]["name"]), None)
    if not qtype:
        return result

    for f in qtype.get("fields", []):
        t = f["type"]
        if t.get("kind") == "NON_NULL":
            list_t = t.get("ofType")
            if list_t and list_t.get("kind") == "LIST":
                mem = list_t.get("ofType")
                if mem and mem.get("kind") == "NON_NULL":
                    base = mem.get("ofType")
                    if base and base.get("kind") == "OBJECT":
                        result[base["name"]] = f["name"]
    return result


def get_insert_mutations(schema: dict) -> dict:
    """
    Map of insert mutations:
    hledá mutace s jediným NON_NULL argumentem INPUT_OBJECT
    bez povinného fieldu lastchange,
    vrací slovník {Typ: názevMutace}
    """
    result = {}
    mtype = next((t for t in schema["types"]
                  if t["name"] == schema["mutationType"]["name"]), None)
    if not mtype:
        return result

    for f in mtype.get("fields", []):
        args = f.get("args", [])
        if len(args) == 1 and args[0]["type"]["kind"] == "NON_NULL":
            arg_def = unwrap_type(args[0]["type"])
            if arg_def and arg_def.get("kind") == "INPUT_OBJECT":
                inp = next((t for t in schema["types"] if t["name"] == arg_def["name"]), None)
                if inp:
                    names = [i["name"] for i in inp.get("inputFields", [])]
                    # bez lastchange
                    if "lastchange" not in names:
                        ret = unwrap_type(f["type"])
                        if ret and ret.get("kind") == "UNION":
                            union_def = next((t for t in schema["types"]
                                              if t["name"] == ret["name"]), None)
                            for pt in union_def.get("possibleTypes", []):
                                if pt["kind"] == "OBJECT" and "Error" not in pt["name"]:
                                    result[pt["name"]] = f["name"]
    return result


def get_update_mutations(schema: dict) -> dict:
    """
    Map of update mutations:
    hledá mutace s jediným NON_NULL INPUT_OBJECT argumentem,
    který má >2 inputFields včetně povinných id & lastchange,
    vrací {Typ: názevMutace}
    """
    result = {}
    mtype = next((t for t in schema["types"]
                  if t["name"] == schema["mutationType"]["name"]), None)
    if not mtype:
        return result

    for f in mtype.get("fields", []):
        args = f.get("args", [])
        if len(args) == 1 and args[0]["type"]["kind"] == "NON_NULL":
            arg_def = unwrap_type(args[0]["type"])
            if arg_def and arg_def.get("kind") == "INPUT_OBJECT":
                inp = next((t for t in schema["types"] if t["name"] == arg_def["name"]), None)
                if inp and len(inp.get("inputFields", [])) > 2:
                    req = [i["name"] for i in inp["inputFields"] if i["type"]["kind"] == "NON_NULL"]
                    if "id" in req and "lastchange" in req:
                        ret = unwrap_type(f["type"])
                        if ret and ret.get("kind") == "UNION":
                            union_def = next((t for t in schema["types"]
                                              if t["name"] == ret["name"]), None)
                            for pt in union_def.get("possibleTypes", []):
                                if pt["kind"] == "OBJECT" and "Error" not in pt["name"]:
                                    result[pt["name"]] = f["name"]
    return result


def get_delete_mutations(schema: dict) -> dict:
    """
    Map of delete mutations:
    hledá mutace s jediným NON_NULL INPUT_OBJECT argumentem,
    jehož inputFields obsahují právě id & lastchange,
    a return OBJECT, kde field 'Entity' ukáže původní typ,
    vrací {Typ: názevMutace}
    """
    result = {}
    mtype = next((t for t in schema["types"]
                  if t["name"] == schema["mutationType"]["name"]), None)
    if not mtype:
        return result

    for f in mtype.get("fields", []):
        args = f.get("args", [])
        if len(args) == 1 and args[0]["type"]["kind"] == "NON_NULL":
            arg_def = unwrap_type(args[0]["type"])
            if arg_def and arg_def.get("kind") == "INPUT_OBJECT":
                inp = next((t for t in schema["types"] if t["name"] == arg_def["name"]), None)
                if inp:
                    req = [i["name"] for i in inp.get("inputFields", [])
                           if i["type"]["kind"] == "NON_NULL"]
                    if set(req) == {"id", "lastchange"}:
                        # rozbal return typ
                        ret = f["type"]
                        if ret.get("kind") == "NON_NULL":
                            ret = ret["ofType"]
                        if ret.get("kind") == "OBJECT":
                            ret_def = next((t for t in schema["types"]
                                            if t["name"] == ret["name"]), None)
                            if ret_def:
                                entity_field = next((fl for fl in ret_def["fields"]
                                                     if fl["name"] == "Entity"), None)
                                if entity_field:
                                    entity_type = unwrap_type(entity_field["type"])["name"]
                                    result[entity_type] = f["name"]
    return result


def get_cruds(schema: dict) -> dict:
    """
    Kombinuje všechny čtyři předchozí mapy a vrací
    slovník {Typ: {read, readp, insert?, update?, delete?}}
    pouze pro typy, které podporují read & readp.
    """
    single = get_read_scalar_value(schema)
    vector = get_read_vector_value(schema)
    ins = get_insert_mutations(schema)
    upd = get_update_mutations(schema)
    dele = get_delete_mutations(schema)

    cruds = {}
    for t, read_name in single.items():
        if t in vector:
            cruds[t] = {
                "read": read_name,
                "readp": vector[t],
                **({"insert": ins[t]} if t in ins else {}),
                **({"update": upd[t]} if t in upd else {}),
                **({"delete": dele[t]} if t in dele else {}),
            }
    return cruds


introspectionQuery = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    types {
      name
      description
      kind
      fields {
        name
        description
        args {
          name
          description
          type {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
      inputFields {
        name
        description
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
            }
          }
        }
      }
      possibleTypes {
        name
        kind
      }
    }
  }
}"""

def build_selection_optional(schema: dict, field_type: dict) -> str:
    """
    Builds a selection set by iterating over fields of the given object type.
    Includes only fields that have no args or only optional args.
    For fields returning OBJECT or LIST of OBJECT, nests them with `{ __typename id }`.
    """
    base = unwrap_type(field_type)
    if base.get("kind") != "OBJECT":
        return "{ __typename }"
    # find type definition
    type_def = next((t for t in schema["types"] if t.get("name") == base.get("name")), None)
    if not type_def or not type_def.get("fields"):
        logging.info(f"Type definition {type_def} failed")
        return ""

    parts = []
    for f in type_def["fields"]:
        name = f.get("name")
        if name.startswith("__"):
            continue
        args = f.get("args", [])
        # only fields without args or only optional args
        if args and any(arg["type"]["kind"] == "NON_NULL" for arg in args):
            continue
        ret_base = unwrap_type(f.get("type"))
        if ret_base.get("kind") in ["OBJECT"]:
            parts.append(f"{name} {{ __typename id }}")
        elif ret_base.get("kind") in ["UNION"]:
            parts.append(f"{name} {{ __typename }}")
        else:
            parts.append(name)
    if not parts:
        return ""
    joined = "\n  ".join(parts)
    return f"{{ {joined} }}"


def build_selection(schema: dict, field_type: dict) -> str:
    """
    Recursively builds selection set based on kind of field_type.
    """
    if not field_type or not field_type.get("kind"):
        logging.info(f"Empty field type: {field_type}")
        return ""
    kind = field_type["kind"]
    if kind == "SCALAR":
        return ""
    if kind == "OBJECT":
        return build_selection_optional(schema, field_type)
    if kind == "LIST":
        return build_selection(schema, field_type.get("ofType"))
    if kind == "NON_NULL":
        return build_selection(schema, field_type.get("ofType"))
    if kind == "UNION":
        # fallback: only __typename
        return "{ __typename }"
    # unknown: return empty
    return ""


def print_type(type_ref: dict) -> str:
    """
    Prints GraphQL type signature, handling NON_NULL and LIST.
    """
    if not type_ref:
        return ""
    kind = type_ref.get("kind")
    if kind == "NON_NULL":
        return f"{print_type(type_ref.get('ofType'))}!"
    if kind == "LIST":
        return f"[{print_type(type_ref.get('ofType'))}]"
    # SCALAR or OBJECT etc.
    return type_ref.get("name", "")


def build_input_type_params(schema: dict, input_type_name: str) -> str:
    """
    Builds parameter definitions string for given INPUT_OBJECT type.
    Outputs GraphQL variable signature, e.g.:
      ($field1: Type1!, $field2: Type2)
    """
    inp_def = next((t for t in schema["types"]
                    if t.get("name") == input_type_name and t.get("kind") == "INPUT_OBJECT"), None)
    if not inp_def or not inp_def.get("inputFields"):
        return ""
    params = []
    for field in inp_def["inputFields"]:
        raw = field.get("type")
        if raw.get("kind") == "NON_NULL":
            type_str = f"{print_type(raw.get('ofType'))}!"
        else:
            type_str = print_type(raw)
        params.append(f"${field['name']}: {type_str}")
    if not params:
        return ""
    joined = ",\n   ".join(params)
    return f"(\n   {joined}\n)"


def build_expanded_mutation(schema: dict, mutation_name: str) -> str:
    """
    Builds complete GraphQL mutation string for given mutation.
    Uses expanded individual fields as variables based on input type.
    """
    mtype = next((t for t in schema["types"] if t.get("name") == schema["mutationType"]["name"]), None)
    if not mtype:
        return ""
    field = next((f for f in mtype.get("fields", []) if f.get("name") == mutation_name), None)
    if not field or len(field.get("args", [])) != 1:
        return ""
    arg = field["args"][0]
    input_name = unwrap_type(arg.get("type")).get("name")
    param_defs = build_input_type_params(schema, input_name)
    # build call args
    inp_def = next((t for t in schema["types"] if t.get("name") == input_name), {})
    inputs = inp_def.get("inputFields", [])
    call_args = ",\n   ".join(f"{f['name']}: ${f['name']}" for f in inputs)
    # build selection
    ret_base = unwrap_type(field.get("type"))
    selection = ""
    if ret_base.get("kind") == "UNION":
        union_def = next((t for t in schema["types"] if t.get("name") == ret_base.get("name")), {})
        parts = []
        for pt in union_def.get("possibleTypes", []):
            # logging.info(f"Union {union_def} \nhas possible type: {pt}")
            # if pt.get("kind") == "OBJECT" and "Error" not in pt.get("name", ""):
            if pt.get("kind") == "OBJECT":
                sel = build_selection(schema, {"kind": "OBJECT", "name": pt.get("name")})
                parts.append(f"... on {pt['name']} {sel}")
        joined = "\n   ".join(parts)
        selection = f" {{\n   __typename\n   {joined}\n }}"
    elif ret_base.get("kind") == "OBJECT":
        sel = build_selection(schema, ret_base)
        selection = f" {sel}" if sel else ""
    return f"mutation {param_defs} {{\n  {mutation_name}({arg['name']}: {{\n   {call_args}\n  }}){selection}\n}}"


def build_query_page(schema: dict, operation_name: str) -> str:
    """
    Builds a readPage query for given type.
    """
    query_type_name = schema["queryType"]["name"]
    # logging.info(f"Query type name: {query_type_name}")
    # logging.info(f"Operation name: {operation_name}")
    query_type = next((t for t in schema["types"] if t["name"] == query_type_name), None)
    assert query_type, f"Query type {query_type_name} not found in schema"
    # logging.info(f"Query type: {query_type}")
    # logging.info(f"Query type fields: {query_type.get('fields', [])}")
    field_def = next((f for f in query_type.get("fields", []) if f["name"] == operation_name), None)
    assert field_def, f"Field {operation_name} not found in schema"
    # logging.info(f"Field def: {field_def}")
    # field_result_type = unwrap_type(field_def.get("type"))
    field_result_type = field_def.get("type")
    assert field_result_type, f"Field result type not found in schema"
    assert field_result_type.get("kind") == "NON_NULL", f"Field {operation_name} must be LIST[OBJECT!]! {field_result_type}"
    field_result_type = field_result_type.get("ofType")
    assert field_result_type, f"Field result type not found in schema"
    assert field_result_type.get("kind") == "LIST", f"Field {operation_name} must be LIST[OBJECT!]! {field_result_type}"
    list_type = field_result_type.get("ofType")
    assert list_type, f"List type not found in schema"
    assert list_type.get("kind") == "NON_NULL", f"List type is not NON_NULL {list_type}"
    type_def = list_type.get("ofType")
    assert type_def, f"Type definition not found in schema"
    assert type_def.get("kind") == "OBJECT", f"Field result type is not a LIST[OBJECT!]!"
    # find type definition
    type_def2 = next((t for t in schema["types"] if t["name"] == type_def.get("name")), None)
    assert type_def2, f"Type definition {type_def.get('name')} not found in schema"
    sel = build_selection(schema, type_def2)
    return f"query {operation_name} {{ {operation_name}{sel} }}"


def build_query_scalar(schema: dict, operation_name: str) -> str:
    """
    Builds a read(id) query for given type.
    """
    query_type_name = schema["queryType"]["name"]
    query_type = next((t for t in schema["types"] if t["name"] == query_type_name), None)
    if not query_type:
        return None
    field_def = next((f for f in query_type.get("fields", []) if f["name"] == operation_name), None)
    if not field_def:
        return None
    field_result_type = unwrap_type(field_def.get("type"))
    # logging.info(f"Field result type: {field_result_type}")
    if field_result_type.get("kind") != "OBJECT":
        return None
    # find type definition
    type_def = next((t for t in schema["types"] if t["name"] == field_result_type.get("name")), None)
    if not type_def:
        return None
    # find field definition
    
    sel = build_selection(schema, type_def)
    return f"query {operation_name}Read($id: UUID!) {{ {operation_name}(id: $id){sel} }}"

def remove_fields(entity: dict, fields: list=["__typename"]) -> dict:
    """
    Removes specified fields from the entity dictionary.
    """
    result = {}
    for key, value in entity.items():
        if key not in fields:
            if isinstance(value, dict):
                result[key] = remove_fields(value, fields)
            elif isinstance(value, list):
                result[key] = [remove_fields(item, fields) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value
    return result

async def test_page(schema, ops, executor):
    operation = ops.get("readp", None)
    query = build_query_page(schema, operation)
    logging.info(f"Querying for page test: \n{query}")
    # logging.info(f"PageQuery: {query}")
    assert query is not None, f"Query for {operation} not found in schema"
    variable_values = {}
    result = await executor(query=query, variable_values=variable_values)
    errors = result.get("errors", None)
    assert errors is None, f"Error during page execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert len(data) > 0, f"Empty response, check loader and datatable"
    return data

async def test_scalar(schema, ops, executor):
    operation = ops.get("read", None)
    [entity, *_] = await test_page(schema, ops, executor)
    query = build_query_scalar(schema, operation)
    logging.info(f"Querying for scalar test: \n{query}\nwith \n{entity}")
    assert query is not None, f"Query for {operation} not found in schema"
    variable_values = {**entity}
    result = await executor(query=query, variable_values=variable_values)
    errors = result.get("errors", None)
    assert errors is None, f"Error during scalar execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert data.get("id") == variable_values["id"], f"ID mismatch, expected {variable_values['id']} but got {data.get('id')}"

async def test_insert(schema, ops, executor):
    operation = ops.get("insert", None)
    query = build_expanded_mutation(schema, operation)
    assert query is not None, f"Mutation for {operation} not found in schema"

    [entity, *_] = await test_page(schema, ops, executor)
    variable_values = {**entity}
    # remove id and lastchange
    variable_values = remove_fields(variable_values, ["id", "lastchange", "__typename"])
    # variable_values.pop("id", None)
    # variable_values.pop("lastchange", None)
    logging.info(f"quering \n{query} \nwith \n{variable_values}")
    result = await executor(query=query, variable_values=variable_values)

    errors = result.get("errors", None)
    assert errors is None, f"Error during insert execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert "Error" not in data.get("__typename", ""), f"{operation} returned {data}"
    return data

async def test_update(schema, ops, executor):
    operation = ops.get("update", None)
    query = build_expanded_mutation(schema, operation)
    assert query is not None, f"Mutation for {operation} not found in schema"
    
    # get entity for update
    entity = await test_insert(schema, ops, executor)
    # variable_values = {**entity}
    variable_values = remove_fields(entity, ["__typename"])
    result = await executor(query=query, variable_values=variable_values)

    errors = result.get("errors", None)
    assert errors is None, f"Error during update execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert "Error" not in data.get("__typename", ""), f"{operation} returned {data}"
    return data

async def test_delete(schema, ops, executor):
    operation = ops.get("delete", None)
    query = build_expanded_mutation(schema, operation)
    assert query is not None, f"Mutation for {operation} not found in schema"

    entity = await test_insert(schema, ops, executor)
    variable_values = {"id": entity["id"], "lastchange": entity["lastchange"]}
    result = await executor(query=query, variable_values=variable_values)

    errors = result.get("errors", None)
    assert errors is None, f"Error during delete execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is None, f"Expected empty response after delete, got {data}"
    return data

def createTests(schema):
    import strawberry
    s : strawberry.federation.Schema = schema
    extensions = schema.extensions
    schema.extensions = []
    introspection = s.execute_sync(introspectionQuery)
    schema.extensions = extensions
    # logging.info(f"Introspection result: {introspection}")
    __schema = introspection.data["__schema"]
    # logging.info(f"Schema: {[key for key in __schema.keys()]}")
    # queryType = __schema.get("queryType", None)
    # queryTypeDef = next((t for t in __schema["types"] if t["name"] == queryType["name"]), None)
    # queryTypeFields = queryTypeDef.get("fields", [])
    
    # logging.info(f"Query type fields: {queryTypeFields}")
    cruds = get_cruds(__schema)

    def create_particular_test(__schema, typename, optype, ops):
        @pytest.mark.asyncio
        async def test_func(SchemaExecutor):
            executor = SchemaExecutor
            if optype == "readp":
                return await test_page(__schema, ops, executor)
            elif optype == "read":
                return await test_scalar(__schema, ops, executor)
            elif optype == "insert":
                return await test_insert(__schema, ops, executor)
            elif optype == "update":
                return await test_update(__schema, ops, executor)
            elif optype == "delete":
                return await test_delete(__schema, ops, executor)
            else:
                raise ValueError(f"Operation {typename} not found in schema")
        return test_func
    result = {}
    for typename, ops in cruds.items():
        for optype, opname in ops.items():
            test = create_particular_test(__schema, typename, optype, ops)
            print(f"Creating test {optype} for {typename}")
            logging.info(f"Creating test {optype} for {typename} {opname}")
            test.__name__ = f"test_{optype}_{typename}"
            globals()[f"test_{optype}_{typename}"] = test
            result[f"test_{optype}_{typename}"] = test
    return result
        

def createResolveTest(schema, types: typing.Dict[str, typing.List[uuid.UUID]]):

    extensions = schema.extensions
    schema.extensions = []
    introspection = schema.execute_sync(introspectionQuery)
    schema.extensions = extensions
    # logging.info(f"Introspection result: {introspection}")
    __schema = introspection.data["__schema"]

    query = build_entities_query(__schema)
    logging.info(f"Entities query: {query}")
    assert query is not None, f"Unable to build entities query"
    
    @pytest.mark.asyncio
    async def test_result(SchemaExecutor):
        executor = SchemaExecutor
        variable_values = {
            "representations": [{"__typename": typename, "id": str(id)} for typename, ids in types.items() for id in ids]
        }
        logging.info(f"Querying for entities: \n{query}\nwith \n{variable_values}")
        result = await executor(query=query, variable_values=variable_values)
        errors = result.get("errors", None)
        assert errors is None, f"Error during entities execution {errors}"
        data = result.get("data", None)
        assert data is not None, f"Empty response, check loader and datatable"
        data = data.get("_entities", None)
        assert data is not None, f"Empty response, check loader and datatable"
        assert len(data) > 0, f"Empty response, check loader and datatable"
        return data
    test_result.__name__ = "test_entities"
    return test_result



def build_entities_query(schema: dict) -> str:
    """
    Builds a federated _entities query selecting all types from the _Entity union.
    Uses build_selection_optional to derive fragment selection.
    Returns a parameterized GraphQL query string.
    """
    # Find the __Entity union definition

    id_nullability = dict()
    for t in schema['types']:
        if t['kind'] == 'OBJECT' and t.get('fields'):
            idf = next((f for f in t['fields'] if f['name'] == 'id'), None)
            if idf:
                # walk through NON_NULL/LIST wrappers to get base kind
                def unwrap_kind(typ):
                    if typ['kind'] in ('NON_NULL', 'LIST'):
                        return f"{typ['kind']}({unwrap_kind(typ['ofType'])})"
                    return typ['name']
                chain = unwrap_kind(idf['type'])
                if not chain in id_nullability:
                    id_nullability[chain] = []
                # add to list of types with this id type
                id_nullability[chain].append(t['name'])

    # now print out groups
    logging.info("ID field definitions by nullability:\n")
    for chain, names in id_nullability.items():
        logging.info(f"  {chain} (i.e. {chain.replace('NON_NULL(', '').replace(')', '')}{'!' if 'NON_NULL' in chain else ''}):")
        for n in names:
            logging.info(f"    – {n}")
        logging.info("\n")


    entity_union = next((t for t in schema.get("types", []) if t.get("name") == "_Entity"), None)
    if not entity_union:
        logging.info(f"{[t for t in schema.get('types', []) if 'ntity' in t.get('name')]}")
        return None
    fragments = []
    for pt in entity_union.get("possibleTypes", []):
        type_name = pt.get("name")
        # Build selection for this type, defaulting to id if none
        sel = build_selection_optional(schema, {"kind": "OBJECT", "name": type_name})
        # sel = build_selection(schema, {"kind": "OBJECT", "name": type_name})
        if not sel.strip():
            sel = "{ __typename id }"
        fragments.append(f"... on {type_name} {sel}")
    fragment_block = "\n    ".join(fragments)
    return (
        "query($representations: [_Any!]!) {\n"
        "  _entities(representations: $representations) {\n"
        f"    {fragment_block}\n"
        "  }\n"
        "}"
    )
