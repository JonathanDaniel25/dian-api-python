import os
from typing import NamedTuple

class XmlTemplatesData(NamedTuple):
    xml_request: str
    xml_invoice: str
    xml_credit_note: str
    xml_test: str

class XmlLoader:
    def __init__(self):
        self._template = None

    def load(self):
        data = {
            'xml_request': self.template_request, 
            'xml_invoice': self.invoice_template, 
            'xml_credit_note': self.credit_note_template, 
            'xml_test': self.template_test, 
        }
    
        self._template = XmlTemplatesData(**data)

    @property
    def template(self):
        if not self._template:
            raise ValueError("Templates data has not been loaded.")
        return self._template
    
    @property
    def template_request(self):
        xml_request = '''
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wcf="http://wcf.dian.colombia">
            <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
                <wsse:Security
                    xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
                    xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsu:Timestamp wsu:Id="TS-C35717809C92836BA3173565889316046">
                        <wsu:Created />
                        <wsu:Expires />
                    </wsu:Timestamp>
                    <wsse:BinarySecurityToken
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary"
                        ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"
                        wsu:Id="X509-C35717809C92836BA3173565889308341" />
                    <ds:Signature Id="SIG-C35717809C92836BA3173565889315445"
                        xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                        <ds:SignedInfo>
                            <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">
                                <ec:InclusiveNamespaces PrefixList="wsa soap wcf"
                                    xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" />
                            </ds:CanonicalizationMethod>
                            <ds:SignatureMethod
                                Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" />
                            <ds:Reference URI="#id-C35717809C92836BA3173565889308344">
                                <ds:Transforms>
                                    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">
                                        <ec:InclusiveNamespaces PrefixList="soap wcf"
                                            xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" />
                                    </ds:Transform>
                                </ds:Transforms>
                                <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256" />
                                <ds:DigestValue />
                            </ds:Reference>
                        </ds:SignedInfo>
                        <ds:SignatureValue />
                        <ds:KeyInfo Id="KI-C35717809C92836BA3173565889308342">
                            <wsse:SecurityTokenReference wsu:Id="STR-C35717809C92836BA3173565889308343">
                                <wsse:Reference URI="#X509-C35717809C92836BA3173565889308341"
                                    ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" />
                            </wsse:SecurityTokenReference>
                        </ds:KeyInfo>
                    </ds:Signature>
                </wsse:Security>
                <wsa:Action>http://wcf.dian.colombia/IWcfDianCustomerServices/SendBillSync</wsa:Action>
                <wsa:To wsu:Id="id-C35717809C92836BA3173565889308344"
                    xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    https://vpfe-hab.dian.gov.co/WcfDianCustomerServices.svc</wsa:To>
            </soap:Header>
            <soap:Body>
                <wcf:SendBillSync>
                    <wcf:contentFile />
                </wcf:SendBillSync>
            </soap:Body>
        </soap:Envelope>
        '''
        return xml_request
    
    @property
    def template_test(self):
        xml_request = '''
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wcf="http://wcf.dian.colombia">
            <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
                <wsse:Security
                    xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
                    xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsu:Timestamp wsu:Id="TS-C35717809C92836BA3173565889316046">
                        <wsu:Created />
                        <wsu:Expires />
                    </wsu:Timestamp>
                    <wsse:BinarySecurityToken
                        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary"
                        ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"
                        wsu:Id="X509-C35717809C92836BA3173565889308341" />
                    <ds:Signature Id="SIG-C35717809C92836BA3173565889315445"
                        xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                        <ds:SignedInfo>
                            <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">
                                <ec:InclusiveNamespaces PrefixList="wsa soap wcf"
                                    xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" />
                            </ds:CanonicalizationMethod>
                            <ds:SignatureMethod
                                Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" />
                            <ds:Reference URI="#id-C35717809C92836BA3173565889308344">
                                <ds:Transforms>
                                    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">
                                        <ec:InclusiveNamespaces PrefixList="soap wcf"
                                            xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" />
                                    </ds:Transform>
                                </ds:Transforms>
                                <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256" />
                                <ds:DigestValue />
                            </ds:Reference>
                        </ds:SignedInfo>
                        <ds:SignatureValue />
                        <ds:KeyInfo Id="KI-C35717809C92836BA3173565889308342">
                            <wsse:SecurityTokenReference wsu:Id="STR-C35717809C92836BA3173565889308343">
                                <wsse:Reference URI="#X509-C35717809C92836BA3173565889308341"
                                    ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" />
                            </wsse:SecurityTokenReference>
                        </ds:KeyInfo>
                    </ds:Signature>
                </wsse:Security>
                <wsa:Action>http://wcf.dian.colombia/IWcfDianCustomerServices/SendTestSetAsync</wsa:Action>
                <wsa:To wsu:Id="id-C35717809C92836BA3173565889308344"
                    xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    https://vpfe-hab.dian.gov.co/WcfDianCustomerServices.svc</wsa:To>
            </soap:Header>
            <soap:Body>
                <wcf:SendTestSetAsync>
                    <wcf:contentFile />
                    <wcf:testSetId />
                </wcf:SendTestSetAsync>
            </soap:Body>
        </soap:Envelope>
        '''
        return xml_request
    
    @property
    def invoice_template(self):
        # Template para la factura
        root_dir = os.path.abspath(os.curdir)
        xml_invoice_path = os.path.join(root_dir, 'shared','xml_models', 'Generica.xml')
        with open(xml_invoice_path, 'r', encoding='utf-8') as file:
            xml_invoice = file.read()
        return xml_invoice
    
    @property
    def credit_note_template(self):
        # Template para la Nota crédito
        root_dir = os.path.abspath(os.curdir)
        xml_invoice_path = os.path.join(root_dir, 'shared','xml_models', 'CreditNote.xml')
        with open(xml_invoice_path, 'r', encoding='utf-8') as file:
            xml_invoice = file.read()
        return xml_invoice
    
templates_loader = XmlLoader()