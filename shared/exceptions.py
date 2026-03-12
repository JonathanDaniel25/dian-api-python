class DianRejectedDocumentError(Exception):
    def __init__(self, message: str, details=None):
        super().__init__(message)
        self.details = details or []