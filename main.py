import uvicorn
from core.config import create_app, custom_openapi
from routes.analyse import router

app = create_app()
app.include_router(router)

app.openapi = lambda: custom_openapi(app)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

