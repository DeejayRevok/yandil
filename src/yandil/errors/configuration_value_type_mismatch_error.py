class ConfigurationValueTypeMismatchError(Exception):
    def __init__(self, configuration_value_name: str, expected_type: type, actual_type: type):
        self.configuration_value_name = configuration_value_name
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__(
            f"Expected type for configuration value {configuration_value_name} "
            f"was {expected_type}, got {actual_type}"
        )
