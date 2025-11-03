"""
Tests for the BPMN Analyzer module.
"""
import pytest
from lxml import etree
from analyzer import BPMNAnalyzer
from samples import SAMPLE_BPMN_SIMPLE, SAMPLE_BPMN_COMPLEX, SAMPLE_BPMN_WITH_LANES, INVALID_XML




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

