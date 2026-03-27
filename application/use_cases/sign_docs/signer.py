import sys
from lxml import etree
from .xml_signerv3 import XmlSignerV3
from .template_xades import TemplateXades
from shared import certificate_loader, templates_loader
import os

def main():
    try:
        
        # Ruta del XML local
        #xml_file = os.path.join(os.path.dirname(__file__), "invoice.xml")
        #print(f"Leyendo XML desde: {xml_file}")

        #with open(xml_file, "r", encoding="utf-8") as f:
        #    xml_input = f.read()

        #if not xml_input:
        #    raise Exception("El archivo XML está vacío")
        #print(f"XML leído: {xml_input[:100]}...")

        xml_input = sys.stdin.read()
        #print("XML recibido desde stdin:", xml_input)
        if not xml_input.strip():
            raise Exception("No se recibió XML en stdin")

        # ⚡ Inicializar loaders
        certificate_loader.load()
        templates_loader.load()
        #print("Certificados y plantillas cargados.")

        # ⚡ Crear template de firma
        TemplateXades.create_signature_template()

        # ⚡ Convertir string a Element
        invoice_root = etree.fromstring(xml_input.encode("utf-8"))
        #print("XML de factura cargado en memoria como ElementTree.")

        # ⚡ Instanciar signer con Element
        signer = XmlSignerV3(invoice_root, None, "FV")
        #print("Instancia de XmlSignerV3 creada.")

        # ⚡ Firmar
        signed_xml = signer.sign()
        #print("Firma generada correctamente.")

        # ⚡ Guardar resultado en archivo
        output_file = os.path.join(os.path.dirname(__file__), "invoice_signed.xml")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(signed_xml)
        #print(f"XML firmado guardado en: {output_file}", signed_xml)

        print(signed_xml)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()