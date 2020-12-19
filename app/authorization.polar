# oso policy

# ROLE-PERMISSION RELATIONSHIPS

## Organization Permissions

### All organization roles let users read the organization
role_allow(role: OrganizationRole, "READ", org: Organization);

### Org members can list repos in the org
role_allow(role: OrganizationRole{name: "MEMBER"}, "LIST_REPOS", organization: Organization);

### The billing role can view billing info
role_allow(role: OrganizationRole{name: "BILLING"}, "READ_BILLING", organization: Organization);

### Org owners can assign roles within the org
role_allow(role: OrganizationRole{name: "OWNER"}, "CREATE_ROLE", organization: Organization);


# ROLE-ROLE RELATIONSHIPS

## Role Hierarchies

### Specify organization role order (most senior on left)
organization_role_order(["OWNER", "MEMBER"]);
organization_role_order(["OWNER", "BILLING"]);
