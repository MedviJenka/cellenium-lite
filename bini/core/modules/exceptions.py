class PromptException(Exception):

    def __init__(self, message: str, exception: Exception) -> None:
        super().__init__(f'error message: {message} | exception{[exception]}')
