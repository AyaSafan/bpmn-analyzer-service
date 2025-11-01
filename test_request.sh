#!/bin/bash
# Example curl commands to test the /analyse endpoint

# Option 1: Single-line JSON with escaped newlines (works best on Linux/Mac)
curl -X 'POST' \
  'http://localhost:8000/analyse' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"bpmn_xml": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><bpmn2:definitions xmlns:bpmn2=\"http://www.omg.org/spec/BPMN/20100524/MODEL\" xmlns:bpmndi=\"http://www.omg.org/spec/BPMN/20100524/DI\" xmlns:dc=\"http://www.omg.org/spec/DD/20100524/DC\" targetNamespace=\"http://bpmn.io/schema/bpmn\"><bpmn2:process id=\"Process_1\" isExecutable=\"true\"><bpmn2:startEvent id=\"StartEvent_1\"/><bpmn2:task id=\"Task_1\" name=\"Task 1\"/><bpmn2:endEvent id=\"EndEvent_1\"/><bpmn2:sequenceFlow id=\"Flow_1\" sourceRef=\"StartEvent_1\" targetRef=\"Task_1\"/><bpmn2:sequenceFlow id=\"Flow_2\" sourceRef=\"Task_1\" targetRef=\"EndEvent_1\"/></bpmn2:process></bpmn2:definitions>"}'

# Option 2: Using a JSON file (recommended for Windows PowerShell)
# First, create a file request.json with the content, then:
# curl -X POST http://localhost:8000/analyse -H "Content-Type: application/json" -d @request.json

