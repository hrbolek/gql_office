# GraphQL Schema Documentation

## Query a Mutation

### Query: Query

#### Fields

- **_entities**: [[_Entity](#_entity)]!
  - **Arguments:**
    - **representations**: [[_Any](#_any)!]!

Example usage:

```graphql
query Example($representations: [_Any!]!) {
  _entities(representations: $representations) {
  ... on FacilityGQLModel { ...Facility }
  ... on GroupGQLModel { ...Group }
  ... on RBACObjectGQLModel { ...RBACObject }
  ... on UserGQLModel { ...User }
}
}

fragment Facility on FacilityGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    label
    startdate
    enddate
    address
    valid
    capacity
    geometry
    geolocation
    groupId
    facilitytypeId
    masterFacilityId
    type { id }
    masterFacility { id }
    masterFacilities { id }
    subFacilities { id }
    group { id }
  }

fragment Group on GroupGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment User on UserGQLModel {
    __typename
    id
  }
```

- **_service**: [_Service](#_service)!

Example usage:

```graphql
query Example {
  _service {
  ..._Service
}
}

fragment _Service on _Service {
  __typename
  sdl
}
```

- **eventById**: [EventGQLModel](#eventgqlmodel) – get a event by its id
  - **Arguments:**
    - **id**: [UUID](#uuid)!

Example usage:

```graphql
query Example($id: UUID!) {
  eventById(id: $id) {
  ...Event
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment EventType on EventTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    parentId
    parent { id }
    children { id }
    events { id }
  }

fragment EventInvitation on EventInvitationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    eventId
    userId
    stateId
    event { id }
    user { id }
    state { id }
  }

fragment Event on EventGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  description
  startDate
  endDate
  parentId
  parent { id }
  children { id }
  typeId
  type { ...EventType }
  invitations { ...EventInvitation }
}
```

- **eventPage**: [[EventGQLModel](#eventgqlmodel)!]! – get a page of events
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [EventInputFilter](#eventinputfilter)

Example usage:

```graphql
query Example($skip: Int, $limit: Int, $orderby: String, $where: EventInputFilter) {
  eventPage(skip: $skip, limit: $limit, orderby: $orderby, where: $where) {
  ...Event
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment EventType on EventTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    parentId
    parent { id }
    children { id }
    events { id }
  }

fragment EventInvitation on EventInvitationGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    eventId
    userId
    stateId
    event { id }
    user { id }
    state { id }
  }

fragment Event on EventGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  description
  startDate
  endDate
  parentId
  parent { id }
  children { id }
  typeId
  type { ...EventType }
  invitations { ...EventInvitation }
}
```

- **facilityById**: [FacilityGQLModel](#facilitygqlmodel) – Get a facility by id
  - **Arguments:**
    - **id**: [UUID](#uuid)!

Example usage:

```graphql
query Example($id: UUID!) {
  facilityById(id: $id) {
  ...Facility
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment FacilityType on FacilityTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    parent { id }
    parentId
    children { id }
  }

fragment Group on GroupGQLModel {
    __typename
    id
  }

fragment Facility on FacilityGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  label
  startdate
  enddate
  address
  valid
  capacity
  geometry
  geolocation
  groupId
  facilitytypeId
  masterFacilityId
  type { ...FacilityType }
  masterFacility { id }
  masterFacilities { id }
  subFacilities { id }
  group { ...Group }
}
```

- **facilityPage**: [[FacilityGQLModel](#facilitygqlmodel)!]! – Get a page of facilities
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [FacilityInputFilter](#facilityinputfilter)

Example usage:

```graphql
query Example($skip: Int, $limit: Int, $orderby: String, $where: FacilityInputFilter) {
  facilityPage(skip: $skip, limit: $limit, orderby: $orderby, where: $where) {
  ...Facility
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment FacilityType on FacilityTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    parent { id }
    parentId
    children { id }
  }

fragment Group on GroupGQLModel {
    __typename
    id
  }

fragment Facility on FacilityGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  label
  startdate
  enddate
  address
  valid
  capacity
  geometry
  geolocation
  groupId
  facilitytypeId
  masterFacilityId
  type { ...FacilityType }
  masterFacility { id }
  masterFacilities { id }
  subFacilities { id }
  group { ...Group }
}
```

- **documentById**: [ElectronicDocumentGQLModel](#electronicdocumentgqlmodel) – Get a Document by id
  - **Arguments:**
    - **id**: [UUID](#uuid)!

Example usage:

```graphql
query Example($id: UUID!) {
  documentById(id: $id) {
  ...ElectronicDocument
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment DocumentType on DocumentTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    parentId
    parent { id }
    children { id }
  }

fragment ElectronicDocument on ElectronicDocumentGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  description
  content
  mimetype
  parentId
  parent { id }
  children { id }
  typeId
  type { ...DocumentType }
}
```

- **documentPage**: [[ElectronicDocumentGQLModel](#electronicdocumentgqlmodel)!]! – Get a page of Documents
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [ElectronicDocumentInputFilter](#electronicdocumentinputfilter)

Example usage:

```graphql
query Example($skip: Int, $limit: Int, $orderby: String, $where: ElectronicDocumentInputFilter) {
  documentPage(skip: $skip, limit: $limit, orderby: $orderby, where: $where) {
  ...ElectronicDocument
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment DocumentType on DocumentTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    parentId
    parent { id }
    children { id }
  }

fragment ElectronicDocument on ElectronicDocumentGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  description
  content
  mimetype
  parentId
  parent { id }
  children { id }
  typeId
  type { ...DocumentType }
}
```

- **digitalDocumentById**: [DigitalFormGQLModel](#digitalformgqlmodel) – Get a DigitalForm by id
  - **Arguments:**
    - **id**: [UUID](#uuid)!

Example usage:

```graphql
query Example($id: UUID!) {
  digitalDocumentById(id: $id) {
  ...DigitalForm
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment State on StateGQLModel {
    __typename
    id
  }

fragment DocumentType on DocumentTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    parentId
    parent { id }
    children { id }
  }

fragment DigitalFormSection on DigitalFormSectionGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    label
    name
    labelEn
    description
    parentId
    sections { id }
    fields { id }
    order
    repatableMin
    repatableMax
    repeatable
    parent { id }
  }

fragment DigitalSubmission on DigitalSubmissionGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    stateId
    state { id }
    typeId
    type { id }
    submittedFields { id }
  }

fragment DigitalForm on DigitalFormGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  description
  stateId
  state { ...State }
  typeId
  type { ...DocumentType }
  sections { ...DigitalFormSection }
  submissions { ...DigitalSubmission }
}
```

- **digitalDocumentPage**: [[DigitalFormGQLModel](#digitalformgqlmodel)!]! – Get all DigitalForms with pagination
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DigitalFormInputFilter](#digitalforminputfilter)

Example usage:

```graphql
query Example($skip: Int, $limit: Int, $orderby: String, $where: DigitalFormInputFilter) {
  digitalDocumentPage(skip: $skip, limit: $limit, orderby: $orderby, where: $where) {
  ...DigitalForm
}
}

fragment User on UserGQLModel {
    __typename
    id
  }

fragment RBACObject on RBACObjectGQLModel {
    __typename
    id
  }

fragment State on StateGQLModel {
    __typename
    id
  }

fragment DocumentType on DocumentTypeGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    parentId
    parent { id }
    children { id }
  }

fragment DigitalFormSection on DigitalFormSectionGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    label
    name
    labelEn
    description
    parentId
    sections { id }
    fields { id }
    order
    repatableMin
    repatableMax
    repeatable
    parent { id }
  }

fragment DigitalSubmission on DigitalSubmissionGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { id }
    changedby { id }
    rbacobject { id }
    name
    nameEn
    description
    stateId
    state { id }
    typeId
    type { id }
    submittedFields { id }
  }

fragment DigitalForm on DigitalFormGQLModel {
  __typename
  id
  lastchange
  created
  createdbyId
  changedbyId
  rbacobjectId
  createdby { ...User }
  changedby { ...User }
  rbacobject { ...RBACObject }
  name
  nameEn
  description
  stateId
  state { ...State }
  typeId
  type { ...DocumentType }
  sections { ...DigitalFormSection }
  submissions { ...DigitalSubmission }
}
```


### Mutation: Mutation

#### Fields

- **eventInsert**: [EventGQLModelInsertError](#eventgqlmodelinserterror)! – Insert a Event
  - **Arguments:**
    - **event**: [EventInsertGQLModel](#eventinsertgqlmodel)!

Example usage:

```graphql
mutation Example($event_name: String, $event_nameEn: String, $event_description: String, $event_startDate: DateTime, $event_endDate: DateTime, $event_parentId: UUID, $event_id: UUID, $event_rbacobjectId: UUID) {
  eventInsert(event: {name: $event_name, nameEn: $event_nameEn, description: $event_description, startDate: $event_startDate, endDate: $event_endDate, parentId: $event_parentId, id: $event_id, rbacobjectId: $event_rbacobjectId}) {
  ... on EventGQLModel { ...Event }
  ... on InsertError { ...InsertError }
}
}

fragment User on UserGQLModel {
      __typename
      id
    }

fragment RBACObject on RBACObjectGQLModel {
      __typename
      id
    }

fragment EventType on EventTypeGQLModel {
      __typename
      id
      lastchange
      created
      createdbyId
      changedbyId
      rbacobjectId
      createdby { id }
      changedby { id }
      rbacobject { id }
      name
      nameEn
      description
      parentId
      parent { id }
      children { id }
      events { id }
    }

fragment EventInvitation on EventInvitationGQLModel {
      __typename
      id
      lastchange
      created
      createdbyId
      changedbyId
      rbacobjectId
      createdby { id }
      changedby { id }
      rbacobject { id }
      eventId
      userId
      stateId
      event { id }
      user { id }
      state { id }
    }

fragment Event on EventGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { ...User }
    changedby { ...User }
    rbacobject { ...RBACObject }
    name
    nameEn
    description
    startDate
    endDate
    parentId
    parent { id }
    children { id }
    typeId
    type { ...EventType }
    invitations { ...EventInvitation }
  }

fragment InsertError on InsertError {
    __typename
    msg
    failed
    input
  }
```

- **eventUpdate**: [EventGQLModelEventGQLModelUpdateError](#eventgqlmodeleventgqlmodelupdateerror)! – Update a Event
  - **Arguments:**
    - **event**: [EventUpdateGQLModel](#eventupdategqlmodel)!

Example usage:

```graphql
mutation Example($event_id: UUID!, $event_name: String, $event_nameEn: String, $event_description: String, $event_startDate: DateTime, $event_endDate: DateTime, $event_parentId: UUID) {
  eventUpdate(event: {id: $event_id, name: $event_name, nameEn: $event_nameEn, description: $event_description, startDate: $event_startDate, endDate: $event_endDate, parentId: $event_parentId}) {
  ... on EventGQLModel { ...Event }
  ... on EventGQLModelUpdateError { ...Error }
}
}

fragment User on UserGQLModel {
      __typename
      id
    }

fragment RBACObject on RBACObjectGQLModel {
      __typename
      id
    }

fragment EventType on EventTypeGQLModel {
      __typename
      id
      lastchange
      created
      createdbyId
      changedbyId
      rbacobjectId
      createdby { id }
      changedby { id }
      rbacobject { id }
      name
      nameEn
      description
      parentId
      parent { id }
      children { id }
      events { id }
    }

fragment EventInvitation on EventInvitationGQLModel {
      __typename
      id
      lastchange
      created
      createdbyId
      changedbyId
      rbacobjectId
      createdby { id }
      changedby { id }
      rbacobject { id }
      eventId
      userId
      stateId
      event { id }
      user { id }
      state { id }
    }

fragment Event on EventGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { ...User }
    changedby { ...User }
    rbacobject { ...RBACObject }
    name
    nameEn
    description
    startDate
    endDate
    parentId
    parent { id }
    children { id }
    typeId
    type { ...EventType }
    invitations { ...EventInvitation }
  }

fragment Error on EventGQLModelUpdateError {
    __typename
    Entity { ...Event }
    msg
    failed
    input
  }
```

- **eventDelete**: [EventGQLModelDeleteError](#eventgqlmodeldeleteerror) – Delete a Event
  - **Arguments:**
    - **event**: [EventDeleteGQLModel](#eventdeletegqlmodel)!

Example usage:

```graphql
mutation Example($event_id: UUID!, $event_lastchange: DateTime!) {
  eventDelete(event: {id: $event_id, lastchange: $event_lastchange}) {
  ...EventGQLModelDeleteError
}
}

fragment User on UserGQLModel {
      __typename
      id
    }

fragment RBACObject on RBACObjectGQLModel {
      __typename
      id
    }

fragment EventType on EventTypeGQLModel {
      __typename
      id
      lastchange
      created
      createdbyId
      changedbyId
      rbacobjectId
      createdby { id }
      changedby { id }
      rbacobject { id }
      name
      nameEn
      description
      parentId
      parent { id }
      children { id }
      events { id }
    }

fragment EventInvitation on EventInvitationGQLModel {
      __typename
      id
      lastchange
      created
      createdbyId
      changedbyId
      rbacobjectId
      createdby { id }
      changedby { id }
      rbacobject { id }
      eventId
      userId
      stateId
      event { id }
      user { id }
      state { id }
    }

fragment Event on EventGQLModel {
    __typename
    id
    lastchange
    created
    createdbyId
    changedbyId
    rbacobjectId
    createdby { ...User }
    changedby { ...User }
    rbacobject { ...RBACObject }
    name
    nameEn
    description
    startDate
    endDate
    parentId
    parent { id }
    children { id }
    typeId
    type { ...EventType }
    invitations { ...EventInvitation }
  }

fragment EventGQLModelDeleteError on EventGQLModelDeleteError {
  __typename
  Entity { ...Event }
  msg
  failed
  input
}
```


## Scalars

#### UUID

#### Date

Date (isoformat)

#### String

The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.

#### DateTime

Date with time (isoformat)

#### Int

The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

#### _Any

#### Boolean

The `Boolean` scalar type represents `true` or `false`.

#### Void

Represents NULL values

#### JSON

The `JSON` scalar type represents JSON values as specified by [ECMA-404](https://ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf).

## Input Types

#### EventInputFilter

Operators definition on EventInputFilter

Input Fields:
- **_or**: [[EventInputFilterOr](#eventinputfilteror)!] – Filter method
- **_and**: [[EventInputFilterAnd](#eventinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **start_date**: [DatetimeFilter](#datetimefilter) – Filter method
- **end_date**: [DatetimeFilter](#datetimefilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method

#### EventInputFilterOr

Or operator definition on EventInputFilter

Input Fields:
- **_and**: [[EventInputFilterAnd](#eventinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **start_date**: [DatetimeFilter](#datetimefilter) – Filter method
- **end_date**: [DatetimeFilter](#datetimefilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method

#### EventInputFilterAnd

And operator definition on EventInputFilter

Input Fields:
- **_or**: [[EventInputFilterOr](#eventinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **start_date**: [DatetimeFilter](#datetimefilter) – Filter method
- **end_date**: [DatetimeFilter](#datetimefilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method

#### StrFilter

Str filter methods, only one constrain allowed

Input Fields:
- **_eq**: String – operation for select.filter() method
- **_le**: String – operation for select.filter() method
- **_lt**: String – operation for select.filter() method
- **_ge**: String – operation for select.filter() method
- **_gt**: String – operation for select.filter() method
- **_like**: String – operation for select.filter() method
- **_ilike**: String – operation for select.filter() method
- **_startswith**: String – operation for select.filter() method
- **_endswith**: String – operation for select.filter() method

#### DatetimeFilter

Datetime filter methods, only one constrain allowed

Input Fields:
- **_eq**: [DateTime](#datetime) – operation for select.filter() method
- **_le**: [DateTime](#datetime) – operation for select.filter() method
- **_lt**: [DateTime](#datetime) – operation for select.filter() method
- **_ge**: [DateTime](#datetime) – operation for select.filter() method
- **_gt**: [DateTime](#datetime) – operation for select.filter() method

#### UuidFilter

Integer filter methods, only one constrain allowed

Input Fields:
- **_eq**: [UUID](#uuid) – operation for select.filter() method
- **_in**: [[UUID](#uuid)!] – operation for select.filter() method

#### EventTypeInputFilter

Operators definition on EventTypeInputFilter

Input Fields:
- **_or**: [[EventTypeInputFilterOr](#eventtypeinputfilteror)!] – Filter method
- **_and**: [[EventTypeInputFilterAnd](#eventtypeinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### EventTypeInputFilterOr

Or operator definition on EventTypeInputFilter

Input Fields:
- **_and**: [[EventTypeInputFilterAnd](#eventtypeinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### EventTypeInputFilterAnd

And operator definition on EventTypeInputFilter

Input Fields:
- **_or**: [[EventTypeInputFilterOr](#eventtypeinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### EventInvitationInputFilter

Operators definition on EventInvitationInputFilter

Input Fields:
- **_or**: [[EventInvitationInputFilterOr](#eventinvitationinputfilteror)!] – Filter method
- **_and**: [[EventInvitationInputFilterAnd](#eventinvitationinputfilterand)!] – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **event_id**: [UuidFilter](#uuidfilter) – Filter method
- **user_id**: [UuidFilter](#uuidfilter) – Filter method
- **state_id**: [UuidFilter](#uuidfilter) – Filter method

#### EventInvitationInputFilterOr

Or operator definition on EventInvitationInputFilter

Input Fields:
- **_and**: [[EventInvitationInputFilterAnd](#eventinvitationinputfilterand)!] – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **event_id**: [UuidFilter](#uuidfilter) – Filter method
- **user_id**: [UuidFilter](#uuidfilter) – Filter method
- **state_id**: [UuidFilter](#uuidfilter) – Filter method

#### EventInvitationInputFilterAnd

And operator definition on EventInvitationInputFilter

Input Fields:
- **_or**: [[EventInvitationInputFilterOr](#eventinvitationinputfilteror)!] – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **event_id**: [UuidFilter](#uuidfilter) – Filter method
- **user_id**: [UuidFilter](#uuidfilter) – Filter method
- **state_id**: [UuidFilter](#uuidfilter) – Filter method

#### DocumentTypeInputFilter

Input type for filtering DocumentTypeGQLModel

Input Fields:
- **name**: String!
- **nameEn**: String!
- **id**: [UUID](#uuid)!

#### FacilityTypeInputFilter

Operators definition on FacilityTypeInputFilter

Input Fields:
- **_or**: [[FacilityTypeInputFilterOr](#facilitytypeinputfilteror)!] – Filter method
- **_and**: [[FacilityTypeInputFilterAnd](#facilitytypeinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method

#### FacilityTypeInputFilterOr

Or operator definition on FacilityTypeInputFilter

Input Fields:
- **_and**: [[FacilityTypeInputFilterAnd](#facilitytypeinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method

#### FacilityTypeInputFilterAnd

And operator definition on FacilityTypeInputFilter

Input Fields:
- **_or**: [[FacilityTypeInputFilterOr](#facilitytypeinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method

#### FacilityInputFilter

Operators definition on FacilityInputFilter

Input Fields:
- **_or**: [[FacilityInputFilterOr](#facilityinputfilteror)!] – Filter method
- **_and**: [[FacilityInputFilterAnd](#facilityinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **valid**: [BoolFilter](#boolfilter) – Filter method
- **label**: [StrFilter](#strfilter) – Filter method
- **capacity**: [IntFilter](#intfilter) – Filter method
- **group_id**: [UuidFilter](#uuidfilter) – Filter method
- **master_facility_id**: [UuidFilter](#uuidfilter) – Filter method
- **facilitytype_id**: [UuidFilter](#uuidfilter) – Filter method
- **address**: [StrFilter](#strfilter) – Filter method

#### FacilityInputFilterOr

Or operator definition on FacilityInputFilter

Input Fields:
- **_and**: [[FacilityInputFilterAnd](#facilityinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **valid**: [BoolFilter](#boolfilter) – Filter method
- **label**: [StrFilter](#strfilter) – Filter method
- **capacity**: [IntFilter](#intfilter) – Filter method
- **group_id**: [UuidFilter](#uuidfilter) – Filter method
- **master_facility_id**: [UuidFilter](#uuidfilter) – Filter method
- **facilitytype_id**: [UuidFilter](#uuidfilter) – Filter method
- **address**: [StrFilter](#strfilter) – Filter method

#### FacilityInputFilterAnd

And operator definition on FacilityInputFilter

Input Fields:
- **_or**: [[FacilityInputFilterOr](#facilityinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **valid**: [BoolFilter](#boolfilter) – Filter method
- **label**: [StrFilter](#strfilter) – Filter method
- **capacity**: [IntFilter](#intfilter) – Filter method
- **group_id**: [UuidFilter](#uuidfilter) – Filter method
- **master_facility_id**: [UuidFilter](#uuidfilter) – Filter method
- **facilitytype_id**: [UuidFilter](#uuidfilter) – Filter method
- **address**: [StrFilter](#strfilter) – Filter method

#### BoolFilter

Integer filter methods, only one constrain allowed

Input Fields:
- **_eq**: Boolean – operation for select.filter() method

#### IntFilter

Integer filter methods, only one constrain allowed

Input Fields:
- **_eq**: Int – operation for select.filter() method
- **_le**: Int – operation for select.filter() method
- **_lt**: Int – operation for select.filter() method
- **_ge**: Int – operation for select.filter() method
- **_gt**: Int – operation for select.filter() method
- **_in**: [Int!] – operation for select.filter() method

#### ElectronicDocumentInputFilter

Operators definition on ElectronicDocumentInputFilter

Input Fields:
- **_or**: [[ElectronicDocumentInputFilterOr](#electronicdocumentinputfilteror)!] – Filter method
- **_and**: [[ElectronicDocumentInputFilterAnd](#electronicdocumentinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **mimetype**: [StrFilter](#strfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### ElectronicDocumentInputFilterOr

Or operator definition on ElectronicDocumentInputFilter

Input Fields:
- **_and**: [[ElectronicDocumentInputFilterAnd](#electronicdocumentinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **mimetype**: [StrFilter](#strfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### ElectronicDocumentInputFilterAnd

And operator definition on ElectronicDocumentInputFilter

Input Fields:
- **_or**: [[ElectronicDocumentInputFilterOr](#electronicdocumentinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **mimetype**: [StrFilter](#strfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormSectionInputFilter

Operators definition on DigitalFormSectionInputFilter

Input Fields:
- **_or**: [[DigitalFormSectionInputFilterOr](#digitalformsectioninputfilteror)!] – Filter method
- **_and**: [[DigitalFormSectionInputFilterAnd](#digitalformsectioninputfilterand)!] – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **label**: [StrFilter](#strfilter) – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **label_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormSectionInputFilterOr

Or operator definition on DigitalFormSectionInputFilter

Input Fields:
- **_and**: [[DigitalFormSectionInputFilterAnd](#digitalformsectioninputfilterand)!] – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **label**: [StrFilter](#strfilter) – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **label_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormSectionInputFilterAnd

And operator definition on DigitalFormSectionInputFilter

Input Fields:
- **_or**: [[DigitalFormSectionInputFilterOr](#digitalformsectioninputfilteror)!] – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **label**: [StrFilter](#strfilter) – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **label_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormFieldInputFilter

Operators definition on DigitalFormFieldInputFilter

Input Fields:
- **_or**: [[DigitalFormFieldInputFilterOr](#digitalformfieldinputfilteror)!] – Filter method
- **_and**: [[DigitalFormFieldInputFilterAnd](#digitalformfieldinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormFieldInputFilterOr

Or operator definition on DigitalFormFieldInputFilter

Input Fields:
- **_and**: [[DigitalFormFieldInputFilterAnd](#digitalformfieldinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormFieldInputFilterAnd

And operator definition on DigitalFormFieldInputFilter

Input Fields:
- **_or**: [[DigitalFormFieldInputFilterOr](#digitalformfieldinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalSubmissionFieldInputFilter

Operators definition on DigitalSubmissionFieldInputFilter

Input Fields:
- **_or**: [[DigitalSubmissionFieldInputFilterOr](#DigitalSubmissionFieldinputfilteror)!] – Filter method
- **_and**: [[DigitalSubmissionFieldInputFilterAnd](#DigitalSubmissionFieldinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **state_id**: [UuidFilter](#uuidfilter) – Filter method
- **field_id**: [UuidFilter](#uuidfilter) – Filter method
- **submission_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalSubmissionFieldInputFilterOr

Or operator definition on DigitalSubmissionFieldInputFilter

Input Fields:
- **_and**: [[DigitalSubmissionFieldInputFilterAnd](#DigitalSubmissionFieldinputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **state_id**: [UuidFilter](#uuidfilter) – Filter method
- **field_id**: [UuidFilter](#uuidfilter) – Filter method
- **submission_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalSubmissionFieldInputFilterAnd

And operator definition on DigitalSubmissionFieldInputFilter

Input Fields:
- **_or**: [[DigitalSubmissionFieldInputFilterOr](#DigitalSubmissionFieldinputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **state_id**: [UuidFilter](#uuidfilter) – Filter method
- **field_id**: [UuidFilter](#uuidfilter) – Filter method
- **submission_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalSubmissionInputFilter

Operators definition on DigitalSubmissionInputFilter

Input Fields:
- **_or**: [[DigitalSubmissionInputFilterOr](#DigitalSubmissioninputfilteror)!] – Filter method
- **_and**: [[DigitalSubmissionInputFilterAnd](#DigitalSubmissioninputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalSubmissionInputFilterOr

Or operator definition on DigitalSubmissionInputFilter

Input Fields:
- **_and**: [[DigitalSubmissionInputFilterAnd](#DigitalSubmissioninputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalSubmissionInputFilterAnd

And operator definition on DigitalSubmissionInputFilter

Input Fields:
- **_or**: [[DigitalSubmissionInputFilterOr](#DigitalSubmissioninputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormInputFilter

Operators definition on DigitalFormInputFilter

Input Fields:
- **_or**: [[DigitalFormInputFilterOr](#digitalforminputfilteror)!] – Filter method
- **_and**: [[DigitalFormInputFilterAnd](#digitalforminputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormInputFilterOr

Or operator definition on DigitalFormInputFilter

Input Fields:
- **_and**: [[DigitalFormInputFilterAnd](#digitalforminputfilterand)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### DigitalFormInputFilterAnd

And operator definition on DigitalFormInputFilter

Input Fields:
- **_or**: [[DigitalFormInputFilterOr](#digitalforminputfilteror)!] – Filter method
- **name**: [StrFilter](#strfilter) – Filter method
- **name_en**: [StrFilter](#strfilter) – Filter method
- **description**: [StrFilter](#strfilter) – Filter method
- **id**: [UuidFilter](#uuidfilter) – Filter method
- **parent_id**: [UuidFilter](#uuidfilter) – Filter method

#### EventInsertGQLModel

Input type for creating a Event

Input Fields:
- **name**: String – Event name assigned by an administrator
- **nameEn**: String – Event eng name assigned by an administrator
- **description**: String – Event description
- **startDate**: [DateTime](#datetime) – Event start date
- **endDate**: [DateTime](#datetime) – Event end date
- **parentId**: [UUID](#uuid) – Event parent id
- **id**: [UUID](#uuid) – Event id
- **rbacobjectId**: [UUID](#uuid) – Event rbacobject id

#### EventUpdateGQLModel

Input type for updating a Event

Input Fields:
- **id**: [UUID](#uuid)! – Event id
- **name**: String – Event name assigned by an administrator
- **nameEn**: String – Event eng name assigned by an administrator
- **description**: String – Event description
- **startDate**: [DateTime](#datetime) – Event start date
- **endDate**: [DateTime](#datetime) – Event end date
- **parentId**: [UUID](#uuid) – Event parent id

#### EventDeleteGQLModel

Input type for deleting a Event

Input Fields:
- **id**: [UUID](#uuid)! – Event id
- **lastchange**: [DateTime](#datetime)! – last change

## Regular Types

#### UserGQLModel

Fields:
- **id**: [UUID](#uuid)!

#### GroupGQLModel

Fields:
- **id**: [UUID](#uuid)!

#### EventGQLModel

Entity representing a Event

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Event name assigned by an administrator
- **nameEn**: String – Event eng name assigned by an administrator
- **description**: String – Event description
- **startDate**: [DateTime](#datetime) – Event start date
- **endDate**: [DateTime](#datetime) – Event end date
- **parentId**: [UUID](#uuid) – Event parent id
- **parent**: [EventGQLModel](#eventgqlmodel) – Event parent
- **children**: [[EventGQLModel](#eventgqlmodel)!]! – Event children
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [EventInputFilter](#eventinputfilter)
- **typeId**: [UUID](#uuid) – Event type id
- **type**: [EventTypeGQLModel](#eventtypegqlmodel) – Event type
- **invitations**: [[EventInvitationGQLModel](#eventinvitationgqlmodel)!]! – Event invitations
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [EventInvitationInputFilter](#eventinvitationinputfilter)

#### EventTypeGQLModel

Entity representing a Event Type

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Event Type name
- **nameEn**: String – Event Type eng name
- **description**: String – Event Type description
- **parentId**: [UUID](#uuid) – Event Type parent id
- **parent**: [EventTypeGQLModel](#eventtypegqlmodel) – Event Type parent
- **children**: [[EventTypeGQLModel](#eventtypegqlmodel)!]! – Event Type children
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [EventTypeInputFilter](#eventtypeinputfilter)
- **events**: [[EventGQLModel](#eventgqlmodel)!]! – Event Type events
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [EventInputFilter](#eventinputfilter)

#### EventInvitationGQLModel

Entity representing a Invitation to an Event and also presence of a user, invitation state and presence is managed by state

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **eventId**: [UUID](#uuid) – Event assigned to the invitation
- **userId**: [UUID](#uuid) – User assigned to the invitation
- **stateId**: [UUID](#uuid) – State assigned to the invitation
- **event**: [EventGQLModel](#eventgqlmodel) – Event assigned to the invitation
- **user**: [UserGQLModel](#usergqlmodel) – User assigned to the invitation
- **state**: [StateGQLModel](#stategqlmodel) – State assigned to the invitation

#### StateGQLModel

Fields:
- **id**: [UUID](#uuid)!

#### RBACObjectGQLModel

Fields:
- **id**: [UUID](#uuid)!

#### DocumentTypeGQLModel

Entity representing a Document

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Document name assigned by an administrator
- **nameEn**: String – Document eng name assigned by an administrator
- **description**: String – Document description
- **parentId**: [UUID](#uuid) – Parent document id
- **parent**: [DocumentTypeGQLModel](#documenttypegqlmodel) – Parent document
- **children**: [[DocumentTypeGQLModel](#documenttypegqlmodel)!]! – Children documents
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DocumentTypeInputFilter](#documenttypeinputfilter)

#### FacilityGQLModel

Entity representing a Facility

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Facility name assigned by an administrator
- **nameEn**: String – Facility eng name assigned by an administrator
- **label**: String – Facility full name assigned by an administrator
- **startdate**: [DateTime](#datetime) – Facility datetime 
- **enddate**: [DateTime](#datetime) – Facility datetime 
- **address**: String – Facility address
- **valid**: Boolean – is the facility still valid
- **capacity**: Int – Facility's capacity
- **geometry**: String – Facility geometry (SVG)
- **geolocation**: String – Facility geo address (WGS84+zoom)
- **groupId**: [UUID](#uuid) – Facility geo address (WGS84+zoom)
- **facilitytypeId**: [UUID](#uuid) – Facility geo address (WGS84+zoom)
- **masterFacilityId**: [UUID](#uuid) – Facility geo address (WGS84+zoom)
- **type**: [FacilityTypeGQLModel](#facilitytypegqlmodel) – Facility type
- **masterFacility**: [FacilityGQLModel](#facilitygqlmodel) – Facility above this
- **masterFacilities**: [[FacilityGQLModel](#facilitygqlmodel)!]! – Facilities above this
- **subFacilities**: [[FacilityGQLModel](#facilitygqlmodel)!]! – Facilities inside facility (like buildings in an areal)
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [Void](#void)
- **group**: [GroupGQLModel](#groupgqlmodel) – Group

#### FacilityTypeGQLModel

Entity representing a Facility type tree

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Facility type name assigned by an administrator
- **nameEn**: String – Facility type eng name assigned by an administrator
- **parent**: [FacilityTypeGQLModel](#facilitytypegqlmodel) – Facility type parent
- **parentId**: [UUID](#uuid) – Facility type parent id
- **children**: [[FacilityTypeGQLModel](#facilitytypegqlmodel)!]! – Facility type children
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [FacilityTypeInputFilter](#facilitytypeinputfilter)

#### ElectronicDocumentGQLModel

Represents a digital form used to capture user input.
Defines the overall structure of the form and stores its submissions.

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – The title of the digital form.
- **nameEn**: String – The eng title of the digital form.
- **description**: String – Document description
- **content**: String – Document content
- **mimetype**: String – Document mimetype
- **parentId**: [UUID](#uuid) – Document parent id
- **parent**: [ElectronicDocumentGQLModel](#electronicdocumentgqlmodel) – Document parent
- **children**: [[ElectronicDocumentGQLModel](#electronicdocumentgqlmodel)!]! – Document children
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [ElectronicDocumentInputFilter](#electronicdocumentinputfilter)
- **typeId**: [UUID](#uuid) – Document type id
- **type**: [DocumentTypeGQLModel](#documenttypegqlmodel) – Document type

#### DigitalFormGQLModel

Represents a digital form used to capture user input.
Defines the overall structure of the form and stores its submissions.

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Document name
- **nameEn**: String – Document eng name
- **description**: String – Document description
- **stateId**: [UUID](#uuid) – State id
- **state**: [StateGQLModel](#stategqlmodel) – State
- **typeId**: [UUID](#uuid) – Type id
- **type**: [DocumentTypeGQLModel](#documenttypegqlmodel) – Type
- **sections**: [[DigitalFormSectionGQLModel](#digitalformsectiongqlmodel)!]! – Digital Document sections
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DigitalFormSectionInputFilter](#digitalformsectioninputfilter)
- **submissions**: [[DigitalSubmissionGQLModel](#DigitalSubmissiongqlmodel)!]! – Digital Document submissions
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DigitalSubmissionInputFilter](#DigitalSubmissioninputfilter)

#### DigitalFormSectionGQLModel

Represents a section (group) of a digital form.
Supports nested sections and repetition.

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **label**: String – Label for display
- **name**: String – name for reference, must be unique and must start with a capitalized letter
- **labelEn**: String – Label for display in english
- **description**: String – Explanation of the form section
- **parentId**: [UUID](#uuid) – Digital document form section parent id which this section belongs to
- **sections**: [[DigitalFormSectionGQLModel](#digitalformsectiongqlmodel)!]! – Digital document form section children
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DigitalFormSectionInputFilter](#digitalformsectioninputfilter)
- **fields**: [[DigitalFormFieldGQLModel](#digitalformfieldgqlmodel)!]! – Digital document form section fields
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DigitalFormFieldInputFilter](#digitalformfieldinputfilter)
- **order**: Int! – Order of the section
- **repatableMin**: Int! – Minimum number of repetitions
- **repatableMax**: Int! – Maximum number of repetitions
- **repeatable**: Boolean! – Is section repeatable
- **parent**: [DigitalFormSectionGQLModelDigitalFormGQLModel](#digitalformsectiongqlmodeldigitalformgqlmodel)! – "form section or document 

#### DigitalFormFieldGQLModel

Represents a field in a digital form.
Defines properties of an individual input, including support for computed values.

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – name for reference, must be unique and must start with a lower letter
- **label**: String – Digital Form Field label for display
- **labelEn**: String – Digital Form Field label for display in english
- **description**: String – Digital Form Field placeholder
- **formSectionId**: [UUID](#uuid) – Digital form section where this field belongs
- **formSection**: [DigitalFormSectionGQLModel](#digitalformsectiongqlmodel) – Digital form section where this field belongs
- **formId**: [UUID](#uuid) – Digital form where this field belongs
- **form**: [DigitalFormGQLModel](#digitalformgqlmodel) – Digital form where this field belongs
- **required**: Boolean – Indicates whether this field is mandatory.
- **order**: Int – Order index to determine the field's position within its section.
- **computed**: Int – Indicates whether the field's value is computed automatically from other fields.
Probably alias for `formula is not None`
- **formula**: String – A mathematical formula (as a string) for computing the field's value.
Example: "price * quantity" where "price" and "quantity" reference other fields.
- **typeId**: [UUID](#uuid) – Specifies the type of input (e.g., "text", "number", "date", "boolean", "select").
- **backendFormula**: String – Specifies the backend payload constant(s).
- **flattenFormula**: String – Specifies the operation on incomming data.

#### DigitalSubmissionGQLModel

Represents a submission of a digital form filled out by a user.
Aggregates responses for all the fields defined in the form.

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **name**: String – Document name
- **nameEn**: String – Document eng name
- **description**: String – Document description
- **stateId**: [UUID](#uuid) – State id
- **state**: [StateGQLModel](#stategqlmodel) – State
- **typeId**: [UUID](#uuid) – Type id
- **type**: [DocumentTypeGQLModel](#documenttypegqlmodel) – Type
- **submittedFields**: [[DigitalSubmissionFieldGQLModel](#DigitalSubmissionFieldgqlmodel)!]! – Digital Form Submission fields assigned by an administrator
  - **Arguments:**
    - **skip**: Int
    - **limit**: Int
    - **orderby**: String
    - **where**: [DigitalSubmissionFieldInputFilter](#DigitalSubmissionFieldinputfilter)

#### DigitalSubmissionFieldGQLModel

Represents a response for a specific form field within a submission.
Links the user's provided value with the corresponding form field.

Fields:
- **id**: [UUID](#uuid) – primary key
- **lastchange**: [Date](#date) – timestamp
- **created**: [Date](#date) – date & time of unit born
- **createdbyId**: [UUID](#uuid) – who created this entity
- **changedbyId**: [UUID](#uuid) – who changed this entity
- **rbacobjectId**: [UUID](#uuid) – rbac ruling object
- **createdby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **changedby**: [UserGQLModel](#usergqlmodel) – who created this entity
- **rbacobject**: [RBACObjectGQLModel](#rbacobjectgqlmodel) – rbac holds relations of user
- **value**: String – Digital Field Response value typed by a user
- **fieldId**: [UUID](#uuid) – Digital Field id
- **submissionId**: [UUID](#uuid) – Digital Form Submission id
- **field**: [DigitalFormFieldGQLModel](#digitalformfieldgqlmodel) – Digital Field
- **submission**: [DigitalSubmissionGQLModel](#DigitalSubmissiongqlmodel) – Digital Form Submission
- **stateId**: [UUID](#uuid) – State id
- **state**: [StateGQLModel](#stategqlmodel) – State

#### _Service

Fields:
- **sdl**: String!

#### InsertError

Error object returned as an result of Insert operation

Fields:
- **msg**: String! – reason of fail
- **failed**: Boolean! – always True, available when error
- **input**: [JSON](#json) – original data

#### EventGQLModelUpdateError

Error object returned as an result of Update operation

Fields:
- **Entity**: [EventGQLModel](#eventgqlmodel) – Entity to be updated
- **msg**: String! – reason of fail
- **failed**: Boolean! – always True, available when error
- **input**: [JSON](#json) – original data

#### EventGQLModelDeleteError

Error object returned as an result of Delete operation

Fields:
- **Entity**: [EventGQLModel](#eventgqlmodel) – Entity to be updated
- **msg**: String! – reason of fail
- **failed**: Boolean! – always True, available when error
- **input**: [JSON](#json) – original data

