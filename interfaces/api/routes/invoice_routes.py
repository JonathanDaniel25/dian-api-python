from fastapi import APIRouter, HTTPException, status
from domain.dtos import InvoiceDto, CreditNoteDto
from application.use_cases import CreateInvoiceCase, CreateNoteCase
from shared import DianRejectedDocumentError

router = APIRouter(
    prefix="/api/invoice",
    tags=["invoice"]
)

@router.post("/create_invoice")
def create(request: InvoiceDto):
    try:
        create_invoice = CreateInvoiceCase(request)
        return create_invoice.send()
    except DianRejectedDocumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la factura: " + str(e))
    
@router.post("/send_test")
def create(request: InvoiceDto):
    try:
        create_invoice = CreateInvoiceCase(request)
        return create_invoice.send_test()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la factura: " + str(e))

@router.post("/create_credit_note")
def create(request: CreditNoteDto):
    try:
        create_note = CreateNoteCase(request)
        return create_note.start()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la factura: " + str(e))