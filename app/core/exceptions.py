class DomainError(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundError(DomainError):
    def __init__(self, detail: str = "Recurso nao encontrado."):
        super().__init__(detail=detail, status_code=404)


class ConflictError(DomainError):
    def __init__(self, detail: str = "Conflito de recurso."):
        super().__init__(detail=detail, status_code=400)


class ConfigurationError(DomainError):
    def __init__(self, detail: str = "Erro de configuracao."):
        super().__init__(detail=detail, status_code=500)


class ExternalServiceError(DomainError):
    def __init__(self, detail: str = "Erro em servico externo.", status_code: int = 500):
        super().__init__(detail=detail, status_code=status_code)
