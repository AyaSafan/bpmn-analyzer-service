"""
Example usage of the BPMN Analyzer Service.
This script demonstrates how to use the analyzer programmatically.
"""
from analyzer import BPMNAnalyzer


# Example BPMN 2.0 XML
SAMPLE_BPMN = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1" name="Review Request"/>
    <bpmn2:exclusiveGateway id="Gateway_1"/>
    <bpmn2:task id="Task_2" name="Approve Request"/>
    <bpmn2:task id="Task_3" name="Reject Request"/>
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


def main():
    """Example usage of the BPMN Analyzer."""
    print("BPMN Analyzer Example Usage\n" + "=" * 50)
    
    # Create analyzer instance
    analyzer = BPMNAnalyzer(SAMPLE_BPMN)
    
    # Analyze the BPMN
    result = analyzer.analyze()
    
    # Display statistics
    print("\nStatistics:")
    print(f"  Total Processes: {result['stats']['total_processes']}")
    print(f"  Total Tasks: {result['stats']['total_tasks']}")
    print(f"  Total Gateways: {result['stats']['total_gateways']}")
    print(f"  Total Events: {result['stats']['total_events']}")
    print(f"  Total Flows: {result['stats']['total_flows']}")
    print(f"  Complexity Score: {result['stats']['complexity_score']}")
    
    print("\nGateway Types:")
    for gateway_type, count in result['stats']['gateway_types'].items():
        if count > 0:
            print(f"  {gateway_type}: {count}")
    
    # Display suggestions
    print("\nSuggestions:")
    for i, suggestion in enumerate(result['suggestions'], 1):
        print(f"  {i}. {suggestion}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

