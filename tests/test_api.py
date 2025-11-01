"""
Tests for the FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


SAMPLE_BPMN = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1" name="Task 1"/>
    <bpmn2:endEvent id="EndEvent_1"/>
    <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="EndEvent_1"/>
  </bpmn2:process>
</bpmn2:definitions>
"""


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
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_analyse_endpoint_success(self, client):
        """Test successful BPMN analysis."""
        response = client.post(
            "/analyse",
            content=SAMPLE_BPMN,
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
            content=SAMPLE_BPMN,
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
        complex_bpmn = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1"/>
    <bpmn2:exclusiveGateway id="Gateway_1"/>
    <bpmn2:task id="Task_2"/>
    <bpmn2:task id="Task_3"/>
    <bpmn2:endEvent id="EndEvent_1"/>
    <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="Gateway_1"/>
    <bpmn2:sequenceFlow id="Flow_3" sourceRef="Gateway_1" targetRef="Task_2"/>
    <bpmn2:sequenceFlow id="Flow_4" sourceRef="Gateway_1" targetRef="Task_3"/>
    <bpmn2:sequenceFlow id="Flow_5" sourceRef="Task_2" targetRef="EndEvent_1"/>
    <bpmn2:sequenceFlow id="Flow_6" sourceRef="Task_3" targetRef="EndEvent_1"/>
  </bpmn2:process>
</bpmn2:definitions>
"""
        response = client.post(
            "/analyse",
            content=complex_bpmn,
            headers={"Content-Type": "application/xml"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stats"]["total_gateways"] == 1
        assert data["stats"]["total_tasks"] == 3

