import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12
from typing import NamedTuple

from .config import Config
from shared import generic

_config = Config()

class CertificateData(NamedTuple):
    private_key: object
    firmante: object
    emisor: object
    ca_raiz: object
    politica_file: object

class CertificateLoader:
    def __init__(self):
        self._sign_path = os.path.join(_config.PATH_BASE, 'certificados', _config.SIGN_NAME)
        self._sign_password =  _config.SIGN_PASSWORD
        self._security = None
        self._politica_path = os.path.join(_config.PATH_BASE, 'certificados', _config.POLITICA_NAME)

    def load(self):
        with open(self._sign_path, 'rb') as pfx_file:
            pfx_data = pfx_file.read()
        private_key, firmante, additional_certs = pkcs12.load_key_and_certificates(
            pfx_data,
            self._sign_password.encode(),
            default_backend()
        )

        data = {
            'private_key': private_key, 
            'firmante': firmante, 
            'emisor': additional_certs[0],
            'ca_raiz': additional_certs[1],
            'politica_file': ''
            # 'politica_file': generic.read_file(path=self._politica_path, mode='rb')
        }

        self._security = CertificateData(**data)

    @property
    def security(self):
        if not self._security:
            raise ValueError("Certificate data has not been loaded.")
        return self._security
    
certificate_loader = CertificateLoader()