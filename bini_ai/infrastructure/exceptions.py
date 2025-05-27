class BiniPromptException(Exception):
    def __init__(self, exception: Exception,  message: str) -> None:
        super().__init__(f'ERROR | Bini Prompt Exception | {message}, {exception}')
        self.message = message
        self.exception = exception
