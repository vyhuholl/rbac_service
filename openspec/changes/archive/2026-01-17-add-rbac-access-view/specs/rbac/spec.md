## ADDED Requirements
### Requirement: Access Check View
The system SHALL provide an API endpoint for checking user access to business resources. The endpoint SHALL accept a user ID, resource name, and required permissions. If the user exists and has the necessary permissions, the system SHALL return the business resource data. If the user does not exist, a 401 Unauthorized error SHALL be returned. If the user exists but lacks permissions, a 403 Forbidden error SHALL be returned.

#### Scenario: User has required permissions
- **WHEN** a GET request is made to the access endpoint with a valid user ID, resource name, and permissions that the user possesses
- **THEN** the system returns the business resource data
- **AND** a 200 OK status is returned

#### Scenario: User does not exist
- **WHEN** a GET request is made to the access endpoint with a non-existent user ID
- **THEN** a 401 Unauthorized status is returned
- **AND** no resource data is returned

#### Scenario: User lacks required permissions
- **WHEN** a GET request is made to the access endpoint with a valid user ID and resource name, but the user does not have the required permissions
- **THEN** a 403 Forbidden status is returned
- **AND** no resource data is returned

#### Scenario: Resource does not exist
- **WHEN** a GET request is made to the access endpoint with a valid user ID but non-existent resource name
- **THEN** a 403 Forbidden status is returned (since access to non-existent resource is denied)
- **AND** no resource data is returned