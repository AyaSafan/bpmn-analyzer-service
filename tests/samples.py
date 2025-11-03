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