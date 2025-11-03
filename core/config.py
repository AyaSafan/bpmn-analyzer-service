from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

def create_app() -> FastAPI:
    app = FastAPI(
        title="BPMN Analyzer Service",
        description="A service to analyze BPMN 2.0 XML files and provide statistics and suggestions",
        version="1.0.0"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Remove duplicate example: Provide only in "examples", not in "schema.example"
    example_xml = """"""

    openapi_schema["paths"]["/analyse"]["post"]["requestBody"] = {
        "required": True,
        "content": {
            "application/xml": {
                "schema": {
                    "type": "string",
                    "format": "xml"
                },
                "examples": {
                    "simple": {
                        "summary": "Simple BPMN Process",
                        "value": example_xml
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