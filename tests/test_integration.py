import pytest
from unifiedcatalogpy.client import UnifiedCatalogClient


@pytest.fixture(scope="module")
def client():
    # Provide valid credentials for integration testing
    account_id = "YOUR_ACCOUNT_GUID"
    credential = None  # Replace with your actual azure.identity credential
    return UnifiedCatalogClient(account_id, credential)


def test_governance_domain_integration(client):
    # Create
    domain = client.create_governance_domain(
        name="IntegrationTestDomain",
        description="Testing domain creation",
        type="FunctionalUnit",
    )
    assert domain.get("id")

    # Read
    fetched_domain = client.get_governance_domain_by_id(domain["id"])
    assert fetched_domain["name"] == "IntegrationTestDomain"

    # Update
    updated_domain = client.update_governance_domain(
        governance_domain_id=domain["id"], name="UpdatedIntegrationTestDomain"
    )
    assert updated_domain["name"] == "UpdatedIntegrationTestDomain"

    # Delete
    result = client.delete_governance_domain(domain["id"])
    assert result


def test_term_integration(client):
    # Create
    term = client.create_term(
        name="IntegrationTestTerm",
        description="Testing term creation",
        governance_domain_id="some-domain-id",
    )
    assert term.get("id")

    # Read
    fetched_term = client.get_term_by_id(term["id"])
    assert fetched_term["name"] == "IntegrationTestTerm"

    # Update
    updated_term = client.update_term(
        term_id=term["id"], name="UpdatedIntegrationTestTerm"
    )
    assert updated_term["name"] == "UpdatedIntegrationTestTerm"

    # Delete
    delete_result = client.delete_term(term["id"])
    assert delete_result


def test_data_product_integration(client):
    # Create
    data_product = client.create_data_product(
        name="IntegrationTestDataProduct",
        description="Testing data product creation",
        governance_domain_id="some-domain-id",
        type="Dataset",
        business_use="Test business use",
    )
    assert data_product.get("id")

    # Read
    fetched_dp = client.get_data_product_by_id(data_product["id"])
    assert fetched_dp["name"] == "IntegrationTestDataProduct"

    # Update
    updated_dp = client.update_data_product(
        data_product_id=data_product["id"], name="UpdatedIntegrationTestDataProduct"
    )
    assert updated_dp["name"] == "UpdatedIntegrationTestDataProduct"

    # Delete
    delete_result = client.delete_data_product(data_product["id"])
    assert delete_result


def test_objective_integration(client):
    # Create
    objective = client.create_objective(
        definition="Testing objective creation", governance_domain_id="some-domain-id"
    )
    assert objective.get("id")

    # Read
    fetched_obj = client.get_objective_by_id(objective["id"])
    assert fetched_obj["definition"] == "Testing objective creation"

    # Update
    updated_obj = client.update_objective(
        objective_id=objective["id"], definition="Updated test objective"
    )
    assert updated_obj["definition"] == "Updated test objective"

    # Delete
    delete_result = client.delete_objective(objective["id"])
    assert delete_result


def test_key_result_integration(client):
    # Create
    # You likely need an existing objective ID for this to work.
    # This example assumes we have an objective already created.
    key_result = client.create_key_result(
        progress=10,
        goal=100,
        max=100,
        status="OnTrack",
        definition="Test KR creation",
        objective_id="some-objective-id",
        governance_domain_id="some-domain-id",
    )
    assert key_result.get("id")

    # Read
    fetched_kr = client.get_key_result_by_id(key_result["id"], "some-objective-id")
    assert fetched_kr["definition"] == "Test KR creation"

    # Update
    updated_kr = client.update_key_result(
        key_result_id=key_result["id"],
        objective_id="some-objective-id",
        governance_domain_id="some-domain-id",
        definition="Updated test KR",
    )
    assert updated_kr["definition"] == "Updated test KR"

    # Delete
    delete_result = client.delete_key_result(key_result["id"], "some-objective-id")
    assert delete_result
