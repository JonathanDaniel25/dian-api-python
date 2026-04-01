import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from interfaces.api import invoice_routes

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("fastapi_app")

app = FastAPI()

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
