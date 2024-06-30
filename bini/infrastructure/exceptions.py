class BiniResponseError(Exception):
    def __init__(self, outcome: object, response: str, exception: Exception) -> None:
        super().__init__(f'outcome: {outcome} response error: {response} , error: {[exception]}')
