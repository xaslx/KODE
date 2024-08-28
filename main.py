from fastapi import FastAPI
from src.routers.auth import auth_router
from src.routers.note import note_router
from fastapi_versioning import VersionedFastAPI


app: FastAPI = FastAPI(title="KODE", version="1")

app.include_router(auth_router)
app.include_router(note_router)

app: VersionedFastAPI = VersionedFastAPI(
    app, version_format="{major}", prefix_format="/v{major}"
)
