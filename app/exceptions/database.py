from typing import Any

class EntityNotFound(Exception):
    def __init__(self, details: dict[str, Any]):
        self.details = details
        super().__init__(self.details)
