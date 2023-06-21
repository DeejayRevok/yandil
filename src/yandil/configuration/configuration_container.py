from typing import Any, Dict, Optional

from yandil.configuration.environment import Environment


class ConfigurationContainer:
    def __init__(self):
        self.__configurations_map: Dict[str, Any] = {}

    def __getitem__(self, configuration_key: str) -> Optional[Any]:
        configuration_value = self.__configurations_map.get(configuration_key)
        if configuration_value is None:
            return None

        if isinstance(configuration_value, Environment):
            configuration_value = configuration_value.resolve()

        return configuration_value

    def __setitem__(self, configuration_key: str, configuration_value: Any) -> None:
        self.__configurations_map[configuration_key] = configuration_value


default_configuration_container = ConfigurationContainer()
