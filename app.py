import logging
import asyncio
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from interfaces.api import invoice_routes
from shared import certificate_loader, templates_loader

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("fastapi_app")

async def load_certificate():
    certificate_loader.load()
    _logger.info("Certificados cargados.")

async def load_templates():
    templates_loader.load()
    _logger.info("Plantillas cargadas.")

async def loads():
    """Ejecuta las cargas en paralelo."""
    await asyncio.gather(load_certificate(), load_templates())
    _logger.info("Todas las tareas de carga completadas.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    _logger.info("Iniciando carga de archivos en segundo plano...")
    # Ejecutar cargas en segundo plano sin bloquear
    asyncio.create_task(loads())
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = []

    for error in exc.errors():
        loc = error.get("loc", [])
        if loc:
            # Convertimos la ubicación a un formato padre.hijo.hijo
            field_path = ".".join(str(part) for part in loc if isinstance(part, str))
            missing_fields.append(field_path)

    return JSONResponse(
        status_code=400,
        content={"missing_fields": missing_fields},
    )

app.include_router(invoice_routes.router)
