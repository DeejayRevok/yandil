class MissingTypeHintItemTypeError(Exception):
    def __init__(self):
        super().__init__("Missing type hint item type")
