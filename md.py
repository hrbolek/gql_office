from src.GraphTypeDefinitions import schema

schema.extensions = []
MD_FILE_PATH = "./graphql_schema.md"


def extract_type_name(field_type):
    """Vrátí správný název typu včetně podpory List[], NonNull! a dalších.
    Returns the correct type name, including support for List[], NonNull!, and more."""

    while field_type:
        kind = field_type.get("kind", "")
        name = field_type.get("name")

        if kind == "LIST" and field_type.get("ofType"):
            return f"List[{extract_type_name(field_type['ofType'])}]"

        if kind == "NON_NULL" and field_type.get("ofType"):
            return f"{extract_type_name(field_type['ofType'])}!"

        if name:
            return name  # Jakmile najdeme platný název, vrátíme ho

        field_type = field_type.get("ofType")  # Posuneme se hlouběji

    return "Unknown"

def generate_markdown_from_schema():   
    """Generuje Markdown dokumentaci z introspektovaného GraphQL schématu.
    Generates Markdown documentation from the introspected GraphQL schema."""

    INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    types {
      name
      description
      fields {
        name
        description
        type {
          name
          kind
          ofType {
            name
            kind
            ofType {
              name
              kind
              ofType {
                name
                kind
                ofType {
                  name
                  kind
                }
              }
            }
          }
        }
      }
    }
  }
}
    """    

    # Spustíme introspekční dotaz přímo nad objektem `schema`
    result = schema.execute_sync(INTROSPECTION_QUERY)
    
    if result.errors:
        raise Exception(f"GraphQL introspection failed: {result.errors}")

    schema_data = result.data

    markdown_content = "# GraphQL API Documentation\n\n"

    for gql_type in schema_data["__schema"]["types"]:
        if gql_type["name"].startswith("__"):  # Přeskakujeme interní GraphQL typy
            continue

        description = gql_type["description"] or "No description available."
        markdown_content += f"## {gql_type['name']}\n\n"
        markdown_content += description.replace("\n", "  \n") + "\n\n"  # Zachování zalomení řádků

        if gql_type.get("fields"):
            markdown_content += "### Fields:\n\n"
            for field in gql_type["fields"]:
                field_name = field["name"]
                field_desc = (field["description"] or "No description available.").replace("\n", "  \n")
                field_type = extract_type_name(field["type"])
                
                markdown_content += f"- **{field_name}** (`{field_type}`): \n\n    {field_desc}\n"

        markdown_content += "\n---\n"

    return markdown_content

# from graphql import get_introspection_query
# introspection_query = get_introspection_query(descriptions=True)

# def format_type(type_ref):
#     """
#     Rekurzivně převede GraphQL type reference na textovou reprezentaci.
#     Např. NON_NULL => "Typ!" a LIST => "[Typ]".
#     """
#     if type_ref is None:
#         return ""
#     kind = type_ref.get("kind")
#     if kind == "NON_NULL":
#         return f"{format_type(type_ref.get('ofType'))}!"
#     elif kind == "LIST":
#         return f"[{format_type(type_ref.get('ofType'))}]"
#     else:
#         return type_ref.get("name") or ""

# def markdown_for_field(field):
#     """
#     Vytvoří Markdown řádek pro pole (field) v objektu nebo query/mutation.
#     Zahrnuje název, typ a případně popis a argumenty.
#     """
#     s = f"- **{field['name']}**: `{format_type(field['type'])}`"
#     if field.get("description"):
#         s += f" – {field['description']}"
#     if field.get("args"):
#         if len(field["args"]) > 0:
#             s += "\n  - **Arguments:**"
#             for arg in field["args"]:
#                 s += f"\n    - **{arg['name']}**: `{format_type(arg['type'])}`"
#                 if arg.get("description"):
#                     s += f" – {arg['description']}"
#     return s

# def markdown_for_input_field(field):
#     """
#     Vytvoří Markdown řádek pro vstupní pole (input field).
#     """
#     s = f"- **{field['name']}**: `{format_type(field['type'])}`"
#     if field.get("description"):
#         s += f" – {field['description']}"
#     return s

