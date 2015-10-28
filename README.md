The schema defines the following properties:

# `publisher` (object)

This element contains the name of the entity, typically a 'publisher', responsible for making the version of record of the resource available. This could be a person, organisation or service

Properties of the `publisher` object:

# `description` (string)

A textual description of the resource.

# `contributors` (array, required)

The people or organizations responsible for making contributions to an object.

The object is an array with all elements of the type `undefined`.

# `title` (string, required)

The title and any sub-titles of the resource.

# `shareProperties` (object)

Properties that are generated and/or organized by the SHARE system (e.g., timestamps of when SHARE processes data). These properities are used internally and are not guaranteed to remain consistent.

Properties of the `shareProperties` object:

## `source` (string, required)

The source of the data in the document

## `docID` (string,, required)

A service-unique identifier for the document

# `otherProperties` (array)

Any structured or unstructured properties (properties that do or do not include URIs to definitions) that do not fall into the schema provided.

The object is an array with all elements of the type `otherProperties`.

# `tags` (array)

Non-hierarchical terms or keywords assigned to an object to aid browsing or searching.

The object is an array with all elements of the type `string`.

# `uris` (object, required)

Properties of the `uris` object:

## `canonicalUri` (string, required)

The preferred persistent HTTP URI that represents the research object. This should be repeated in exactly one other field in the uris object.

## `anyOf`

# `languages` (array)

The primary languages in which the content of the resource is presented. Values used for this element MUST conform to ISO 639–3. This offers three letter tags e.g. "eng" for English.

The object is an array with all elements of the type `string`.

# `providerUpdatedDateTime` (string, required)

The date and time the provider describing the object has been updated about either the creation or update of an object by its contributors. E.g., this may be the date a manuscript is published, but not necessarily the date the manuscript was written.

# `sponsorships` (array)

Sponsorships associated with the object

The object is an array with all elements of the type `sponsorship`.

# `version` (object)

Infomation about this version of the object.

Properties of the `version` object:

## `versionId`

The name or number representing this version of the object.

## `versionDateTime` (string)

The date and time the object was created or updated by its contributors. If the data for the object describes the first version of that object, it will be the date and time of object creation, otherwise it will be considered the date and time the object was updated.

## `versionOf` (string)

If the object is an update, the HTTP URI of the object the content is updating. Depending upon what the upate is relative to, that could be the object at creation or a previous version.

# `freeToRead` (object)

A date range specifying when this research object will be accessible, without restrictsions such as fee or registration). If the object is free to read, then only the startDate is required.

Properties of the `freeToRead` object:

## `startDate` (string, required)

The date and time at which the object will be accessible. If the resource was always free to read, then the date the object was created should be used.

## `endDate` (string)

The date and time at which restrictions such as fees or registrations will be in place limiting accessibility.

# `licenses` (array)

The licenses under which the object has been released.

The object is an array with all elements of the type `license`.

# `subjects` (array)

The topic or domain of the object. Follows recommendations of http://dublincore.org/documents/2012/06/14/dcmi-terms/?v=elements#terms-subject

The object is an array with all elements of the type `string`.

---

# Sub Schemas

The schema defines the following additional types:

## `person` (object)

A person that is a contributor to the research object.

Properties of the `person` object:

### `affiliation` (array)

The organization(s) that this person is affiliated with. For example, a school/university.

The object is an array with all elements of the type `organization`.

### `givenName` (string)

Also called the "first name", this element is preferred over using the combined "name" field.

### `additionalName` (string)

Also called the "middle name", this element will be derived from the creator.name by SHARE if not supplied by the source.

### `name` (string, required)

The name of the person if familyName, givenName, and/or additionalName.

### `sameAs` (array)

An array of identifiers expressed as HTTP URIs that describe the person. For example, an ORCID, ResearcherID, arXiv author ID, ScopusID,  ISNI, or other unique identifier expressed as an HTTP URI.

The object is an array with all elements of the type `string`.

### `familyName` (string)

Also called the "last name", this element is preferred over using the combined "name" field.

### `email` (string)

The email address for this person.

## `sponsor` (object)

This describes the sponsor of the resource.

Properties of the `sponsor` object:

### `sponsorName` (string, required)

The name of the entity responsible for sponsoring the resource, recorded here as text.

### `sponsorIdentifier` (string)

A globally unique identifier for the sponsor of the resource should be recorded here.

## `license` (object)

Properties of the `license` object:

### `startDate` (string)

The date and time at which the license will apply to this object. If the resource was always licensed this way, then this date can be omitted.

### `endDate` (string)

The date and time at which this resource will no longer be licensed in this way.

### `uri` (string, required)

The HTTP URI of the license of the object or--if startDate and endDate are included--in effect during the period listed.

### `description` (string)

Text describing to what aspect of the object the license is applied.

## `organization` (object)

An organization or institution.

Properties of the `organization` object:

### `sameAs` (array)

Identifiers that describe this organization

The object is an array with all elements of the type `string`.

### `name` (string, required)

The name of the organization.

### `email` (string)

An email address for this organization

## `otherProperties` (object)

Properties of the `otherProperties` object:

### `description` (string)

A description of this collection of properties.

### `properties` (object, required)

The collection of key/value pair properties.

Properties of the `properties` object:

### `name` (string, required)

A name that describes this collection of properties.

### `uri` (string)

A URI that points to the definition, schema, and/or vocabulary of this entry.

## `award` (object)

The award made in support of the object.

Properties of the `award` object:

### `awardIdentifier` (string)

An HTTP URI for the award.

### `awardName` (string, required)

The textual representation of the award identifier as issued by the sponsor.

## `sponsorship` (object)

A sponsorship associated with the resource.

Properties of the `sponsorship` object:

### `sponsor` (sponsor, required)

### `award` (award)