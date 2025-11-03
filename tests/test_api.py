"""
Tests for the FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from tests.samples import SAMPLE_BPMN_SIMPLE, SAMPLE_BPMN_COMPLEX


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        
    def test_analyse_endpoint_success(self, client):
        """Test successful BPMN analysis."""
        response = client.post(
            "/analyse",
            content=SAMPLE_BPMN_SIMPLE,
            headers={"Content-Type": "application/xml"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "suggestions" in data
        assert isinstance(data["stats"], dict)
        assert isinstance(data["suggestions"], list)
        assert "total_processes" in data["stats"]
        assert "total_tasks" in data["stats"]
    
    def test_analyse_endpoint_invalid_xml(self, client):
        """Test analysis with invalid XML."""
        response = client.post(
            "/analyse",
            content="<invalid>xml</invalid>",
            headers={"Content-Type": "application/xml"}
        )
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_analyse_endpoint_empty_xml(self, client):
        """Test analysis with empty XML."""
        response = client.post(
            "/analyse",
            content="",
            headers={"Content-Type": "application/xml"}
        )
        # Should fail validation or parsing
        assert response.status_code == 400
    
    def test_analyse_response_structure(self, client):
        """Test that the response has the correct structure."""
        response = client.post(
            "/analyse",
            content=SAMPLE_BPMN_SIMPLE,
            headers={"Content-Type": "application/xml"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check stats structure
        stats = data["stats"]
        required_stats_fields = [
            "total_processes", "total_lanes", "total_tasks", "task_types",
            "total_gateways", "gateway_types", "total_events",
            "event_types", "total_flows", "flow_types",
            "total_subprocesses", "total_data_objects",
            "total_data_stores", "has_error_handling", 
            "has_compensation", "complexity_score"
        ]
        
        for field in required_stats_fields:
            assert field in stats, f"Missing field in stats: {field}"
        
        # Check suggestions
        assert isinstance(data["suggestions"], list)
        assert len(data["suggestions"]) > 0
    
    def test_analyse_complex_bpmn(self, client):
        """Test analysis of a more complex BPMN."""
       
        response = client.post(
            "/analyse",
            content= SAMPLE_BPMN_COMPLEX,
            headers={"Content-Type": "application/xml"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stats"]["total_gateways"] == 2
        assert data["stats"]["total_tasks"] == 3