# def markdown_for_object_type(type_obj):
#     """
#     Vygeneruje Markdown popis pro objektový typ (fields, popis).
#     """
#     s = f"#### {type_obj['name']}\n\n"
#     if type_obj.get("description"):
#         s += f"{type_obj['description']}\n\n"
#     if type_obj.get("fields"):
#         s += "Fields:\n"
#         for field in type_obj["fields"]:
#             s += markdown_for_field(field) + "\n"
#         s += "\n"
#     return s

# def markdown_for_input_object_type(type_obj):
#     """
#     Vygeneruje Markdown popis pro vstupní objekt.
#     """
#     s = f"#### {type_obj['name']}\n\n"
#     if type_obj.get("description"):
#         s += f"{type_obj['description']}\n\n"
#     if type_obj.get("inputFields"):
#         s += "Input Fields:\n"
#         for field in type_obj["inputFields"]:
#             s += markdown_for_input_field(field) + "\n"
#         s += "\n"
#     return s

# def markdown_for_scalar_type(type_obj):
#     """
#     Vygeneruje Markdown popis pro skalární typ.
#     """
#     s = f"#### {type_obj['name']}\n\n"
#     if type_obj.get("description"):
#         s += f"{type_obj['description']}\n\n"
#     return s


# # --- Hlavní funkce, která provede introspekci a vygeneruje Markdown dokumentaci ---

# def generate_markdown_from_schema2():
#     # Provedeme introspekci schématu
#     # introspection_query = get_introspection_query(descriptions=True)
#     result = schema.execute_sync(introspection_query)
#     if result.errors:
#         print("Chyby při introspekci:", result.errors)
#         return

#     schema_data = result.data["__schema"]
#     types = schema_data["types"]

#     # Zjistíme názvy query a mutation typů
#     query_type_name = schema_data["queryType"]["name"] if schema_data.get("queryType") else None
#     mutation_type_name = schema_data["mutationType"]["name"] if schema_data.get("mutationType") else None

#     query_type = None
#     mutation_type = None
#     scalars = []
#     inputs = []
#     objects = []

#     # Rozřadíme typy do kategorií (ignorujeme interní typy začínající "__")
#     for t in types:
#         if t["name"].startswith("__"):
#             continue
#         if t["name"] == query_type_name:
#             query_type = t
#         elif t["name"] == mutation_type_name:
#             mutation_type = t
#         elif t["kind"] == "SCALAR":
#             scalars.append(t)
#         elif t["kind"] == "INPUT_OBJECT":
#             inputs.append(t)
#         elif t["kind"] == "OBJECT":
#             objects.append(t)

#     markdown = "# GraphQL Schema Documentation\n\n"

#     # Sekce Query a Mutation
#     markdown += "## Query a Mutation\n\n"
#     if query_type:
#         markdown += f"### Query: {query_type['name']}\n\n"
#         if query_type.get("description"):
#             markdown += f"{query_type['description']}\n\n"
#         if query_type.get("fields"):
#             markdown += "Fields:\n"
#             for field in query_type["fields"]:
#                 markdown += markdown_for_field(field) + "\n"
#         markdown += "\n"

#     if mutation_type:
#         markdown += f"### Mutation: {mutation_type['name']}\n\n"
#         if mutation_type.get("description"):
#             markdown += f"{mutation_type['description']}\n\n"
#         if mutation_type.get("fields"):
#             markdown += "Fields:\n"
#             for field in mutation_type["fields"]:
#                 markdown += markdown_for_field(field) + "\n"
#         markdown += "\n"

#     # Sekce Skaláry
#     markdown += "## Skaláry\n\n"
#     for scalar in scalars:
#         markdown += markdown_for_scalar_type(scalar)

#     # Sekce Vstupní typy (inputs)
#     markdown += "## Vstupní typy\n\n"
#     for input_obj in inputs:
#         markdown += markdown_for_input_object_type(input_obj)

#     # Sekce Regulérní typy (objects)
#     markdown += "## Regulérní typy\n\n"
#     for obj in objects:
#         # Vynecháme již zpracované query a mutation typy
#         if obj["name"] in [query_type_name, mutation_type_name]:
#             continue
#         markdown += markdown_for_object_type(obj)
#     return markdown

