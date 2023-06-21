class MissingConfigurationValueError(Exception):
    def __init__(self, configuration_value_name: str):
        self.configuration_value_name = configuration_value_name
        super().__init__(f"Missing configuration value for {configuration_value_name}")
