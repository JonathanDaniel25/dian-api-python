import sys
import json
from lxml import etree
from shared import certificate_loader, templates_loader
from domain.xml_models import InvoiceXml
from ..sign_docs.xml_signerv3 import XmlSignerV3

def main():
    try:
        # Leer JSON desde stdin
        json_input = sys.stdin.read()

        print("JSON recibido:", json_input, file=sys.stderr)
        if not json_input.strip():
            raise Exception("No se recibió JSON en stdin")

        invoice_json = json.loads(json_input)

        # ⚡ Inicializar loaders
        certificate_loader.load()
        templates_loader.load()

        # ⚡ Crear XML
        invoice_xml = InvoiceXml()

        # ⚡ Control
        control = invoice_json.get("Control", {})
        invoice_xml.Control.StartDate = control.get("StartDate")
        invoice_xml.Control.EndDate = control.get("EndDate")
        invoice_xml.Control.InvoiceAuthorization = control.get("InvoiceAuthorization")
        invoice_xml.Control.Prefix = control.get("Prefix")
        invoice_xml.Control.From = control.get("From")
        invoice_xml.Control.To = control.get("To")
        invoice_xml.Control.ProviderID = control.get("ProviderID")
        invoice_xml.Control.SoftwareID = control.get("SoftwareID")
        invoice_xml.Control.SoftwareSecurityCode = f"{control.get('SoftwareID')}{control.get('Pin')}{invoice_json.get('ID')}"
        invoice_xml.Control.QRCode = f"https://catalogovpfe.dian.gov.co/document/searchqr?documentkey={invoice_json.get('ID')}"
        invoice_xml.Control.ProfileExecutionID = control.get("ProfileExecutionID")

        # ⚡ Company
        company = invoice_json.get("Company", {})
        address = company.get("Address", {})
        invoice_xml.Company.PartyName = company.get("PartyName")
        invoice_xml.Company.CompanyID = company.get("CompanyID")
        invoice_xml.Company.DocumentType = company.get("DocumentType")
        invoice_xml.Company.VerificationDigit = company.get("VerificationDigit")
        invoice_xml.Company.AddressLine = address.get("AddressLine")
        invoice_xml.Company.AddressCityName = address.get("CityName")
        invoice_xml.Company.AddressCountrySubentity = address.get("CountrySubentity")
        invoice_xml.Company.CorporateRegistrationID = control.get("Prefix")

        # ⚡ Customer
        customer = invoice_json.get("Customer", {})
        address_c = customer.get("Address", {})
        invoice_xml.Customer.PartyName = customer.get("PartyName")
        invoice_xml.Customer.CompanyID = customer.get("ID")
        invoice_xml.Customer.DocumentType = customer.get("DocumentType")
        invoice_xml.Customer.AddressLine = address_c.get("AddressLine")
        invoice_xml.Customer.AddressCityName = address_c.get("CityName")
        invoice_xml.Customer.AddressCountrySubentity = address_c.get("CountrySubentity")

        # ⚡ Invoice
        invoice_xml.ID = invoice_json.get("ID")
        invoice_xml.IssueDate = invoice_json.get("IssueDate")
        invoice_xml.IssueTime = invoice_json.get("IssueTime")
        invoice_xml.LineCountNumeric = str(len(invoice_json.get("Lines", [])))

        # ⚡ Amounts
        amounts = invoice_json.get("Amounts", {})
        invoice_xml.Amounts.LineExtensionAmount = amounts.get("LineExtensionAmount")
        invoice_xml.Amounts.TaxExclusiveAmount = amounts.get("TaxExclusiveAmount")
        invoice_xml.Amounts.TaxInclusiveAmount = amounts.get("TaxInclusiveAmount")
        invoice_xml.Amounts.PrepaidAmount = amounts.get("PrepaidAmount")
        invoice_xml.Amounts.PayableAmount = amounts.get("PayableAmount")

        for tax in amounts.get("TaxTotals", []):
            invoice_xml.add_tax_total(
                tax_amount=tax.get("TaxAmount"),
                lines=tax.get("TaxSubtotal", [])
            )

        # ⚡ Lines
        for idx, line in enumerate(invoice_json.get("Lines", [])):
            line['ID'] = idx + 1  # numeración
            invoice_xml.add_invoice_line(**line)

        # ⚡ Crear template de firma y firmar
        from ..sign_docs.template_xades import TemplateXades
        TemplateXades.create_signature_template()

        signer = XmlSignerV3(invoice_xml.get_root, None, "FV")
        signed_xml = signer.sign()

        # ⚡ Retornar XML firmado
        print(signed_xml)

    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()