# from graphql import get_introspection_query
# introspection_query = get_introspection_query(descriptions=True)

# def format_type(type_ref):
#     """
#     Recursively converts a GraphQL type reference into its text representation.
#     For NON_NULL, returns "Type!" and for LIST returns "[Type]".
#     For a named type, wraps the type name in a Markdown link to its documentation section.
#     """
#     if type_ref is None:
#         return ""
#     kind = type_ref.get("kind")
#     if kind == "NON_NULL":
#         return f"{format_type(type_ref.get('ofType'))}!"
#     elif kind == "LIST":
#         return f"[{format_type(type_ref.get('ofType'))}]"
#     else:
#         type_name = type_ref.get("name") or ""
#         if type_name:
#             # Optionally, you might exclude built-in scalars from linking:
#             built_in_scalars = {"String", "Int", "Float", "Boolean", "ID"}
#             if type_name in built_in_scalars:
#                 return type_name
#             # Generate a link using a simple slug (lower-case the type name)
#             anchor = type_name.lower()
#             return f"[{type_name}](#{anchor})"
#         else:
#             return ""

# def markdown_for_field(field):
#     """
#     Creates a Markdown line for a field in an object or query/mutation.
#     Includes the field name, its type (with a link if applicable), description, and arguments.
#     """
#     s = f"- **{field['name']}**: {format_type(field['type'])}"
#     if field.get("description"):
#         s += f" – {field['description']}"
#     if field.get("args"):
#         if len(field["args"]) > 0:
#             s += "\n  - **Arguments:**"
#             for arg in field["args"]:
#                 s += f"\n    - **{arg['name']}**: {format_type(arg['type'])}"
#                 if arg.get("description"):
#                     s += f" – {arg['description']}"
#     return s

# def markdown_for_input_field(field):
#     """
#     Creates a Markdown line for an input field.
#     """
#     s = f"- **{field['name']}**: {format_type(field['type'])}"
#     if field.get("description"):
#         s += f" – {field['description']}"
#     return s

# def markdown_for_object_type(type_obj):
#     """
#     Generates Markdown documentation for an object type (its fields and description).
#     """
#     s = f"#### {type_obj['name']}\n\n"
#     if type_obj.get("description"):
#         s += f"{type_obj['description']}\n\n"
#     if type_obj.get("fields"):
#         s += "Fields:\n"
#         for field in type_obj["fields"]:
#             s += markdown_for_field(field) + "\n"
#         s += "\n"
#     return s

# def markdown_for_input_object_type(type_obj):
#     """
#     Generates Markdown documentation for an input object type.
#     """
#     s = f"#### {type_obj['name']}\n\n"
#     if type_obj.get("description"):
#         s += f"{type_obj['description']}\n\n"
#     if type_obj.get("inputFields"):
#         s += "Input Fields:\n"
#         for field in type_obj["inputFields"]:
#             s += markdown_for_input_field(field) + "\n"
#         s += "\n"
#     return s

# def markdown_for_scalar_type(type_obj):
#     """
#     Generates Markdown documentation for a scalar type.
#     """
#     s = f"#### {type_obj['name']}\n\n"
#     if type_obj.get("description"):
#         s += f"{type_obj['description']}\n\n"
#     return s

# # --- Main function that performs introspection and generates Markdown documentation ---

# def generate_markdown_from_schema2():
#     # Perform schema introspection
#     result = schema.execute_sync(introspection_query)
#     if result.errors:
#         print("Errors during introspection:", result.errors)
#         return

#     schema_data = result.data["__schema"]
#     types = schema_data["types"]

#     # Get the names for query and mutation types
#     query_type_name = schema_data["queryType"]["name"] if schema_data.get("queryType") else None
#     mutation_type_name = schema_data["mutationType"]["name"] if schema_data.get("mutationType") else None

#     query_type = None
#     mutation_type = None
#     scalars = []
#     inputs = []
#     objects = []

