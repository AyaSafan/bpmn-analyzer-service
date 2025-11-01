"""
Tests for the BPMN Analyzer module.
"""
import pytest
from lxml import etree
from analyzer import BPMNAnalyzer


SAMPLE_BPMN_SIMPLE = """<?xml version="1.0" encoding="UTF-8"?>
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

SAMPLE_BPMN_COMPLEX = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1" name="Task 1"/>
    <bpmn2:exclusiveGateway id="Gateway_1"/>
    <bpmn2:task id="Task_2" name="Task 2"/>
    <bpmn2:task id="Task_3" name="Task 3"/>
    <bpmn2:parallelGateway id="Gateway_2"/>
    <bpmn2:subProcess id="SubProcess_1"/>
    <bpmn2:endEvent id="EndEvent_1">
      <bpmn2:errorEventDefinition id="ErrorEvent_1"/>
    </bpmn2:endEvent>
    <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="Gateway_1"/>
    <bpmn2:sequenceFlow id="Flow_3" sourceRef="Gateway_1" targetRef="Task_2"/>
    <bpmn2:sequenceFlow id="Flow_4" sourceRef="Gateway_1" targetRef="Task_3"/>
    <bpmn2:sequenceFlow id="Flow_5" sourceRef="Task_2" targetRef="Gateway_2"/>
    <bpmn2:sequenceFlow id="Flow_6" sourceRef="Task_3" targetRef="Gateway_2"/>
    <bpmn2:sequenceFlow id="Flow_7" sourceRef="Gateway_2" targetRef="SubProcess_1"/>
    <bpmn2:sequenceFlow id="Flow_8" sourceRef="SubProcess_1" targetRef="EndEvent_1"/>
  </bpmn2:process>
</bpmn2:definitions>
"""

SAMPLE_BPMN_WITH_LANES = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:laneSet id="LaneSet_1">
      <bpmn2:lane id="Lane_1" name="Role A"/>
      <bpmn2:lane id="Lane_2" name="Role B"/>
    </bpmn2:laneSet>
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1" name="Task 1"/>
    <bpmn2:task id="Task_2" name="Task 2"/>
    <bpmn2:endEvent id="EndEvent_1"/>
    <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="Task_2"/>
    <bpmn2:sequenceFlow id="Flow_3" sourceRef="Task_2" targetRef="EndEvent_1"/>
  </bpmn2:process>
</bpmn2:definitions>
"""

INVALID_XML = "<invalid>xml content</invalid>"


class TestBPMNAnalyzer:
    """Test cases for BPMNAnalyzer."""
    
    def test_simple_bpmn_analysis(self):
        """Test analysis of a simple BPMN file."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_SIMPLE)
        result = analyzer.analyze()
        
        assert "stats" in result
        assert "suggestions" in result
        assert result["stats"]["total_processes"] == 1
        assert result["stats"]["total_tasks"] == 1
        assert result["stats"]["total_gateways"] == 0
        assert result["stats"]["total_events"] == 2  # start + end
        assert result["stats"]["total_flows"] >= 2
        assert len(result["suggestions"]) > 0
    
    def test_complex_bpmn_analysis(self):
        """Test analysis of a complex BPMN file."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_COMPLEX)
        result = analyzer.analyze()
        
        assert result["stats"]["total_processes"] == 1
        assert result["stats"]["total_tasks"] == 3
        assert result["stats"]["total_gateways"] == 2
        assert result["stats"]["total_subprocesses"] == 1
        assert result["stats"]["has_error_handling"] is True
        assert "exclusive" in result["stats"]["gateway_types"]
        assert "parallel" in result["stats"]["gateway_types"]
    
    def test_bpmn_with_lanes(self):
        """Test analysis of BPMN file with lanes."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_WITH_LANES)
        result = analyzer.analyze()
        
        assert result["stats"]["total_lanes"] == 2
    
    def test_invalid_xml(self):
        """Test that invalid XML raises an error."""
        analyzer = BPMNAnalyzer(INVALID_XML)
        with pytest.raises(ValueError):
            analyzer.analyze()
    
    def test_empty_xml(self):
        """Test that empty XML raises an error."""
        analyzer = BPMNAnalyzer("")
        with pytest.raises((ValueError, etree.XMLSyntaxError)):
            analyzer.analyze()
    
    def test_stats_structure(self):
        """Test that stats have the expected structure."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_SIMPLE)
        result = analyzer.analyze()
        stats = result["stats"]
        
        required_keys = [
            "total_processes", "total_lanes", "total_tasks", "task_types",
            "total_gateways", "gateway_types", "total_events",
            "event_types", "total_flows", "flow_types",
            "total_subprocesses", "total_data_objects",
            "total_data_stores", "has_error_handling", 
            "has_compensation", "complexity_score"
        ]
        
        for key in required_keys:
            assert key in stats, f"Missing key: {key}"
    
    def test_suggestions_generated(self):
        """Test that suggestions are generated."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_SIMPLE)
        result = analyzer.analyze()
        
        assert isinstance(result["suggestions"], list)
        assert len(result["suggestions"]) > 0
        assert all(isinstance(s, str) for s in result["suggestions"])
    
    def test_complexity_score_calculation(self):
        """Test complexity score calculation."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_SIMPLE)
        result = analyzer.analyze()
        
        assert "complexity_score" in result["stats"]
        assert isinstance(result["stats"]["complexity_score"], int)
        assert result["stats"]["complexity_score"] >= 0
    
    def test_multiple_calls_same_analyzer(self):
        """Test that analyzer can be called multiple times."""
        analyzer = BPMNAnalyzer(SAMPLE_BPMN_SIMPLE)
        result1 = analyzer.analyze()
        result2 = analyzer.analyze()
        
        assert result1["stats"] == result2["stats"]

