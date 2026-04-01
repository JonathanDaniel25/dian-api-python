from fastapi import APIRouter, UploadFile, File, Form,  HTTPException, status
from fastapi.responses import Response
from lxml import etree
from domain.dtos import InvoiceDto, CreditNoteDto
from application.use_cases import CreateInvoiceCase, CreateNoteCase
from shared import DianRejectedDocumentError, certificate
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
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
        print('xml recibido', voucher)
        voucher_xml_root = etree.fromstring(voucher.encode('utf-8'))
        private_key, firmante, additional_certs = pkcs12.load_key_and_certificates(
            cert_bytes,
            password.encode(),
            default_backend()
        )

        emisor = additional_certs[0] if additional_certs and len(additional_certs) > 0 else None
        ca_raiz = additional_certs[1] if additional_certs and len(additional_certs) > 1 else emisor

        document_type = 'FV'
        root_tag = voucher_xml_root.tag
        if root_tag.endswith('CreditNote') or root_tag.endswith('CreditNote-2'):
            document_type = 'NC'

        signer = XmlSignerV3(
            invoice_xml=voucher_xml_root,
            document_type=document_type,
            private_key=private_key,
            firmante=firmante,
            emisor=emisor,
            ca_raiz=ca_raiz
        )

        signed_voucher = signer.sign()
        print('send sign', signed_voucher)
        return Response(content=signed_voucher, media_type="application/xml")
    except DianRejectedDocumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la factura: " + str(e))