#     # Categorize types (ignore internal types that start with "__")
#     for t in types:
#         if t["name"].startswith("__"):
#             continue
#         if t["name"] == query_type_name:
#             query_type = t
#         elif t["name"] == mutation_type_name:
#             mutation_type = t
#         elif t["kind"] == "SCALAR":
#             scalars.append(t)
#         elif t["kind"] == "INPUT_OBJECT":
#             inputs.append(t)
#         elif t["kind"] == "OBJECT":
#             objects.append(t)

#     markdown = "# GraphQL Schema Documentation\n\n"

#     # Section for Query and Mutation
#     markdown += "## Query a Mutation\n\n"
#     if query_type:
#         markdown += f"### Query: {query_type['name']}\n\n"
#         if query_type.get("description"):
#             markdown += f"{query_type['description']}\n\n"
#         if query_type.get("fields"):
#             markdown += "Fields:\n"
#             for field in query_type["fields"]:
#                 markdown += markdown_for_field(field) + "\n"
#         markdown += "\n"

#     if mutation_type:
#         markdown += f"### Mutation: {mutation_type['name']}\n\n"
#         if mutation_type.get("description"):
#             markdown += f"{mutation_type['description']}\n\n"
#         if mutation_type.get("fields"):
#             markdown += "Fields:\n"
#             for field in mutation_type["fields"]:
#                 markdown += markdown_for_field(field) + "\n"
#         markdown += "\n"

#     # Section for Scalars
#     markdown += "## Skaláry\n\n"
#     for scalar in scalars:
#         markdown += markdown_for_scalar_type(scalar)

#     # Section for Input Types
#     markdown += "## Vstupní typy\n\n"
#     for input_obj in inputs:
#         markdown += markdown_for_input_object_type(input_obj)

#     # Section for Regular (Object) Types
#     markdown += "## Regulérní typy\n\n"
#     for obj in objects:
#         # Skip the already processed query and mutation types
#         if obj["name"] in [query_type_name, mutation_type_name]:
#             continue
#         markdown += markdown_for_object_type(obj)
#     return markdown

from graphql import get_introspection_query
introspection_query = get_introspection_query(descriptions=True)

def format_type(type_ref):
    if type_ref is None:
        return ""
    kind = type_ref.get("kind")
    if kind == "NON_NULL":
        return f"{format_type(type_ref.get('ofType'))}!"
    elif kind == "LIST":
        return f"[{format_type(type_ref.get('ofType'))}]"
    else:
        type_name = type_ref.get("name") or ""
        if type_name:
            built_in_scalars = {"String", "Int", "Float", "Boolean", "ID"}
            if type_name in built_in_scalars:
                return type_name
            anchor = type_name.lower()
            return f"[{type_name}](#{anchor})"
        else:
            return ""

def markdown_for_field(field):
    s = f"- **{field['name']}**: {format_type(field['type'])}"
    if field.get("description"):
        s += f" – {field['description']}"
    if field.get("args"):
        if len(field["args"]) > 0:
            s += "\n  - **Arguments:**"
            for arg in field["args"]:
                s += f"\n    - **{arg['name']}**: {format_type(arg['type'])}"
                if arg.get("description"):
                    s += f" – {arg['description']}"
    return s

def markdown_for_input_field(field):
    s = f"- **{field['name']}**: {format_type(field['type'])}"
    if field.get("description"):
        s += f" – {field['description']}"
    return s

def markdown_for_object_type(type_obj):
    s = f"#### {type_obj['name']}\n\n"
    if type_obj.get("description"):
        s += f"{type_obj['description']}\n\n"
    if type_obj.get("fields"):
        s += "Fields:\n"
        for field in type_obj["fields"]:
            s += markdown_for_field(field) + "\n"
        s += "\n"
    return s

def markdown_for_input_object_type(type_obj):
    s = f"#### {type_obj['name']}\n\n"
    if type_obj.get("description"):
        s += f"{type_obj['description']}\n\n"
    if type_obj.get("inputFields"):
        s += "Input Fields:\n"
        for field in type_obj["inputFields"]:
            s += markdown_for_input_field(field) + "\n"
        s += "\n"
    return s

def markdown_for_scalar_type(type_obj):
    s = f"#### {type_obj['name']}\n\n"
    if type_obj.get("description"):
        s += f"{type_obj['description']}\n\n"
    return s

