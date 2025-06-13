import responses
import pytest
from unifiedcatalogpy.client import UnifiedCatalogClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://example.purview.com/catalog/businessdomains"


@pytest.fixture
def client():
    # Initialize the DefaultAzureCredential
    credential = DefaultAzureCredential()

    """Fixture to initialize UnifiedCatalogClient with a credential."""
    return UnifiedCatalogClient(account_id="0234567890abcd", credential=credential)


@responses.activate
def test_get_governance_domains(client):
    """Test retrieving all governance domains."""
    responses.add(
        responses.GET,
        BASE_URL,
        json={"value": [{"id": "123", "name": "Finance"}]},
        status=200,
    )

    result = client.get_governance_domains()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "Finance"


@responses.activate
def test_get_governance_domain_by_id(client):
    """Test retrieving a governance domain by ID."""
    domain_id = "123"
    responses.add(
        responses.GET,
        f"{BASE_URL}/{domain_id}",
        json={"id": "123", "name": "Finance"},
        status=200,
    )

    result = client.get_governance_domain_by_id(domain_id)

    assert result["id"] == "123"
    assert result["name"] == "Finance"


@responses.activate
def test_create_governance_domain(client):
    """Test creating a new governance domain."""
    responses.add(
        responses.POST, BASE_URL, json={"id": "456", "name": "HR"}, status=201
    )

    result = client.create_governance_domain(
        name="HR", description="HR Domain", type="DataDomain"
    )

    assert result["id"] == "456"
    assert result["name"] == "HR"


@responses.activate
def test_update_governance_domain(client):
    """Test updating an existing governance domain."""
    domain_id = "123"
    responses.add(
        responses.PUT,
        f"{BASE_URL}/{domain_id}",
        json={"id": "123", "name": "Updated Finance"},
        status=200,
    )

    result = client.update_governance_domain(
        governance_domain_id="123", name="Updated Finance"
    )

    assert result["id"] == "123"
    assert result["name"] == "Updated Finance"


@responses.activate
def test_delete_governance_domain(client):
    """Test deleting a governance domain."""
    domain_id = "123"
    responses.add(responses.DELETE, f"{BASE_URL}/{domain_id}", status=204)

    result = client.delete_governance_domain(domain_id)

    assert result is True
