## ADDED Requirements
### Requirement: Role Management API
The system SHALL provide REST API endpoints for managing roles. The endpoints SHALL allow superusers to list, create, retrieve, update, and delete roles. Non-superusers SHALL NOT have access to these endpoints.

#### Scenario: List all roles
- **WHEN** a GET request is made to the roles endpoint by an authenticated superuser
- **THEN** all roles are returned
- **AND** a 200 OK status is returned

#### Scenario: Create a new role
- **WHEN** a POST request is made to the roles endpoint by an authenticated superuser with valid role data
- **THEN** a new role is created
- **AND** the created role data is returned
- **AND** a 201 Created status is returned

#### Scenario: Retrieve a specific role
- **WHEN** a GET request is made to a specific role endpoint by an authenticated superuser
- **THEN** the role details are returned
- **AND** a 200 OK status is returned

#### Scenario: Update a role
- **WHEN** a PUT or PATCH request is made to a specific role endpoint by an authenticated superuser with valid role data
- **THEN** the role is updated
- **AND** the updated role data is returned
- **AND** a 200 OK status is returned

#### Scenario: Delete a role
- **WHEN** a DELETE request is made to a specific role endpoint by an authenticated superuser
- **THEN** the role is deleted
- **AND** a 204 No Content status is returned

#### Scenario: Non-superuser access denied
- **WHEN** any request is made to the roles endpoints by a non-superuser
- **THEN** the request is denied
- **AND** a 403 Forbidden status is returned

#### Scenario: Unauthenticated access denied
- **WHEN** any request is made to the roles endpoints without authentication
- **THEN** the request is denied
- **AND** a 401 Unauthorized status is returned

### Requirement: Business Element Management API
The system SHALL provide REST API endpoints for managing business elements. The endpoints SHALL allow superusers to list, create, retrieve, update, and delete business elements. Non-superusers SHALL NOT have access to these endpoints.

#### Scenario: List all business elements
- **WHEN** a GET request is made to the business elements endpoint by an authenticated superuser
- **THEN** all business elements are returned
- **AND** a 200 OK status is returned

#### Scenario: Create a new business element
- **WHEN** a POST request is made to the business elements endpoint by an authenticated superuser with valid business element data
- **THEN** a new business element is created
- **AND** the created business element data is returned
- **AND** a 201 Created status is returned

#### Scenario: Retrieve a specific business element
- **WHEN** a GET request is made to a specific business element endpoint by an authenticated superuser
- **THEN** the business element details are returned
- **AND** a 200 OK status is returned

#### Scenario: Update a business element
- **WHEN** a PUT or PATCH request is made to a specific business element endpoint by an authenticated superuser with valid business element data
- **THEN** the business element is updated
- **AND** the updated business element data is returned
- **AND** a 200 OK status is returned

#### Scenario: Delete a business element
- **WHEN** a DELETE request is made to a specific business element endpoint by an authenticated superuser
- **THEN** the business element is deleted
- **AND** a 204 No Content status is returned

#### Scenario: Non-superuser access denied
- **WHEN** any request is made to the business elements endpoints by a non-superuser
- **THEN** the request is denied
- **AND** a 403 Forbidden status is returned

#### Scenario: Unauthenticated access denied
- **WHEN** any request is made to the business elements endpoints without authentication
- **THEN** the request is denied
- **AND** a 401 Unauthorized status is returned

### Requirement: Access Rule Management API
The system SHALL provide REST API endpoints for managing access role rules. The endpoints SHALL allow superusers to list, create, retrieve, update, and delete access rules. Non-superusers SHALL NOT have access to these endpoints.

#### Scenario: List all access rules
- **WHEN** a GET request is made to the access rules endpoint by an authenticated superuser
- **THEN** all access rules are returned
- **AND** a 200 OK status is returned

#### Scenario: Create a new access rule
- **WHEN** a POST request is made to the access rules endpoint by an authenticated superuser with valid access rule data
- **THEN** a new access rule is created
- **AND** the created access rule data is returned
- **AND** a 201 Created status is returned

#### Scenario: Retrieve a specific access rule
- **WHEN** a GET request is made to a specific access rule endpoint by an authenticated superuser
- **THEN** the access rule details are returned
- **AND** a 200 OK status is returned

#### Scenario: Update an access rule
- **WHEN** a PUT or PATCH request is made to a specific access rule endpoint by an authenticated superuser with valid access rule data
- **THEN** the access rule is updated
- **AND** the updated access rule data is returned
- **AND** a 200 OK status is returned

#### Scenario: Delete an access rule
- **WHEN** a DELETE request is made to a specific access rule endpoint by an authenticated superuser
- **THEN** the access rule is deleted
- **AND** a 204 No Content status is returned

#### Scenario: Non-superuser access denied
- **WHEN** any request is made to the access rules endpoints by a non-superuser
- **THEN** the request is denied
- **AND** a 403 Forbidden status is returned

#### Scenario: Unauthenticated access denied
- **WHEN** any request is made to the access rules endpoints without authentication
- **THEN** the request is denied
- **AND** a 401 Unauthorized status is returned

#### Scenario: Duplicate access rule creation fails
- **WHEN** a POST request is made to create an access rule with a role and element combination that already exists
- **THEN** the creation fails
- **AND** a 400 Bad Request status is returned
- **AND** an error message indicates the duplicate constraint violation