def get_named_type(type_ref):
    while type_ref.get("ofType"):
        type_ref = type_ref["ofType"]
    return type_ref

def variable_type_string(type_ref):
    if type_ref is None:
        return ""
    kind = type_ref.get("kind")
    if kind == "NON_NULL":
        return f"{variable_type_string(type_ref.get('ofType'))}!"
    elif kind == "LIST":
        return f"[{variable_type_string(type_ref.get('ofType'))}]"
    else:
        return type_ref.get("name") or ""

def generate_variable_definitions(args, types_by_name):
    var_defs = []
    for arg in args:
        if arg["name"] == "where":
            var_defs.append(f'${arg["name"]}: {variable_type_string(arg["type"])}')
        else:
            named = get_named_type(arg["type"])
            if named.get("kind") == "INPUT_OBJECT":
                input_def = types_by_name.get(named.get("name"))
                if input_def and input_def.get("inputFields"):
                    for field in input_def["inputFields"]:
                        var_defs.append(f'${arg["name"]}_{field["name"]}: {variable_type_string(field["type"])}')
                else:
                    var_defs.append(f'${arg["name"]}: {variable_type_string(arg["type"])}')
            else:
                var_defs.append(f'${arg["name"]}: {variable_type_string(arg["type"])}')
    return var_defs

def generate_field_arguments(args, types_by_name):
    parts = []
    for arg in args:
        if arg["name"] == "where":
            parts.append(f'{arg["name"]}: ${arg["name"]}')
        else:
            named = get_named_type(arg["type"])
            if named.get("kind") == "INPUT_OBJECT":
                input_def = types_by_name.get(named.get("name"))
                if input_def and input_def.get("inputFields"):
                    fields = []
                    for field in input_def["inputFields"]:
                        fields.append(f'{field["name"]}: ${arg["name"]}_{field["name"]}')
                    obj_str = "{" + ", ".join(fields) + "}"
                    parts.append(f'{arg["name"]}: {obj_str}')
                else:
                    parts.append(f'{arg["name"]}: ${arg["name"]}')
            else:
                parts.append(f'{arg["name"]}: ${arg["name"]}')
    if parts:
        return "(" + ", ".join(parts) + ")"
    else:
        return ""

def get_fragment_name(type_name):
    # Custom mapping: remove "GQLModel" suffix for success branch,
    # map types with "UpdateError" to "Error".
    if type_name.endswith("GQLModelUpdateError"):
        return "Error"
    elif type_name.endswith("GQLModel"):
        return type_name[:-len("GQLModel")]
    else:
        return type_name

def get_fragment_name(type_name):
    # Map "GQLModelUpdateError" types to "Error" and remove "GQLModel" suffix otherwise.
    if type_name.endswith("GQLModelUpdateError"):
        return "Error"
    elif type_name.endswith("GQLModel"):
        return type_name[:-len("GQLModel")]
    else:
        return type_name

