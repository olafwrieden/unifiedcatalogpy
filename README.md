![Banner](https://raw.githubusercontent.com/olafwrieden/unifiedcatalogpy/main/assets/media/banner.png)

# Introducing: UnifiedCatalogPy

A Python wrapper for Microsoft Purview Data Governance's Unified Catalog API. Not affiliated or officially supported by Microsoft. Built as a personal project by tediously observing the internet browser's XHR network traffic and reverse engineering the API - ☕️ [buy me a coffee](https://buymeacoffee.com/olafwrieden).

## Overview 🔥

UnifiedCatalogPy simplifies the interaction with Microsoft Purview's Unified Catalog API. It provides a set of features that allow you to manage and interact with various data governance elements, including operations for creating, retrieving, updating, and deleting business concepts.

**Interact with:**

- Governance Domains
- Glossary Terms
- Data Products
- Objectives and Key Results (OKRs)
- Critical Data Elements (CDEs)
- Custom Attributes (🚧 coming soon)
- Requests (🚧 coming soon)
- Health Management (🚧 coming soon)
  - Health Controls
  - Health Actions
  - ~~Data Quality~~ (no API support yet!)

> [!WARNING]
> This library is not locked to a specific stable version of the Microsoft Purview API as an official API for the Unified Catalog is not yet available. This means functionality may change unexpectedly. [See limitations](#limitations-)

## Quick Start 🚀

### 1. Installation

Start by installing the library. You will also need to install the `azure-identity` library to authenticate with Microsoft Purview.

```bash
# Install the libraries
pip install unifiedcatalogpy azure-identity
```

### 2. Authentication

Microsoft Purview requires an authorized identity to perform tasks. You can choose between authenticating as a user (via [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)) or using a Service Principal.

> [!NOTE]
> In most cases you should be using a Service Principal to query Microsoft Purview (RBAC permissions can be scoped independently of a user). Remember that ownership of an artifact defaults to its creator unless you specify a user/group at creation.

#### Using Azure CLI

If you are using the Azure CLI, be sure to log in using `az login` before running your Python notebook. Your credentials will be automatically picked up by the `DefaultAzureCredential` class. Your user must have the **Data Governance Administrator** role in Microsoft Purview to perform operations.

#### Using a Service Principal

1. ️Navigate to the Azure portal to [create a new Service Principal](https://learn.microsoft.com/en-us/purview/tutorial-using-rest-apis) for your application and generate a client secret.
2. Copy the Application (client) ID, Directory (tenant) ID, and Client Secret (value) into your Python environment variables.

   ```
   AZURE_CLIENT_ID=
   AZURE_TENANT_ID=
   AZURE_CLIENT_SECRET=
   ```

3. Navigate to the _Properties_ tab of your Microsoft Purview Azure resource to locate your Purview account ID. It can be found in the _Atlas endpoint URL_.

   **Example:** `https://<your-purview-account-id>-api.purview-service.microsoft.com/catalog`

   Copy the `<your-purview-account-id>` - you will need it in a moment to create the client.

4. Navigate to the Microsoft Purview portal _> Settings > Solution Settings > Unified Catalog > Roles and Permissions > Data Governance Administrators_ and add the Service Principal as a **Data Governance Administrator**.

5. Your Service Principal is now authorized to interact with Microsoft Purview Data Governance Unified Catalog API. Let's test it out! 🚀

### 3. Using the Client

In your Python notebook, you can use the library as follows:

```python
# Import the library
from unfiedcatalogpy.client import UnifiedCatalogClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Create the Unified Catalog Client
client = UnifiedCatalogClient(
 account_id="<your-purview-account-id>",
 credential=credential
)

# Interact with the client
domains = client.get_governance_domains()
```

**💡 Good to know:** You can import types from the `unifiedcatalogpy.types` module to help with type hinting and IDE autocompletion. Detailed usage examples for supported functionality is provided in the documentation section below. _Let's automate!_

## Documentation 📖

Here is what's possible with the `UnifiedCatalogPy` client.

### Governance Domain

An organizational object that provides context for your data assets and make it easier scale data governance practices. [Learn more](https://learn.microsoft.com/en-us/purview/concept-governance-domain)

#### Create a Governance Domain

```python
from unifiedcatalogpy.types import GovernanceDomainType, GovernanceDomainStatus

# Create a new governance domain
new_domain = client.create_governance_domain(
    name="My First Domain",
    description="<div>This is an example of a <b>rich text</b> description.</div>",
    type=GovernanceDomainType.FunctionalUnit,
    status=GovernanceDomainStatus.Draft,
)

# Show the new governance domain
print(new_domain)
```

#### Retrieve all Governance Domains

```python
# Get all governance domains
domains = client.get_governance_domains()
```

_Note: Pagination over governance domains is not yet supported._

#### Retrieve a Governance Domain by ID

```python
# Get a governance domain by ID
domain = client.get_governance_domain_by_id("<your-governance-domain-id>")

# Show the governance domain
print(domain)
```

#### Update a Governance Domain

```python
from unifiedcatalogpy.types import GovernanceDomainType, GovernanceDomainStatus

# Update a governance domain by ID
updated_domain = client.update_governance_domain(
    governance_domain_id="<your-governance-domain-id>",
    name="Updated Domain Name",
    description="<div>This is an <b>updated</b> domain description.</div>",
    owners=[{ "id": "<entra-object-id>" }],
    type=GovernanceDomainType.FunctionalUnit,
    status=GovernanceDomainStatus.Draft,
)

# Show the updated governance domain
print(updated_domain)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Delete a Governance Domain

```python
# Delete a governance domain by ID
deleted = client.delete_governance_domain("<your-governance-domain-id>")

if deleted:
    print("Governance domain deleted successfully.")
else:
    print("Failed to delete governance domain.")
```

---

### Glossary Terms

Active values that provide context but also apply policies that determine how your data should be managed, governed, and made discoverable for use. [Learn more](https://learn.microsoft.com/en-us/purview/concept-glossary-terms)

#### Create a Glossary Term

```python
from unifiedcatalogpy.types import TermStatus

# Create new glossary term
term = client.create_term(
    name="My First Term",
    description="<div>This is a <b>rich description</b> of my first term.</div>",
    status=TermStatus.Draft,
    governance_domain_id="<your-governance-domain-id>",
    acronyms=["ACRONYM_1", "ACRONYM_2"],
    resources=[
        {
            "name": "Read more details",
            "url": "https://example.com",
        }
    ],
    owners=[{"id": "<entra-object-id>"}],
)

# Show the new glossary term
print(term)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Retrieve all Glossary Terms in a Governance Domain

```python
# Get all terms in the governance domain
terms = client.get_terms("<your-governance-domain-id>")

# Enumerate the terms
for term in terms:
    print(term)
```

_Note: Pagination over glossary terms is not yet supported._

#### Retrieve a Glossary Term by ID

```python
# Get a specific term by ID
term = client.get_term_by_id("<your-term-id>")

# Show the term
print(term)
```

#### Update a Glossary Term

```python
from unifiedcatalogpy.types import TermStatus

# Update a term
updated_term = client.update_term(
    term_id="<your-term-id>",
    name="Updated Term Name",
    description="<div>This is an updated term description.</div>",
    governance_domain_id="<your-governance-domain-id>",
    owners=[{"id": "<entra-object-id>"}],
    acronyms=["ACRONYM_1_UPDATED", "ACRONYM_2_UPDATED"],
    resources=[
        {
            "name": "Read more about this term",
            "url": "https://example.com/more",
        }
    ],
    status=TermStatus.Draft,
)

# Show the updated term
print(updated_term)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Delete a Glossary Term

```python
# Delete a term
deleted = client.delete_term("<your-term-id>")

if deleted:
    print("Governance domain deleted successfully.")
else:
    print("Failed to delete governance domain.")
```

#### Create a Term Relationship (Synonyms / Related Terms)

##### Link Term to a Synonym

```python
# Link a synonym to a term
relationship = client.create_term_relationship(
    term_id="<your-term-id>",
    relationship_type="Synonym",
    entity_id="<your-target-term-id>",
    description="This is a synonym relationship.",
)

# Show the relationship
print(relationship)
```

##### Link Term to a Related Term

```python
# Link a related term to a term
relationship = client.create_term_relationship(
    term_id="<your-term-id>",
    relationship_type="Related",
    entity_id="<your-related-term-id>",
    description="This is a related term relationship.",
)

# Show the relationship
print(relationship)
```

#### Delete a Term Relationship (Synonyms / Related Terms)

##### Delete a Synonym relationship

```python
# Delete a term relationship
deleted = client.delete_term_relationship(
    term_id="<your-term-id>",
    entity_id="<your-target-term-id>",
    relationship_type="Synonym",
    entity_type="Term",
)

if deleted:
    print("Synonym relationship deleted successfully.")
else:
    print("Failed to delete the synonym relationship.")
```

##### Delete a Related Term relationship

```python
# Delete a term relationship
deleted = client.delete_term_relationship(
    term_id="<your-term-id>",
    entity_id="<your-target-term-id>",
    relationship_type="Related",
    entity_type="Term",
)

if deleted:
    print("Related relationship deleted successfully.")
else:
    print("Failed to delete the related relationship.")
```

---

### Data Products

A kit of data assets (tables, files, Power BI reports, etc.) that provides assets with a use case for ease of discovery and understanding. [Learn more](https://learn.microsoft.com/en-us/purview/concept-data-products)

#### Create a Data Product

```python
from unifiedcatalogpy.types import DataProductStatus, DataProductType, DataProductUpdateFrequency

# Create a new Data Product
data_product = client.create_data_product(
    governance_domain_id="<your-governance-domain-id>",
    name="My First Data Product",
    description="<div>This is a <b>new</b> data product created for demonstration purposes.</div>",
    type=DataProductType.Operational,
    owners=[{"id": "<entra-object-id>"}],
    status=DataProductStatus.Draft,
    audience=[],
    business_use="<div>Use Case 1, 2, 3</div>",
    documentation=[],
    updateFrequency=DataProductUpdateFrequency.Weekly,
    endorsed=False,
    terms_of_use=[],
)

# Show Data Product
print(data_product)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Retrieve all Data Products in a Governance Domain

```python
# Get all data products in the governance domain
data_products = client.get_data_products("<your-governance-domain-id>")

# Enumerate the data products
for data_product in data_products:
    print(data_product)
```

_Note: Pagination over data products is not yet supported._

#### Retrieve a Data Product by ID

```python
# Get data product by ID
data_product = client.get_data_product_by_id("<your-data-product-id>")

# Show data product
print(data_product)
```

#### Update a Data Product

```python
from unifiedcatalogpy.types import DataProductStatus, DataProductType, DataProductUpdateFrequency

# Update a data product
updated_data_product = client.update_data_product(
    data_product_id="<your-data-product-id>",
    governance_domain_id="<your-governance-domain-id>",
    name="My Updated Data Product",
    description="<div>This is an <b>updated</b> data product description.</div>",
    owners=[
        {
            "id": "<entra-object-id>",
            "description": "Data Product Owner",
        }
    ],
    status=DataProductStatus.Draft,
    audience=[],
    business_use="<div>Use Case 1, 2, 3</div>",
    documentation=[],
    endorsed=False,
    terms_of_use=[],
    type=DataProductType.Operational,
    updateFrequency=DataProductUpdateFrequency.Weekly,
)

# Show the updated data product
print(updated_data_product)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Delete a Data Product

```python
# Delete data product
deleted = client.delete_data_product("<your-data-product-id>")

if deleted:
    print("Data Product deleted successfully.")
else:
    print("Failed to delete Data Product.")
```

#### Link a Glossary Term to a Data Product

#### Unlink a Glossary Term from a Data Product

#### Link an Asset to a Data Product

#### Unlink an Asset from a Data Product

#### Link an Objective to a Data Product

#### Unlink an Objective from a Data Product

#### Link a Critical Data Element to a Data Product

#### Unlink a Critical Data Element from a Data Product

---

### Objectives and Key Results (OKRs)

Objectives and key results link data products directly to your objectives to bridge the gap between your business and Unified Catalog. You use data to discover and track objectives in your business, and Unified Catalog should make it easy to see those connections and track your goals. [Learn more](https://learn.microsoft.com/en-us/purview/concept-okr)

#### Create an Objective

```python
# Create an objective
objective = client.create_objective(
    definition="Revamp customer service to improve satisfaction and retention rates.",
    governance_domain_id="<your-governance-domain-id>",
    status="Draft",
    owners=[
        {
            "id": "<entra-object-id>",
            "description": "Objective Owner",
        }
    ],
    target_date="2025-12-30T14:00:00.000Z",
)

# Show the objective
print(objective)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Retrieve all Objectives in a Governance Domain

```python
# Get all objectives in the governance domain
objectives = client.get_objectives("<your-governance-domain-id>")

# Show objectives
print(objectives)
```

_Note: Pagination over objectives is not yet supported._

#### Retrieve an Objective by ID

```python
# Get objective by its ID
objective = client.get_objective_by_id("<your-objective-id>")

# Show the objective
print(objective)
```

#### Update an Objective

```python
# Update an objective
updated_objective = client.update_objective(
    objective_id="<your-objective-id>",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    owners=[
        {
            "id": "<entra-object-id>",
            "description": "Objective Owner",
        }
    ],
    definition="Improve customer service to improve satisfaction and retention rates.",
    target_date="2025-06-15T14:00:00.000Z",
)

# Show updated objective
print(updated_objective)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Delete an Objective

```python
# Delete an objective
deleted = client.delete_objective("<your-objective-id>")

if deleted:
    print("Objective deleted successfully.")
else:
    print("Failed to delete Objective.")
```

#### Create a Key Result for an Objective

```python
# Create a key result
key_result = client.create_key_result(
    progress=60,
    goal=80,
    max=100,
    status="AtRisk",
    definition="Increase customer satisfaction score by 20%.",
    objective_id="<your-objective-id>",
    governance_domain_id="<your-governance-domain-id>",
)

# Show the key result
print(key_result)
```

#### Retrieve all Key Results of an Objective

```python
# Get all key results of an objective
key_results = client.get_key_results("<your-objective-id>")

# Show the key results
print(key_results)
```

#### Retrieve a Key Result by ID

```python
# Get a key result by ID
key_result = client.get_key_result_by_id(
    key_result_id="<your-key-result-id>",
    objective_id="<your-objective-id>",
)

# Show key result
print(key_result)
```

#### Update a Key Result of an Objective

```python
# Update a key result
updated_key_result = client.update_key_result(
    key_result_id="<your-key-result-id>",
    progress=70,
    goal=80,
    max=100,
    status="OnTrack",
    definition="Increase customer satisfaction score by 20%.",
    objective_id="<your-objective-id>",
    governance_domain_id="<your-governance-domain-id>",
)

# Show the updated key result
print(updated_key_result)
```

#### Delete a Key Result of an Objective

```python
# Delete a key result
deleted = client.delete_key_result(
    key_result_id="<your-key-result-id>",
    objective_id="<your-objective-id>",
)

if deleted:
    print("Key Result deleted successfully.")
else:
    print("Failed to delete Key Result.")
```

#### Link a Data Product to an Objective

#### Unlink a Data Product from an Objective

---

### Critical Data Elements (preview)

Critical data elements are a logical grouping of important pieces of information across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-create-manage-critical-data)

#### Create a Critical Data Element

```python
# Create a critical data element
cde = client.create_critical_data_element(
    name="Customer Identifier (CID)",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    description="<div>Describes a numeric <b>customer identifier</b> throughout the data estate.</div>",
    data_type="Number",
    owners=[{ "id": "<entra-object-id>" }],
)

# Show critical data element
print(cde)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Retrieve all Critical Data Elements in a Governance Domain

```python
# Get all critical data elements in the governance domain
cdes = client.get_critical_data_elements("<your-governance-domain-id>")

# Enumerate the critical data elements
for cde in cdes:
    print(cde)
```

_Note: Pagination over critical data elements is not yet supported._

#### Retrieve a Critical Data Element by ID

```python
# Get critical data element by its ID
cde = client.get_critical_data_element_by_id("<your-critical-data-element-id>")

# Show critical data element
print(cde)
```

#### Update a Critical Data Element

```python
# Update a critical data element
updated_cde = client.update_critical_data_element(
    cde_id="<your-critical-data-element-id>",
    name="Customer Identifier (CID)",
    description="<div>An <b>updated description</b> of a customer identifier.</div>",
    status="Draft",
    governance_domain_id="<your-governance-domain-id>",
    data_type="String",
    owners=[{ "id": "<entra-object-id>" }],
)

# Show updated critical data element
print(updated_cde)
```

**💡 Good to know:** See [Converting Between User/Group Names and Object IDs](#converting-between-usergroup-names-and-object-ids-) if you you need a human-readable name instead of an ID.

#### Delete a Critical Data Element

```python
# Delete a critical data element
deleted = client.delete_critical_data_element("<your-critical-data-element-id>")

if deleted:
    print("Critical Data Element deleted successfully.")
else:
    print("Failed to delete Critical Data Element.")
```

#### Add a Column to a Critical Data Element

#### Remove a Column from a Critical Data Element

#### Link a Glossary Term to a Critical Data Element

#### Unlink a Glossary Term from a Critical Data Element

---

### Custom Attributes (preview)

Custom attributes are admin-defined, attributes that can be applied to add additional metadata to business concepts in the Unified Catalog.

> [!WARNING]
> You cannot interact with Custom Attributes through this library yet.

---

### Requests

If you discover a data product in the catalog that you would like to access, you can request access directly through Microsoft Purview. The request triggers a workflow requesting that the owners of the data resource grant you access to the data product. [Learn more](https://learn.microsoft.com/en-us/purview/unified-catalog-access-policies)

> [!WARNING]
> You cannot interact with Requests through this library yet. This is work in progress. A pull request to add this functionality is welcome.

#### Create a Request

#### Retrieve all Requests in a Governance Domain

#### Retrieve a Request by ID

#### Update a Request

#### Delete a Request

---

### Health Management

Health management refers to the ongoing processes and practices involved in ensuring that an organization's data remains accurate, complete, consistent, secure, and accessible throughout its lifecycle.

#### Health Controls (preview)

Track your journey to complete data governance by monitoring health controls to track your progress. Health controls measure your current governance practices against standards that give your data estate a score. [Learn more](https://learn.microsoft.com/en-us/purview/how-to-health-controls)

> [!WARNING]
> Not all Health Control functions can be interacted with through this library yet. This is work in progress.

##### Create a Health Control

##### Retrieve a Health Control

##### Update a Health Control

##### Update Health Controls Refresh Schedule

```python
# Update the health control refresh schedule
schedule = client.update_health_control_refresh_schedule(
    frequency="Week",
    interval=1,
    status="Enabled",
    start_time="2025-01-01T00:00:00Z",
    time_zone="E. Australia Standard Time",
    end_time=None,
)

# Show the updated schedule
print(schedule)
```

Note: Health Controls cannot be deleted, you should instead update their status to "Disabled".

#### Health Actions (preview)

Health actions are concrete steps you can take to improve data governance across your data estate. The actions are provided in a single list that can focus your data governance journey, and democratize ownership. Completing these actions will improve data quality and discoverability across your data estate. [Learn more](https://learn.microsoft.com/en-us/purview/data-estate-health-actions)

**💡 Good to know:** To continually export Health Actions from Purview for condition-based alerting or reporting, you may like to consider using the [Self-serve analytics and insights (preview)](https://learn.microsoft.com/en-us/purview/purview-dg-self-service-analytics-and-insight) integration to natively export the entire Purview domain model to Microsoft Fabric OneLake or to an Azure Data Lake Storage Gen2 account.

> [!WARNING]
> Not all Health Action functions can be interacted with through this library. This is work in progress.

##### Retrieve all Health Actions in a Governance Domain

##### Retrieve a Health Action by ID

```python
# Get a health action by ID
action = client.get_health_action_by_id("<your-health-action-id>")

# Show the health action
print(action)
```

##### Update a Health Action

```python

```

Note: Health Actions cannot be deleted, you should instead update their status to "Resolved".

#### Data Quality

Data quality is the measurement of the quality of data in an organization, based on data quality rules that are configured and defined in Unified Catalog. [Learn more](https://learn.microsoft.com/en-us/purview/data-quality-overview)

> [!WARNING]
> You cannot interact with Data Quality through this library yet. There is a lot of complexity in the API, data quality sub-features, and interpretation of the results. A pull request to add this functionality is welcome.

## Converting between User/Group Names and Object IDs 📃

As shown in many of the code examples above, Microsoft Purview item ownership is specified using the user's or group's Object ID as shown in your Microsoft Entra tenant.

You may like to install the [Microsoft Graph Python SDK](https://pypi.org/project/msgraph-sdk/) using `pip install msgraph-sdk` to convert between user/group names or email addresses and their respective Object IDs.

**Example Scenario:** Utilising the Graph SDK would allow you to specify a spreadsheet of governance domains and their owners (by name or email address), read it using Python, and then convert the names to Object IDs before passing them to the Unified Catalog API.

Either way, Microsoft Purview will automatically convert the ID into the user/group name when showing ownership information in the Unified Catalog.

## Limitations 🚧

- This library is not affiliated with Microsoft.
- The library is not locked to a specific version of the Microsoft Purview API as an official Microsoft Purview Data Governance API for the Unified Catalog is not yet available. This means functionality may change unexpectedly. Do not rely on this library in production for this reason.
- The library is maintained on a best-effort basis. It is not a full-time project and PRs are welcome.
- Managing business concept policies and data quality is not yet supported.
- No automated tests are included, functionality has been manually tested on a best-effort basis. PRs are welcome to add tests.
- No typed return schema is provided as the API is not yet stable.
