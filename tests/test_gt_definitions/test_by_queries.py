from .gt_utils import (
    createByIdTest2,
    createPageTest2,
    createInsertTest2,
    createUpdateTest2,
    createDeleteTest2,
    createTest2
)

test_digital_form_section_by_id = createByIdTest2(tableName="digital_form_sections")
test_digital_form_section_page = createPageTest2(tableName="digital_form_sections")
test_digital_form_section_insert = createInsertTest2(
    tableName="digital_form_sections", 
    variables={
        "id": "aae16f75-e76e-43a7-b0bc-556f0f6dd29d",
        "name": "new section",
        "formId": "ff9b7547-8f90-46dc-894e-ad0341a48bf8"
    })

test_digital_form_section_update = createUpdateTest2(
    tableName="digital_form_sections", 
    variables={
        "name": "new section",
        "formId": "ff9b7547-8f90-46dc-894e-ad0341a48bf8"
    })

test_digital_form_section_delete = createDeleteTest2(
    tableName="digital_form_sections",
    variables={
        "name": "new section",
        "formId": "ff9b7547-8f90-46dc-894e-ad0341a48bf8",
        "sections": [
            {
                "formId": "ff9b7547-8f90-46dc-894e-ad0341a48bf8",
                "name": "inner section",
                "fields": [
                    {
                        "formId": "ff9b7547-8f90-46dc-894e-ad0341a48bf8",
                        "name": "inner field",
                        "label": "",
                        "labelEn": "",
                        "description": "desc"
                    }
                ]
            }
        ]
    }
)

test_digital_form_by_id = createByIdTest2(tableName="digital_forms")
test_digital_form_page = createPageTest2(tableName="digital_forms")
test_digital_form_insert = createInsertTest2(
    tableName="digital_forms", 
    variables={
        "id": "aae16f75-e76e-43a7-b0bc-556f0f6dd29d",
        "name": "new form"
        
    })

test_digital_form_update = createUpdateTest2(
    tableName="digital_forms", 
    variables={
        "name": "new form",
        
    })

test_digital_form_delete = createDeleteTest2(
    tableName="digital_forms",
    variables={
        "name": "new form",
        
    }
)


test_facility_type_by_id = createByIdTest2(tableName="facilitytypes")
test_facility_type_page = createPageTest2(tableName="facilitytypes")
test_facility_type_insert = createInsertTest2(
    tableName="facilitytypes", 
    variables={
        "id": "aae16f75-e76e-43a7-b0bc-556f0f6dd29d",
        "name": "new facility",
        "typeId": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_facility_type_update = createUpdateTest2(
    tableName="facilitytypes", 
    variables={
        "name": "new facility renamed",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_facility_type_delete = createDeleteTest2(
    tableName="facilitytypes",
    variables={
        "name": "new facility",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    }
)

test_facility_by_id = createByIdTest2(tableName="facilities")
test_facility_page = createPageTest2(tableName="facilities")
test_facility_insert = createInsertTest2(
    tableName="facilities", 
    variables={
        "id": "aae16f75-e76e-43a7-b0bc-556f0f6dd29d",
        "name": "new facility",
        "typeId": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_facility_update = createUpdateTest2(
    tableName="facilities", 
    variables={
        "name": "new facility renamed",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_facility_delete = createDeleteTest2(
    tableName="facilities",
    variables={
        "name": "new facility",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    }
)


test_event_by_id = createByIdTest2(tableName="events")
test_event_page = createPageTest2(tableName="events")
test_event_insert = createInsertTest2(
    tableName="events", 
    variables={
        "id": "aae16f75-e76e-43a7-b0bc-556f0f6dd29d",
        "name": "new event",
        "typeId": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_event_update = createUpdateTest2(
    tableName="events", 
    variables={
        "name": "new event renamed",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_event_delete = createDeleteTest2(
    tableName="events",
    variables={
        "name": "new event",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    }
)

test_event_type_by_id = createByIdTest2(tableName="eventtypes")
test_event_type_page = createPageTest2(tableName="eventtypes")
test_event_type_insert = createInsertTest2(
    tableName="eventtypes", 
    variables={
        "id": "aae16f75-e76e-43a7-b0bc-556f0f6dd29d",
        "name": "new event",
        "typeId": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_event_type_update = createUpdateTest2(
    tableName="eventtypes", 
    variables={
        "name": "new event renamed",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    })

test_event_type_delete = createDeleteTest2(
    tableName="eventtypes",
    variables={
        "name": "new event",
        "type_id": "c0a12392-ae0e-11ed-9bd8-0242ac110002"
    }
)