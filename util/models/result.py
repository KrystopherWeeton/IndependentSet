from datetime import date


class Result:
    """
    Super class for result objects which provides some common and universal functionality
    """

    def __init__(self, result_identifier: str):
        self.result_identifier: str = result_identifier

    
    def generate_file_name(self) -> str:
        """
        Generates a file name for this instance of results. Uses the `result_identifier` to
        create a file name
        """
        return f"{self.result_identifier}-{date.today()}"
