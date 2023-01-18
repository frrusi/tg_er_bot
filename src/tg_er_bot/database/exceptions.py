class DatabaseQueryError(Exception):
    pass


class DataNotFound(DatabaseQueryError):
    def __init__(self, row_id):
        super().__init__(f"String with ID #{row_id} not found")
