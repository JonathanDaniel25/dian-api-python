import os
import threading
from shared import Config, DianRejectedDocumentError, generic
from domain.xml_models import InvoiceXml
from domain.dtos import ControlDto, InvoiceDto
from ..sign_docs.xml_signerv3 import XmlSignerV3
from ..soap.soap_invoice import SoapRequest
from ..soap.soap_test import SoapRequestTest

_config = Config()

class CreateInvoiceCase:
    def __init__(self, invoice: InvoiceDto):
        self.invoice = invoice
        self.xml = InvoiceXml()
        self.soap_invoice = SoapRequest()
        self.soap_test = SoapRequestTest(invoice.Control.TestID)

        self.xml_name = f'FV{self.invoice.ID}.xml'
        self.zip_name = f'FV{self.invoice.ID}.zip'

        self.zip_full_path = os.path.join(_config.PATH_BASE, self.invoice.Control.InvoiceAuthorization, 'XMLFacturas', self.zip_name)

    @property
    def cufe(self):
        data = {
            "NumFac": self.invoice.ID,
            "FecFac": self.invoice.IssueDate,
            "HorFac": self.invoice.IssueTime,
            "ValFac": self.invoice.Amounts.LineExtensionAmount,
            # IVA
            "CodImp1": '01', 
            "ValImp1": self.invoice.Amounts.TaxTotals[0].TaxAmount,
            # Impuesto Nacional al Consumo
            "CodImp2": '04',
            "ValImp2": '0.00',
            # ICA
            "CodImp3": '03', 
            "ValImp3": '0.00',
            "ValTot": self.invoice.Amounts.TaxInclusiveAmount,
            "NitOFE": self.invoice.Company.CompanyID,
            "NumAdq": self.invoice.Customer.ID,
            "ClTec": self.invoice.Control.TechnicalKey,
            "TipoAmbiente": self.invoice.Control.ProfileExecutionID
        }
        return self.xml.get_cufe(data)

    def _create(self):
        # Llenar el xml de la factura con todos los datos
        self._set_control(self.invoice.Control)
        self._set_company()
        self._set_customer()
        self._set_invoice()
        self._set_amounts()
        self._set_payment()
        self._set_lines()

        # Firmar Factura
        self.signer = XmlSignerV3(self.xml.get_root, self.invoice, 'FV')
        signed_invoice = self.signer.sign()
        
        return signed_invoice
 
    def send(self):
        signed_invoice = self._create()

        # Comprimir Factura
        zip_invoice = generic.zip_document(signed_invoice, self.xml_name)

        # Guardar .zip en un segundo plano
        args = (zip_invoice, self.zip_full_path)
        thread = threading.Thread(target=generic.write_file_from_base64, args=args)
        thread.start()

        # Enviar la Factura
        try:
            response = self.soap_invoice.send_xml(zip_invoice)
            is_valid, messages = generic.extract_errors_invoice(response.text)

            if is_valid == 'false':
                print(f"Error al enviar la factura. XML enviado: {self.xml_name}")
                print(f"Error al enviar la factura. Respuesta XML: {response.text}")
                detail = messages[0] if len(messages) == 1 else messages
                raise DianRejectedDocumentError("La DIAN rechazo el documento.", detail)
            
        except Exception as e:
            print(f"Error al enviar la factura. XML enviado: {self.xml_name}")
            print(f"Error al enviar la factura. Respuesta XML: {e}")
            raise
        
        return messages

    def send_test(self):
        signed_invoice = self._create()

        # Comprimir Factura
        zip_invoice = generic.zip_document(signed_invoice, self.xml_name)

        # Guardar .zip en un segundo plano
        args = (zip_invoice, self.zip_full_path)
        thread = threading.Thread(target=generic.write_file_from_base64, args=args)
        thread.start()

        # Enviar la Factura
        try:
            response = self.soap_test.send_xml(zip_invoice)
            return { "status": response.status_code, "text": response.text }
        except Exception as e:
            print(f"Error al enviar la factura. XML enviado: {self.xml_name}")
            print(f"Error al enviar la factura. Respuesta XML: {e}")
            raise

    def _set_customer(self):
        self.xml.Customer.AdditionalAccountID = self.invoice.Customer.AdditionalAccountID
        self.xml.Customer.PartyName = self.invoice.Customer.PartyName
        self.xml.Customer.CompanyID = self.invoice.Customer.ID
        self.xml.Customer.DocumentType = self.invoice.Customer.DocumentType
        self.xml.Customer.PartyIdentificationID = self.invoice.Customer.ID
        self.xml.Customer.TaxLevelCode = self.invoice.Customer.TaxLevelCode
        
        self.xml.Customer.AddressID = self.invoice.Customer.Address.AddressID
        self.xml.Customer.AddressCountrySubentityCode = self.invoice.Customer.Address.CountrySubentityCode
        self.xml.Customer.AddressCityName = self.invoice.Customer.Address.CityName
        self.xml.Customer.AddressCountrySubentity = self.invoice.Customer.Address.CountrySubentity
        self.xml.Customer.AddressLine = self.invoice.Customer.Address.AddressLine

        self.xml.Customer.RegistrationName = self.invoice.Customer.PartyName
        self.xml.Customer.RegistrationID = self.invoice.Customer.ID
        self.xml.Customer.RegistrationCountrySubentityCode = self.invoice.Customer.Address.CountrySubentityCode
        self.xml.Customer.RegistrationCityName = self.invoice.Customer.Address.CityName
        self.xml.Customer.RegistrationCountrySubentity = self.invoice.Customer.Address.CountrySubentity
        self.xml.Customer.RegistrationAddressLine = self.invoice.Customer.Address.AddressLine

        self.xml.Customer.LegalRegistrationName = self.invoice.Customer.PartyName
        self.xml.Customer.LegalCompanyID = self.invoice.Customer.ID
        self.xml.Customer.LegalDocumentType = self.invoice.Customer.DocumentType
    
    def _set_company(self):
        self.xml.Company.AdditionalAccountID = self.invoice.Company.AdditionalAccountID
        self.xml.Company.PartyName = self.invoice.Company.PartyName
        self.xml.Company.CompanyID = self.invoice.Company.CompanyID
        self.xml.Company.DocumentType = self.invoice.Company.DocumentType
        self.xml.Company.VerificationDigit = self.invoice.Company.VerificationDigit
        self.xml.Company.TaxLevelCode = self.invoice.Company.TaxLevelCode
        
        self.xml.Company.AddressID = self.invoice.Company.Address.AddressID
        self.xml.Company.AddressCityName = self.invoice.Company.Address.CityName
        self.xml.Company.AddressCountrySubentityCode = self.invoice.Company.Address.CountrySubentityCode
        self.xml.Company.AddressCountrySubentity = self.invoice.Company.Address.CountrySubentity
        self.xml.Company.AddressLine = self.invoice.Company.Address.AddressLine

        self.xml.Company.RegistrationName = self.invoice.Company.PartyName
        self.xml.Company.RegistrationID = self.invoice.Company.Address.AddressID
        self.xml.Company.RegistrationCityName = self.invoice.Company.Address.CityName
        self.xml.Company.RegistrationCountrySubentityCode = self.invoice.Company.Address.CountrySubentityCode
        self.xml.Company.RegistrationCountrySubentity = self.invoice.Company.Address.CountrySubentity
        self.xml.Company.RegistrationAddressLine = self.invoice.Company.Address.AddressLine

        self.xml.Company.LegalRegistrationName = self.invoice.Company.PartyName
        self.xml.Company.LegalCompanyID = self.invoice.Company.CompanyID
        self.xml.Company.LegalDocumentType = self.invoice.Company.DocumentType
        self.xml.Company.LegalVerificationDigit = self.invoice.Company.VerificationDigit

        self.xml.Company.CorporateRegistrationID = self.invoice.Control.Prefix
    
    def _set_lines(self):
        for index, line in enumerate(self.invoice.Lines):
            line.ID = index  + 1
            self.xml.add_invoice_line(line.__dict__)
    
    def _set_amounts(self):
        self.xml.Amounts.LineExtensionAmount = self.invoice.Amounts.LineExtensionAmount #  Subtotal - Total Valor Bruto antes de tributos
        self.xml.Amounts.TaxExclusiveAmount = self.invoice.Amounts.TaxExclusiveAmount #  Subtotal - Total Valor Bruto antes de tributos
        self.xml.Amounts.TaxInclusiveAmount = self.invoice.Amounts.TaxInclusiveAmount # Total de Valor Bruto mas tributos
        self.xml.Amounts.PrepaidAmount = self.invoice.Amounts.PrepaidAmount # 
        self.xml.Amounts.PayableAmount = self.invoice.Amounts.PayableAmount # Total que paga el cliente - Total de Valor Bruto mas tributos

        # 13.2.2 Tributos, Lista de tributos que general la factura
        for item in self.invoice.Amounts.TaxTotals:
            tax_data = {
                "tax_amount": item.TaxAmount, # Total del impuesto generado (IVA/IC/ICA)
                "lines": item.TaxSubtotal
            }
            self.xml.add_tax_total(**tax_data)
    
    def _set_payment(self):
        self.xml.Payment.PaymentID = self.invoice.Payment.PaymentID
        self.xml.Payment.PaymentCode = self.invoice.Payment.PaymentCode

    def _set_invoice(self):
        firt_day, last_day = generic.get_period(self.invoice.IssueDate)

        self.xml.ID = self.invoice.ID
        self.xml.IssueDate = self.invoice.IssueDate
        self.xml.IssueTime = self.invoice.IssueTime
        self.xml.LineCountNumeric = str(len(self.invoice.Lines))
        self.xml.PeriodStartDate = firt_day
        self.xml.PeriodEndDate = last_day
        self.xml.UUID = self.cufe

    def _set_control(self, control: ControlDto):
        self.xml.Control.StartDate = control.StartDate
        self.xml.Control.EndDate = control.EndDate
        self.xml.Control.InvoiceAuthorization = control.InvoiceAuthorization
        self.xml.Control.Prefix = control.Prefix
        self.xml.Control.From = control.From
        self.xml.Control.To = control.To
        self.xml.Control.ProviderID = control.ProviderID
        self.xml.Control.SoftwareID = control.SoftwareID
        self.xml.Control.SoftwareSecurityCode = f"{control.SoftwareID}{control.Pin}{self.invoice.ID}"
        self.xml.Control.QRCode = f'https://catalogovpfe.dian.gov.co/document/searchqr?documentkey={self.cufe}'
        self.xml.Control.ProfileExecutionID = control.ProfileExecutionID

        self.xml.Control.VerificationDigit = self.invoice.Company.VerificationDigit