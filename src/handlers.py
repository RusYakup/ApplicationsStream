import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse
from src.config import logging_config, settings
from src.kafka import kafka_publisher
from src.modeldb import Application, db_manager
from src.schemas import ApplicationIn

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging_config(settings.LOG_LEVEL)
        log.info("Starting application")

        yield
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


app = FastAPI(lifespan=lifespan)


@app.post("/applications", tags=["Applications"], summary="Create a new application", status_code=201,
          description="Create a new application")
async def create_application(application_in: ApplicationIn, request: Request):
    log.info(f"Received new application from {request.client.host}")
    try:
        print(application_in)
        application = Application(user_name=application_in.user_name,
                                  description=application_in.description)
        await db_manager.add_application(application)
        await kafka_publisher.publish_message("new_applications", {
            "id": application.id,
            "user_name": application.user_name,
            "description": application.description,
            "created_at": application.created_at.isoformat()
        })
        return JSONResponse(status_code=201, content={"message": "Application created successfully"})
    except Exception as e:
        log.error(f"Failed to create application: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/applications", summary="Get list of applications", tags=["Applications"],
         description="Get list of applications")
async def get_applications(request: Request, user_name: str = None, page: int = 1, size: int = 10):
    offset = (page - 1) * size
    applications = await db_manager.get_applications(user_name, offset, size)
    return {"applications": [{"id": app.id, "user_name": app.user_name, "description": app.description,
                              "created_at": app.created_at.isoformat()} for app in applications]}