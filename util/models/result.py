from datetime import date

from networkx.drawing.layout import rescale_layout_dict


class Result:
    """
    Super class for result objects which provides some common and universal functionality
    """

    result_identifier: str = None

    @classmethod    
    def generate_file_name(cls) -> str:
        """
        Generates a file name for this instance of results. Uses the `result_identifier` to
        create a file name
        """
        return f"{cls.result_identifier}-{date.today()}"
