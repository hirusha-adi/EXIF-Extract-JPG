class Error(Exception):
    """
    Base class for other exceptions
    """
    pass


class ModuleNameError(Exception):
    """
    No Module Name given to install using pip
    """

    def __init__(self, message="No module name is given to install"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return str(self.message)
