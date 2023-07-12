from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from app_dash import create_dash_app


app = FastAPI()


@app.get("/")
def hello():
    return {"str": "hello world"}


@app.get("/status")
def get_status():
    return {"status": "ok"}

@app.get("/st")
def get_status():
    return {"st": "hahaha"}


dash_app = create_dash_app(requests_pathname_prefix="/dash/")
app.mount("/dash", WSGIMiddleware(dash_app.server))



if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)

    server = uvicorn.run(
        "server_fastapi:app", 
        host="0.0.0.0", 
        port=8000, 
        log_level="info", 
        access_log=False, 
        reload=True
    )
