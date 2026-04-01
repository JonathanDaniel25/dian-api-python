from fastapi import APIRouter, UploadFile, File, Form,  HTTPException, status
from fastapi.responses import Response
from shared import DianRejectedDocumentError
from application.use_cases.sign_docs.xml_signerv3 import XmlSignerV3

router = APIRouter(
    prefix="/api/voucher",
    tags=["voucher"]
)

@router.post("/sign")
async def create(
    voucher: str = Form(...),
    certificate: UploadFile = File(...),
    password: str = Form(...)
):
    cert_bytes = await certificate.read()
    try:
        signer = XmlSignerV3.from_voucher_and_certificate(voucher, cert_bytes, password)
        signed_voucher = signer.sign()
        return Response(content=signed_voucher, media_type="application/xml")
    except DianRejectedDocumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la factura: " + str(e))