def generate_selection_set_with_fragments(type_ref, types_by_name, fragments, depth=0, max_depth=2, indent_level=1, indent_str="  "):
    base = get_named_type(type_ref)
    # Handle UNION types: always generate an inline fragment for each possible member.
    if base.get("kind") == "UNION":
        possible_types = base.get("possibleTypes")
        if not possible_types:
            union_def = types_by_name.get(base.get("name"))
            possible_types = union_def.get("possibleTypes", []) if union_def else []
        union_lines = []
        for possible in possible_types:
            possible_name = possible.get("name")
            if possible_name not in fragments:
                _ = generate_selection_set_with_fragments(possible, types_by_name, fragments, depth+1, max_depth, indent_level+1, indent_str)
            inline_fragment = f"... on {possible_name} {{ ...{get_fragment_name(possible_name)} }}"
            union_lines.append(indent_str * indent_level + inline_fragment)
        if union_lines:
            union_block = "{\n" + "\n".join(union_lines) + "\n" + indent_str * (indent_level - 1) + "}"
            return union_block
        else:
            return ""
    elif base.get("kind") != "OBJECT":
        return ""
    if depth >= max_depth:
        return "{ __typename, id }"
    type_name = base.get("name")
    if type_name not in fragments:
        type_def = types_by_name.get(type_name)
        if not type_def or "fields" not in type_def:
            fragment_body = "{ __typename, id }"
        else:
            fragment_lines = []
            # Always include __typename first.
            fragment_lines.append(indent_str * indent_level + "__typename")
            for f in type_def["fields"]:
                f_type = f["type"]
                f_named = get_named_type(f_type)
                if f_named.get("kind") in ["OBJECT", "UNION"]:
                    if depth + 1 < max_depth:
                        _ = generate_selection_set_with_fragments(f_type, types_by_name, fragments, depth + 1, max_depth, indent_level + 1, indent_str)
                        fragment_lines.append(indent_str * indent_level + f"{f['name']} {{ ...{get_fragment_name(f_named.get('name'))} }}")
                    else:
                        fragment_lines.append(indent_str * indent_level + f"{f['name']} {{ id }}")
                else:
                    fragment_lines.append(indent_str * indent_level + f"{f['name']}")
            fragment_body = "{\n" + "\n".join(fragment_lines) + "\n" + indent_str * (indent_level - 1) + "}"
        fragment_def = f"fragment {get_fragment_name(type_name)} on {type_name} {fragment_body}"
        fragments[type_name] = fragment_def
    return "{\n" + indent_str + f"...{get_fragment_name(type_name)}\n}}"



def generate_query_example(field, types_by_name, operation_type="query", max_depth=2):
    # For mutations, use a higher recursion depth.
    if operation_type == "mutation":
        max_depth = 3
    args = field.get("args") or []
    var_defs = generate_variable_definitions(args, types_by_name)
    var_defs_str = ""
    if var_defs:
        var_defs_str = "(" + ", ".join(var_defs) + ")"
    field_args = generate_field_arguments(args, types_by_name)
    fragments = {}
    selection_set = ""
    base = get_named_type(field["type"])
    if base.get("kind") in ["OBJECT", "UNION"]:
        selection_set = generate_selection_set_with_fragments(field["type"], types_by_name, fragments, depth=0, max_depth=max_depth, indent_level=1, indent_str="  ")
        if not selection_set.strip().startswith("{"):
            selection_set = "{\n    " + selection_set.strip() + "\n  }"
    else:
        selection_set = ""
    if operation_type == "mutation" and not selection_set:
        selection_set = "{ __typename, id }"
    lines = []
    lines.append(f"{operation_type} Example{var_defs_str} {{")
    if selection_set:
        lines.append(f"  {field['name']}{field_args} {selection_set}")
    else:
        lines.append(f"  {field['name']}{field_args}")
    lines.append("}")
    query = "\n".join(lines)
    if fragments:
        fragments_text = "\n\n".join(fragments[frag] for frag in fragments)
        query += "\n\n" + fragments_text
    return query

def generate_markdown_from_schema2():
    result = schema.execute_sync(introspection_query)
    if result.errors:
        print("Errors during introspection:", result.errors)
        return
    schema_data = result.data["__schema"]
    types = schema_data["types"]
    types_by_name = {}
    for t in types:
        if t["name"].startswith("__"):
            continue
        types_by_name[t["name"]] = t
    query_type_name = schema_data["queryType"]["name"] if schema_data.get("queryType") else None
    mutation_type_name = schema_data["mutationType"]["name"] if schema_data.get("mutationType") else None
    query_type = None
    mutation_type = None
    scalars = []
    inputs = []
    objects = []
    for t in types:
        if t["name"].startswith("__"):
            continue
        if t["name"] == query_type_name:
            query_type = t
        elif t["name"] == mutation_type_name:
            mutation_type = t
        elif t["kind"] == "SCALAR":
            scalars.append(t)
        elif t["kind"] == "INPUT_OBJECT":
            inputs.append(t)
        elif t["kind"] == "OBJECT":
            objects.append(t)
    markdown = "# GraphQL Schema Documentation\n\n"
    markdown += "## Query a Mutation\n\n"
    if query_type:
        markdown += f"### Query: {query_type['name']}\n\n"
        if query_type.get("description"):
            markdown += f"{query_type['description']}\n\n"
        if query_type.get("fields"):
            markdown += "#### Fields\n\n"
            for field in query_type["fields"]:
                markdown += markdown_for_field(field) + "\n\n"
                example = generate_query_example(field, types_by_name, operation_type="query")
                markdown += "Example usage:\n\n```graphql\n" + example + "\n```\n\n"
        markdown += "\n"
    if mutation_type:
        markdown += f"### Mutation: {mutation_type['name']}\n\n"
        if mutation_type.get("description"):
            markdown += f"{mutation_type['description']}\n\n"
        if mutation_type.get("fields"):
            markdown += "#### Fields\n\n"
            for field in mutation_type["fields"]:
                markdown += markdown_for_field(field) + "\n\n"
                example = generate_query_example(field, types_by_name, operation_type="mutation")
                markdown += "Example usage:\n\n```graphql\n" + example + "\n```\n\n"
        markdown += "\n"
    markdown += "## Scalars\n\n"
    for scalar in scalars:
        markdown += markdown_for_scalar_type(scalar)
    markdown += "## Input Types\n\n"
    for input_obj in inputs:
        markdown += markdown_for_input_object_type(input_obj)
    markdown += "## Regular Types\n\n"
    for obj in objects:
        if obj["name"] in [query_type_name, mutation_type_name]:
            continue
        markdown += markdown_for_object_type(obj)
    return markdown

