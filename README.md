# Proyecto facturacion-electronica-colombia

Este proyecto facturacion-electronica-colombia es una aplicación web desarrollada en Python utilizando el framework FastAPI. Proporciona una API para enviar facturas, notas crédito y prontamente notas débito a la DIAN en Colombia.

Actualmente está operando en ambiente de habilitación. Para más detalles acerca de cómo correr y depurar el proyecto, puedes consultar este video de YouTube:

[Facturación electrónica DIAN COLOMBIA software propio - API GRATIS](https://youtu.be/EaDoYikq-DI?si=W-lIRWI1gwBewll2)

En caso tal de necesitar ayuda me pueden contactar al WhatsApp +57 300 812 0524

---

## Instalación

1. Clona el repositorio desde GitHub:

    ```bash
    git clone https://github.com/Crispancho93/facturacion-electronica-colombia.git
    ```

2. Accede al directorio del proyecto:

    ```bash
    cd facturacion-electronica-colombia
    ```

3. Crea un entorno virtual e instala las dependencias:

    ```bash
    .\venv\Scripts\Activate     #Acticar entorno
    python -m venv venv
    source venv/bin/activate    # Linux / macOS
    .\venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```

    alternativas: 
    - pip install lxml --only-binary :all: 
    - python -m pip install --upgrade pip
    - pip install --upgrade pip setuptools wheel
    - pip install "lxml>=4.9.3"
    - pip install lxml==5.2.1

    .\venv\Scripts\python -m uvicorn app:app --host 0.0.0.0 --reload

## Uso

1. Ejecuta el servidor de desarrollo:

    ```bash
    uvicorn app:app --reload
    ```

2. Accede a la documentación de la API en tu navegador:

    ```
    http://localhost:8000/docs
    ```

3. Realiza solicitudes HTTP a la API utilizando herramientas como cURL o Postman.

## Contribución

¡Agradecemos las contribuciones! Si deseas contribuir al proyecto, sigue estos pasos:

1. Fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y commitealos (`git commit -am 'Agrega nueva característica'`).
4. Sube los cambios a tu repositorio (`git push origin feature/nueva-caracteristica`).
5. Crea un Pull Request.

## Estructura del Proyecto

## Pendiente por validar
1. Validar campo IndustryClasificationCode - Código de actividad que registra en el RUT

---

## Licencia

Este proyecto está licenciado bajo la misma licencia de código abierto que el kernel de Linux: [Licencia GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html). Esto significa que puedes usar, modificar y distribuir el software bajo los términos de la licencia.



## Request Postman

```json
{
  "Control": {
    "TestID": "",
    "StartDate": "2019-01-19",
    "EndDate": "2030-01-19",
    "InvoiceAuthorization": "18760000001",
    "Pin": "12345",
    "Prefix": "SETP",
    "From": "990000000",
    "To": "995000000",
    "ProviderID": "",
    "SoftwareID": "",
    "ProfileExecutionID": "2",
    "TechnicalKey": ""
  },
  "ID": "SETP990000001",
  "IssueDate": "2026-03-12",
  "IssueTime": "10:30:00-05:00",
  "Payment": {
    "PaymentID": "1",
    "PaymentCode": "10",
    "PaymentMeansID": "1",
    "PaymentMeansCode": "10",
    "PaymentDueDate": "2026-03-12"
  },
  "Company": {
    "AdditionalAccountID": "2",
    "PartyName": "",
    "DocumentType": "31",
    "CompanyID": "",
    "VerificationDigit": "1",
    "TaxLevelCode": "O-99",
    "Address": {
      "AddressID": "11001",
      "CountrySubentityCode": "11001",
      "CityName": "Bogota",
      "CountryCode": "CO",
      "CountryName": "Colombia",
      "CountrySubentity": "Bogota",
      "AddressLine": "Calle 123 #45-67"
    }
  },
  "Customer": {
    "ID": "123456789",
    "AdditionalAccountID": "2",
    "PartyName": "CLIENTE PRUEBA",
    "DocumentType": "13",
    "CompanyID": "123456789",
    "Telephone": "3001234567",
    "Email": "cliente@test.com",
    "TaxLevelCode": "O-99",
    "Address": {
      "AddressID": "11001",
      "CountrySubentityCode": "11001",
      "CityName": "Bogota",
      "CountryCode": "CO",
      "CountrySubentity": "Bogota",
      "AddressLine": "Carrera 10 #20-30"
    }
  },
  "Amounts": {
    "LineExtensionAmount": "100000.00",
    "TaxExclusiveAmount": "100000.00",
    "TaxInclusiveAmount": "119000.00",
    "PrepaidAmount": "0.00",
    "PayableAmount": "119000.00",
    "TaxTotals": [
      {
        "TaxAmount": "19000.00",
        "TaxSubtotal": [
          {
            "TaxableAmount": "100000.00",
            "TaxAmount": "19000.00",
            "TaxPercent": "19.00",
            "TaxSchemeID": "01",
            "TaxSchemeName": "IVA"
          }
        ]
      }
    ]
  },
  "Lines": [
    {
      "ID": "1",
      "Quantity": "1.000000",
      "BaseQuantity": "1.000000",
      "LineExtensionAmount": "100000.00",
      "TaxableAmount": "100000.00",
      "TaxAmount": "19000.00",
      "TaxSubtotalAmount": "19000.00",
      "TaxPercent": "19.00",
      "TaxSchemeID": "01",
      "TaxSchemeName": "IVA",
      "SellersItemID": "ITEM001",
      "AdditionalItemID": "001",
      "PriceAmount": "100000.00",
      "Description": "Servicio de prueba DIAN"
    }
  ]
}
```