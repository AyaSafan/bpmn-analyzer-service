from fastapi import APIRouter, Request, HTTPException
from models.responses import StatsResponse, AnalysisResponse
from services.analyzer import BPMNAnalyzer

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "BPMN Analyzer Service",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyse",
            "docs": "/docs"
        }
    }



@router.post(
    "/analyse",
    response_model=AnalysisResponse,
    summary="Analyze BPMN 2.0 XML",
    description="Accepts BPMN 2.0 XML directly as application/xml or text/xml"
)
async def analyse_bpmn(request: Request) -> AnalysisResponse:
    try:
        body = await request.body()
        bpmn_xml = body.decode('utf-8')

        if not bpmn_xml.strip():
            raise HTTPException(status_code=400, detail="Empty BPMN XML provided")

        analyzer = BPMNAnalyzer(bpmn_xml)
        result = analyzer.analyze()

        stats_response = StatsResponse(**result["stats"])
        return AnalysisResponse(stats=stats_response, suggestions=result["suggestions"])

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
