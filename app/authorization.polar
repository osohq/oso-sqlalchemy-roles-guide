# # RBAC RULES

# # RESOURCE-ROLE RELATIONSHIPS

# ## These rules allow roles to apply to resources other than those that they are scoped to.
# ## The most common example of this is nested resources, e.g. Repository roles should apply to the Issues
# ## nested in that repository.


### An organization's roles apply to its child roles
resource_role_applies_to(role: OrganizationRole, parent_org) if
    parent_org := role.organization and
    parent_org matches Organization;

# # ROLE-PERMISSION RELATIONSHIPS

# ## Record-level Organization Permissions

### All organization roles let users read the organization
role_allow(role: OrganizationRole, "READ", org: Organization) if
    role.organization = org;

role_allow(role: OrganizationRole{name: "OWNER"}, "LIST_ROLES", organization: Organization);
role_allow(role: OrganizationRole{name: "MEMBER"}, "LIST_REPOS", organization: Organization);

## OrganizationRole Permissions

### Organization owners can access the Organization's roles
role_allow(role: OrganizationRole{name: "OWNER"}, "READ", role_resource: OrganizationRole) if
    role.organization.id = role_resource.organization.id;

# ROLE-ROLE RELATIONSHIPS

## Role Hierarchies

### Specify organization role order (most senior on left)
organization_role_order(["OWNER", "MEMBER"]);
organization_role_order(["OWNER", "BILLING"]);
