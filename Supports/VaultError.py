class VaultError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class FileNotFound(VaultError):
    ...

class FileTooLarge(VaultError):
    ...

class InvalidName(VaultError):
    ...

class AuthFailed(VaultError):
    ...