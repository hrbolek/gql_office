import uuid

def create_DigitalSubmissionFieldInsertGQLModel(form_field, section_id, submission_id, index=0):
    from .DigitalSubmissionFieldGQLModel import DigitalSubmissionFieldInsertGQLModel
    params = {
        "field_id": form_field["field"]["id"],
        "section_id": section_id,
        "submission_id": submission_id,
        # "index": index # nepouziva se
        "value": ""
    }

    result = DigitalSubmissionFieldInsertGQLModel(**params)
    return result
    

def create_SubmissionSectionInsertGQLModel(form_section, submission_id=None, submission_section_id=None, index=0):    
    from .DigitalSubmissionSectionGQLModel import SubmissionSectionInsertGQLModel
    id = uuid.uuid4()
    params = {
        "submission_id": submission_id,
        "section_id": submission_section_id, # nepouziva se dovodi se jinde
        "form_section_id": form_section["section"]["id"],
        "index": index,
        "id": id,
        "sections": [],
        "fields": [],
    }
    
    form_section_sections = form_section["sections"]
    form_section_fields = form_section["fields"]
    result = SubmissionSectionInsertGQLModel(**params)
    result.fields = [
        create_DigitalSubmissionFieldInsertGQLModel(
            form_field=form_field,
            section_id=id,
            submission_id=submission_id,
            index=index
        )
        for (index, form_field) in enumerate(form_section_fields)]
    result_sections = []
    for form_sub_section in form_section_sections:
        repeatable_min = form_sub_section["section"]["repeatable_min"] or 0
        repeatable_max = form_sub_section["section"]["repeatable_max"] or 1
        if repeatable_max < repeatable_min:
            repeatable_max = repeatable_min
        if repeatable_max == 0:
            repeatable_max = 1
        desired = max(1, repeatable_min)
        desired = min(desired, repeatable_max)
        for index in range(desired):
            submission_sub_section = create_SubmissionSectionInsertGQLModel(
                form_section=form_sub_section,
                submission_id=submission_id,
                submission_section_id=id,
                index=index
            )
            result_sections.append(submission_sub_section)
    result.sections = result_sections
    return result
