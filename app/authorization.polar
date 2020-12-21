# oso policy

# ROLE-PERMISSION RELATIONSHIPS

## Organization Permissions

### All organization roles let users read the organization
role_allow(_role: OrganizationRole, "READ", _org: Organization);

### Org members can list repos in the org
role_allow(_role: OrganizationRole{name: "MEMBER"}, "LIST_REPOS", _org: Organization);

### The billing role can view billing info
role_allow(_role: OrganizationRole{name: "BILLING"}, "READ_BILLING", _org: Organization);

### Org owners can assign roles within the org
role_allow(_role: OrganizationRole{name: "OWNER"}, "CREATE_ROLE", _org: Organization);


# ROLE-ROLE RELATIONSHIPS

## Role Hierarchies

### Specify organization role order (most senior on left)
organization_role_order(["OWNER", "MEMBER"]);
organization_role_order(["OWNER", "BILLING"]);
