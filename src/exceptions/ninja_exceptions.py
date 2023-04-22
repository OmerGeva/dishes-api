class NinjaTimeoutException(Exception):
    def __init__(self, message="Ninja could not be reached!"):
        self.message = message
        super().__init__(self.message)

class NinjaEmptyException(Exception):
    def __init__(self, message="Ninja has no nutrients based on the name provided!"):
        self.message = message
        super().__init__(self.message)