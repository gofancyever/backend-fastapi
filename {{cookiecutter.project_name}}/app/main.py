import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException,Response,Request
from app.routers import items, users,pathParms,queryParms,bodyParms,auth,task
from app.database import Base,engine,SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.setting import settings
Base.metadata.create_all(bind=engine)

app = FastAPI(title="{{cookiecutter.project_name}}", description="{{cookiecutter.project_description}}", version="{{cookiecutter.project_version}}",docs_url=settings.docs_url, redoc_url=settings.redoc_url)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(task.router, tags=["队列"])
app.include_router(auth.router,tags=["认证"])
app.include_router(users.router)

app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    pathParms.router,
    prefix="/path",
    tags=["paths"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    queryParms.router,
    prefix="/query",
    tags=["query"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    bodyParms.router,
    prefix="/body",
    tags=["body"],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)