# Example usage:
# md_documentation = generate_markdown_from_schema2()
# with open("schema_documentation.md", "w", encoding="utf-8") as f:
#     f.write(md_documentation)


def unwrap_type(type_obj):
    """
    Rekurzivně "rozbalí" typ, aby získal základní pojmenovaný typ.
    Například NON_NULL nebo LIST obalí skutečný typ, který nás zajímá.
    """
    while type_obj and type_obj.get("ofType"):
        type_obj = type_obj["ofType"]
    return type_obj

def create_dot():
    

    result = schema.execute_sync(introspection_query)
    if result.errors:
        print("Chyby při introspekci:", result.errors)
        return

    schema_data = result.data["__schema"]
    types = schema_data["types"]


    # Vybereme pouze objektové typy, které nejsou systémové (nezačínají "__")
    entities = {t["name"]: t for t in types if t["kind"] == "OBJECT" and not t["name"].startswith("__")}

    # Budeme uchovávat vztahy ve formě: (zdroj, cíl) -> množina názvů polí
    edges = {}
    for entity_name, entity in entities.items():
        fields = entity.get("fields", [])
        for field in fields:
            named_type = unwrap_type(field["type"])
            if not named_type:
                continue
            target_name = named_type.get("name")
            # Pokud cílový typ je také objekt (entita) v našem schématu, vytvoříme vztah.
            if target_name in entities:
                key = (entity_name, target_name)
                if key not in edges:
                    edges[key] = set()
                edges[key].add(field["name"])

    # Generujeme obsah DOT souboru
    dot_lines = []
    dot_lines.append("digraph G {")
    dot_lines.append("  node [shape=rectangle];")
    # Vykreslíme všechny entity jako uzly
    for entity_name in entities:
        dot_lines.append(f'  "{entity_name}";')
    dot_lines.append("")  # prázdný řádek pro přehlednost

    # Vykreslíme vztahy (šipky) mezi entitami s popiskem obsahujícím názvy polí
    for (src, tgt), field_names in edges.items():
        label = ", ".join(sorted(field_names))
        dot_lines.append(f'  "{src}" -> "{tgt}" [label="{label}"];')
    dot_lines.append("}")

    return "\n".join(dot_lines)

    print(f"DOT file generated: {output_file}")

markdown_content = generate_markdown_from_schema()
with open(MD_FILE_PATH, "w", encoding="utf-8") as md_file:
    md_file.write(markdown_content)

markdown_content = generate_markdown_from_schema2()
# with open(MD_FILE_PATH + ".md", "w", encoding="utf-8") as md_file:
with open(MD_FILE_PATH, "w", encoding="utf-8") as md_file:    
    md_file.write(markdown_content)

output_file = ".schema.dot"
dot_lines = create_dot()
with open(output_file, "w", encoding="utf-8") as f:
    f.write(dot_lines)
