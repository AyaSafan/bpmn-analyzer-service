# BPMN Analyzer Service

A FastAPI-based backend service that reads BPMN 2.0 XML files, analyzes them, and provides statistics and suggestions.

## Features

- Analyzes BPMN 2.0 XML files
- Provides comprehensive statistics about process elements
- Provides actionable suggestions for process improvement
- RESTful API endpoint `/analyse`

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the service is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoint

### POST `/analyse`

Analyzes a BPMN 2.0 XML file and returns statistics and suggestions.

**Request:**
- **Content-Type:** `application/xml` or `text/xml`
- **Body:** Raw BPMN 2.0 XML content

**Example using curl:**
```bash
curl -X POST http://localhost:8000/analyse \
  -H "Content-Type: application/xml" \
  -d @your_file.bpmn
```

**Response:**
```json
{
  "stats": {
    "total_processes": 1,
    "total_tasks": 5,
    "total_gateways": 2,
    "total_events": 3,
    ...
  },
  "suggestions": [
    "Consider adding error handling...",
    ...
  ]
}
```

## Testing

```bash
pytest
```

## CI/CD

The project includes GitHub Actions workflow for automated testing on push and pull requests.

