# Testing the API

## API Now Accepts Raw XML

The `/analyse` endpoint now accepts BPMN 2.0 XML directly as `application/xml` content type. No need to wrap it in JSON!

## Usage Examples

### Option 1: Using curl with a file (Easiest!)

```bash
curl -X POST http://localhost:8000/analyse \
  -H "Content-Type: application/xml" \
  -d @sample.bpmn
```

**Windows PowerShell:**
```powershell
$xml = Get-Content sample.bpmn -Raw
Invoke-RestMethod -Uri http://localhost:8000/analyse -Method Post -ContentType "application/xml" -Body $xml
```

### Option 2: Using PowerShell script

Just run the provided script:
```powershell
.\test_api_simple.ps1
```

### Option 3: Inline XML with curl

```bash
curl -X POST http://localhost:8000/analyse \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?><bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"><bpmn2:process id="Process_1"><bpmn2:startEvent id="StartEvent_1"/><bpmn2:task id="Task_1"/><bpmn2:endEvent id="EndEvent_1"/></bpmn2:process></bpmn2:definitions>'
```

### Option 4: Using Swagger UI (Easiest!)

Visit `http://localhost:8000/docs` and use the interactive API documentation. You can paste your XML directly into the request body.

## Request Format

- **Method:** POST
- **URL:** `http://localhost:8000/analyse`
- **Content-Type:** `application/xml` or `text/xml`
- **Body:** Raw BPMN 2.0 XML content

## Response Format

```json
{
  "stats": {
    "total_processes": 1,
    "total_tasks": 1,
    "total_gateways": 0,
    "total_events": 2,
    ...
  },
  "suggestions": [
    "Consider adding error handling...",
    ...
  ]
}
```

## Example Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1" name="Task 1"/>
    <bpmn2:endEvent id="EndEvent_1"/>
    <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="EndEvent_1"/>
  </bpmn2:process>
</bpmn2:definitions>
```

Just POST this XML directly - no JSON wrapper needed!
