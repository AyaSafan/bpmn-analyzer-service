"""
BPMN 2.0 XML Analyzer Module
Analyzes BPMN XML files and extracts statistics and suggestions.
"""
from typing import Dict, List, Any
from lxml import etree
from collections import defaultdict
from collections import Counter

class BPMNAnalyzer:
    """Analyzes BPMN 2.0 XML files."""
    
    # BPMN 2.0 namespaces
    BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
    BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
    
    def __init__(self, bpmn_xml: str):
        """Initialize analyzer with BPMN XML string."""
        self.bpmn_xml = bpmn_xml
        self.root = None
        self.nsmap = {
            'bpmn': self.BPMN_NS,
            'bpmndi': self.BPMNDI_NS
        }
        
    def parse(self) -> None:
        """Parse the BPMN XML."""
        try:
            self.root = etree.fromstring(self.bpmn_xml.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Invalid XML: {e}")
        # Basic validation: ensure this looks like a BPMN 2.0 document
        is_bpmn = bool(self.root.xpath('//bpmn:definitions | //bpmn:process', namespaces=self.nsmap))
        if not is_bpmn:
            raise ValueError("Not a valid BPMN 2.0 XML document: missing <definitions> or <process> in BPMN namespace")
    
    def analyze(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of the BPMN file."""
        if self.root is None:
            self.parse()
        
        stats = self._extract_stats()
        suggestions = self._generate_suggestions(stats)
        
        return {
            "stats": stats,
            "suggestions": suggestions
        }
    
    def _extract_stats(self) -> Dict[str, Any]:
        """Extract statistics from the BPMN XML."""
        stats = {
            "total_processes": 0,
            "total_tasks": 0,
            "task_types": defaultdict(int),
            "total_gateways": 0,
            "gateway_types": defaultdict(int),
            "total_events": 0,
            "event_types": defaultdict(int),
            "total_flows": 0,
            "flow_types": defaultdict(int),
            "total_lanes": 0,
            "total_subprocesses": 0,
            "total_data_objects": 0,
            "total_data_stores": 0,
            "has_error_handling": False,
            "has_compensation": False,
            "complexity_score": 0
        }
        
        # Count processes
        processes = self.root.xpath('//bpmn:process', namespaces=self.nsmap)
        stats["total_processes"] = len(processes)

        # Count lanes
        lanes = self.root.xpath('//bpmn:laneSet/bpmn:lane', namespaces=self.nsmap)
        stats["total_lanes"] = len(lanes)

        # Count tasks
        stats["task_types"].clear()
        stats["total_tasks"] = 0  
        tag_task_map = {
            "userTask": "//bpmn:userTask",
            "serviceTask": "//bpmn:serviceTask",
            "scriptTask": "//bpmn:scriptTask",
            "manualTask": "//bpmn:manualTask",
            "businessRuleTask": "//bpmn:businessRuleTask",
            "sendTask": "//bpmn:sendTask",
            "receiveTask": "//bpmn:receiveTask",
            "callActivity": "//bpmn:callActivity",
            "task": "//bpmn:task",  # generic
        }
        # Count all the above tasks
        for task_type, xpath in tag_task_map.items():
            matches = self.root.xpath(xpath, namespaces=self.nsmap)
            count = len(matches)
            if count > 0:
                stats["task_types"][task_type] += count
                stats["total_tasks"] += count
        
        # Count gateways
        exclusive_gateways = self.root.xpath('//bpmn:exclusiveGateway', namespaces=self.nsmap)
        inclusive_gateways = self.root.xpath('//bpmn:inclusiveGateway', namespaces=self.nsmap)
        parallel_gateways = self.root.xpath('//bpmn:parallelGateway', namespaces=self.nsmap)
        event_gateways = self.root.xpath('//bpmn:eventBasedGateway', namespaces=self.nsmap)
        complex_gateways = self.root.xpath('//bpmn:complexGateway', namespaces=self.nsmap)
        
        stats["total_gateways"] = (
            len(exclusive_gateways) + len(inclusive_gateways) + 
            len(parallel_gateways) + len(event_gateways) + len(complex_gateways)
        )
        stats["gateway_types"]["exclusive"] = len(exclusive_gateways)
        stats["gateway_types"]["inclusive"] = len(inclusive_gateways)
        stats["gateway_types"]["parallel"] = len(parallel_gateways)
        stats["gateway_types"]["eventBased"] = len(event_gateways)
        stats["gateway_types"]["complex"] = len(complex_gateways)
        
        # Count events
        start_events = self.root.xpath('//bpmn:startEvent', namespaces=self.nsmap)
        intermediate_events = self.root.xpath('//bpmn:intermediateCatchEvent | //bpmn:intermediateThrowEvent', namespaces=self.nsmap)
        end_events = self.root.xpath('//bpmn:endEvent', namespaces=self.nsmap)
        boundary_events = self.root.xpath('//bpmn:boundaryEvent', namespaces=self.nsmap)
        
        stats["total_events"] = len(start_events) + len(intermediate_events) + len(end_events) + len(boundary_events)
        stats["event_types"]["start"] = len(start_events)
        stats["event_types"]["intermediate"] = len(intermediate_events)
        stats["event_types"]["end"] = len(end_events)
        stats["event_types"]["boundary"] = len(boundary_events)
        
        # Count flows
        sequence_flows = self.root.xpath('//bpmn:sequenceFlow', namespaces=self.nsmap)
        message_flows = self.root.xpath('//bpmn:messageFlow', namespaces=self.nsmap)
        
        stats["total_flows"] = len(sequence_flows) + len(message_flows)
        stats["flow_types"]["sequence"] = len(sequence_flows)
        stats["flow_types"]["message"] = len(message_flows)
        
              
        # Count subprocesses
        subprocesses = self.root.xpath('//bpmn:subProcess', namespaces=self.nsmap)
        stats["total_subprocesses"] = len(subprocesses)
        
        # Count data objects and stores
        data_objects = self.root.xpath('//bpmn:dataObject', namespaces=self.nsmap)
        data_stores = self.root.xpath('//bpmn:dataStoreReference', namespaces=self.nsmap)
        stats["total_data_objects"] = len(data_objects)
        stats["total_data_stores"] = len(data_stores)
        
        # Check for specific features
        error_events = self.root.xpath('//bpmn:errorEventDefinition', namespaces=self.nsmap)
        stats["has_error_handling"] = len(error_events) > 0
        
        
        compensation_events = self.root.xpath('//bpmn:compensateEventDefinition', namespaces=self.nsmap)
        stats["has_compensation"] = len(compensation_events) > 0
        
        # Calculate complexity score
        stats["complexity_score"] = self._calculate_complexity_score(stats)
        
        # Convert defaultdicts to regular dicts for JSON serialization
        stats["task_types"] = dict(stats["task_types"])
        stats["gateway_types"] = dict(stats["gateway_types"])
        stats["event_types"] = dict(stats["event_types"])
        stats["flow_types"] = dict(stats["flow_types"])
        
        return stats
    
    def _calculate_complexity_score(self, stats: Dict[str, Any]) -> int:
        """Calculate a complexity score based on various factors."""
        score = 0
        score += stats["total_tasks"] * 1
        score += stats["total_gateways"] * 2
        score += stats["total_events"] * 1
        score += stats["total_subprocesses"] * 5
        score += stats["total_flows"] * 0.5
        score += stats["total_lanes"] * 2
        return int(score)
    
    def _generate_suggestions(self, stats: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on the analysis."""
        suggestions = []
        
        # Process count suggestions
        if stats["total_processes"] == 0:
            suggestions.append("No processes found in the BPMN file. Ensure the file contains valid BPMN process definitions.")
        
        # Gateway balance suggestions
        if stats["total_gateways"] == 0 and stats["total_tasks"] > 3:
            suggestions.append("Consider using gateways to model decision points and parallel execution for better process clarity.")
        
        elif stats["gateway_types"].get("complex", 0) > 0:
            suggestions.append("Complex gateways detected. Consider simplifying by using exclusive or inclusive gateways where possible.")
        
        # Flow suggestions
        if stats["flow_types"].get("sequence", 0) == 0 and stats["total_tasks"] > 0:
            suggestions.append("No sequence flows found. Ensure tasks are properly connected with sequence flows.")
        
        # Lanes suggestions
        if stats["total_lanes"] == 0 and stats["total_tasks"] > 5:
            suggestions.append("Consider adding lanes to organize activities by roles or organizational units for better clarity.")
        
        # Complexity suggestions
        if stats["complexity_score"] > 100:
            suggestions.append(f"High complexity score ({stats['complexity_score']}). Consider breaking down the process into smaller subprocesses.")
        elif stats["complexity_score"] < 10:
            suggestions.append("Very simple process. Ensure all necessary business logic is captured.")
        
              
        if not stats["flow_types"]["message"] == 0 and stats["total_processes"] > 1:
            suggestions.append("For multi-process scenarios, consider using message flows for inter-process communication.")
        
        # Data handling
        if stats["total_data_objects"] == 0 and stats["total_data_stores"] == 0 and stats["total_tasks"] > 0:
            suggestions.append("No data objects or data stores found. Consider modeling data flow for better process documentation.")
        
        # Subprocess suggestions
        if stats["total_subprocesses"] == 0 and stats["complexity_score"] > 50:
            suggestions.append("Consider extracting complex sections into subprocesses to improve readability and reusability.")
        
        if not suggestions:
            suggestions.append("No specific suggestions. The BPMN file appears well-structured.")
        
        return suggestions

