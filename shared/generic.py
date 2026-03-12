import os
import io
import re
import base64 
import zipfile
import requests
from datetime import datetime, timedelta
from lxml import etree

def read_file(path: str, mode: str = "r"):
    with open(path, mode) as file:
        file_content = file.read()
    return file_content

def write_file_from_base64(base64_content, output_file_path):
    """
    Escribe un archivo desde un contenido codificado en Base64.
    
    Args:
        base64_content (str): El contenido en Base64 a decodificar.
        output_file_path (str): Ruta donde se guardará el archivo.
    """
    if not base64_content:
        raise ValueError("No se recibio contenido Base64 para guardar el archivo.")

    output_directory = os.path.dirname(output_file_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    # Decodificar el contenido de Base64
    file_content = base64.b64decode(base64_content)
    
    # Escribir el archivo decodificado
    with open(output_file_path, 'wb') as file:
        file.write(file_content)


def make_request(method, url, headers=None, data=None, params=None):
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif method.upper() == 'POST':
        response = requests.post(url, headers=headers, json=data, params=params)
    elif method.upper() == 'PUT':
        response = requests.put(url, headers=headers, json=data, params=params)
    elif method.upper() == 'DELETE':
        response = requests.delete(url, headers=headers, params=params)
    else:
        raise ValueError(f"Invalid method: {method}")

    return response

def get_identification_digit( vat):
    clean_string = re.sub(r'\s+', ' ', vat).strip()
    parts = clean_string.split("-")
    result = parts[1] if len(parts) > 1 else '0'
    return result

def get_period(fecha_str: str):
    date = datetime.strptime(fecha_str, "%Y-%m-%d")
    firt_day = date.replace(day=1)
    
    # Obtener el último día del mes
    next_moth = firt_day.replace(day=28) + timedelta(days=4)
    last_day = next_moth - timedelta(days=next_moth.day)
    
    firt_day = firt_day.strftime("%Y-%m-%d")
    last_day = last_day.strftime("%Y-%m-%d")

    return (firt_day, last_day)

"""
    Convierte un objeto en un diccionario, manejando subobjetos de forma recursiva.
"""
def to_dict(obj):
    if hasattr(obj, "__dict__"):
        return {key: to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}
    else:
        return obj  # Para tipos primitivos
    
def get_sequence(value):
    try:
        number = int(value)
        number += 1
        return str(number)
    except ValueError:
        return "Convert Error in get_id"
    
def compress_file_to_base64(file_path):
    # Crear un buffer en memoria
    buffer = io.BytesIO()
    
    # Comprimir el archivo y guardarlo en el buffer
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_path, arcname=file_path.split('/')[-1])
    
    # Obtener el contenido del buffer
    buffer.seek(0)
    zip_content = buffer.read()
    
    # Codificar el contenido en Base64
    base64_content = base64.b64encode(zip_content).decode('utf-8')
    
    return base64_content

def convert_and_compress_xml_to_base64(xml_root, xml_name):
    """
    Convierte un árbol XML de lxml en un archivo en memoria, 
    lo comprime en un archivo ZIP y lo codifica en Base64.
    
    Args:
        xml_root (etree.Element): El elemento raíz del árbol XML.
    
    Returns:
        str: El contenido del archivo comprimido en formato Base64.
    """
    # Crear un buffer en memoria para el archivo XML
    xml_buffer = io.BytesIO()
    
    # Guardar el árbol XML en el buffer
    xml_tree = etree.ElementTree(xml_root)
    xml_tree.write(xml_buffer, pretty_print=True, encoding='utf-8', xml_declaration=True)
    
    # Resetear el puntero del buffer
    xml_buffer.seek(0)
    
    # Crear un buffer en memoria para el archivo ZIP
    zip_buffer = io.BytesIO()
    
    # Comprimir el archivo XML en el buffer ZIP
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(xml_name, xml_buffer.getvalue())
    
    # Obtener el contenido del buffer ZIP
    zip_buffer.seek(0)
    zip_content = zip_buffer.read()
    
    # Codificar el contenido del ZIP en Base64
    base64_content = base64.b64encode(zip_content).decode('utf-8')
    
    return base64_content

def zip_document(invoice_xml, name_invoice):
    """
    Toma una factura en formato string, la comprime en un archivo ZIP
    y retorna su contenido codificado en Base64.

    Args:
        factura_str (str): La factura en formato texto (string).
        nombre_archivo (str): Nombre del archivo dentro del ZIP. Por defecto es "factura.xml".

    Returns:
        str: El contenido del archivo ZIP codificado en Base64.
    """
    # Crear un buffer en memoria para el archivo ZIP
    buffer_zip = io.BytesIO()
    
    # Crear un archivo ZIP en memoria y añadir la factura como un archivo
    with zipfile.ZipFile(buffer_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_mem:
        zip_mem.writestr(name_invoice, invoice_xml)
    
    # Obtener los bytes del ZIP
    buffer_zip.seek(0)
    zip_bytes = buffer_zip.read()
    
    # Codificar el archivo ZIP en Base64
    base64_encoded = base64.b64encode(zip_bytes).decode('utf-8')
    
    return base64_encoded

def extract_errors_invoice(xml_response):
        if isinstance(xml_response, str):
            xml_response = xml_response.encode('utf-8')

        tree = etree.fromstring(xml_response)
        namespaces = {
            's': 'http://www.w3.org/2003/05/soap-envelope',
            'a': 'http://www.w3.org/2005/08/addressing',
            'u': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd',
            'b': 'http://schemas.datacontract.org/2004/07/DianResponse',
            'c': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
        }
        
        error_elements = tree.findall('.//c:string', namespaces)
        error_messages = [element.text.strip() for element in error_elements if element.text]

        is_valid_element = tree.find('.//b:IsValid', namespaces)
        status_code_element = tree.find('.//b:StatusCode', namespaces)
        status_description_element = tree.find('.//b:StatusDescription', namespaces)
        status_message_element = tree.find('.//b:StatusMessage', namespaces)

        is_valid = is_valid_element.text.lower() if is_valid_element is not None and is_valid_element.text else ''
        status_code = status_code_element.text.strip() if status_code_element is not None and status_code_element.text else ''
        status_description = status_description_element.text.strip() if status_description_element is not None and status_description_element.text else ''
        status_message = status_message_element.text.strip() if status_message_element is not None and status_message_element.text else ''

        if status_description and status_description not in error_messages:
            error_messages.append(status_description)

        if status_message and status_message not in error_messages:
            error_messages.append(status_message)

        if status_code and not error_messages:
            error_messages.append(f'Codigo DIAN: {status_code}')

        return (is_valid, error_messages)