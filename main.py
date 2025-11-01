"""
FastAPI application for BPMN 2.0 XML analysis.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Dict, Any, List
from analyzer import BPMNAnalyzer

app = FastAPI(
    title="BPMN Analyzer Service",
    description="A service to analyze BPMN 2.0 XML files and provide statistics and suggestions",
    version="1.0.0"
)


def custom_openapi():
    """Customize OpenAPI schema to properly document XML request body."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Customize the /analyse endpoint to show XML in Swagger
    openapi_schema["paths"]["/analyse"]["post"]["requestBody"] = {
        "required": True,
        "content": {
            "application/xml": {
                "schema": {
                    "type": "string",
                    "format": "xml",
                    "example": """<?xml version="1.0" encoding="UTF-8"?>
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
</bpmn2:definitions>"""
                },
                "examples": {
                    "simple": {
                        "summary": "Simple BPMN Process",
                        "value": """<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn2:process id="Process_1" isExecutable="true">
    <bpmn2:startEvent id="StartEvent_1"/>
    <bpmn2:task id="Task_1" name="Task 1"/>
    <bpmn2:endEvent id="EndEvent_1"/>
    <bpmn2:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <bpmn2:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="EndEvent_1"/>
  </bpmn2:process>
</bpmn2:definitions>"""
                    }
                }
            },
            "text/xml": {
                "schema": {
                    "type": "string",
                    "format": "xml"
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StatsResponse(BaseModel):
    """Response model for statistics."""
    total_processes: int
    total_lanes: int
    total_tasks: int
    task_types: Dict[str, int]
    total_gateways: int
    gateway_types: Dict[str, int]
    total_events: int
    event_types: Dict[str, int]
    total_flows: int
    flow_types: Dict[str, int]
    total_subprocesses: int
    total_data_objects: int
    total_data_stores: int
    has_error_handling: bool
    has_compensation: bool
    complexity_score: int


class AnalysisResponse(BaseModel):
    """Response model for BPMN analysis."""
    stats: StatsResponse
    suggestions: List[str]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "BPMN Analyzer Service",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyse",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post(
    "/analyse",
    response_model=AnalysisResponse,
    summary="Analyze BPMN 2.0 XML",
    description="Accepts BPMN 2.0 XML directly as application/xml or text/xml",
    responses={
        200: {
            "description": "Successful analysis",
            "content": {
                "application/json": {
                    "example": {
                        "stats": {
                            "total_processes": 1,
                            "total_tasks": 1,
                            "task_types": {"default": 1},
                            "total_gateways": 0,
                            "gateway_types": {},
                            "total_events": 2,
                            "event_types": {"start": 1, "end": 1},
                            "total_flows": 2,
                            "flow_types": {"sequence": 2},
                            "total_lanes": 0,
                            "total_subprocesses": 0,
                            "total_data_objects": 0,
                            "total_data_stores": 0,
                            "has_error_handling": False,
                            "has_compensation": False,
                            "complexity_score": 4
                        },
                        "suggestions": [
                            "Consider adding error handling with error boundary events or error end events to improve process robustness."
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Invalid BPMN XML or parsing error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid XML: ..."}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error: ..."}
                }
            }
        }
    }
)
async def analyse_bpmn(request: Request) -> AnalysisResponse:
    """
    Analyze a BPMN 2.0 XML file and return statistics and suggestions.
    
    Accepts BPMN XML directly as the request body with Content-Type: application/xml
    
    Request Body:
        Raw BPMN 2.0 XML content
        
    Returns:
        AnalysisResponse with statistics and suggestions
        
    Raises:
        HTTPException: If the BPMN XML is invalid or cannot be parsed
    """
    try:
        # Read raw XML body
        body = await request.body()
        bpmn_xml = body.decode('utf-8')
        
        if not bpmn_xml or len(bpmn_xml.strip()) == 0:
            raise HTTPException(status_code=400, detail="Empty BPMN XML provided")
        
        analyzer = BPMNAnalyzer(bpmn_xml)
        result = analyzer.analyze()
        
        # Convert stats dict to StatsResponse model
        stats_response = StatsResponse(**result["stats"])
        
        return AnalysisResponse(
            stats=stats_response,
            suggestions=result["suggestions"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

