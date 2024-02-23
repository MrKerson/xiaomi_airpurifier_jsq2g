import enum
import logging
from typing import Any, Dict, Optional

import click

from ....click_common import EnumType, command, format_output
from ....miot_device import DeviceStatus, MiotDevice

_LOGGER = logging.getLogger(__name__)
_MAPPING = {
    # Source https://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:humidifier:0000A00E:deerma-jsqs:2
    # Air Humidifier (siid=2)
    "power": {"siid": 2, "piid": 1},  # bool
    "fault": {"siid": 2, "piid": 2},  # 0 - No Faults, 1 - Insufficient Water, 2 - Water Separation
    "fan_level": {"siid": 2, "piid": 5},  # 1 - lvl1, 2 - lvl2, 3 - lvl3, 4 - auto
    "target_humidity": {"siid": 2, "piid": 6},  # [40, 80] step 1
    "status": {"siid": 2, "piid": 7},  # 1 - Idle, 2 - Busy
    "mode": {"siid": 2, "piid": 8},  # 0 - None, 1 - Constant Humidity
    # Environment (siid=3)
    "relative_humidity": {"siid": 3, "piid": 1},  # [0, 100] step 1
    "temperature": {"siid": 3, "piid": 7},  # [-30, 100] step 1
    # Alarm (siid=5)
    "buzzer": {"siid": 5, "piid": 1},  # bool
    # Light (siid=6)
    "led_light": {"siid": 6, "piid": 1},  # bool
    # Other (siid=7)
    "tank_filed": {"siid": 7, "piid": 1},  # bool
    "water_shortage_fault": {"siid": 7, "piid": 2},  # bool
    "humi_sensor_fault": {"siid": 7, "piid": 3},  # bool
    "temp_sensor_fault": {"siid": 7, "piid": 4},  # bool
    "overwet_protect": {"siid": 7, "piid": 5},  # bool
    "overwet_protect_on": {"siid": 7, "piid": 6},  # bool
    "overtop_humidity": {"siid": 7, "piid": 7},  # bool
    "overtop_humidity": {"siid": 7, "piid": 8},  # bool
}

SUPPORTED_MODELS = [
    "deerma.humidifier.jsq2w",
    "deerma.humidifier.jsq2g",
]
MIOT_MAPPING = {model: _MAPPING for model in SUPPORTED_MODELS}


class OperationMode(enum.Enum):
    Low = 1
    Mid = 2
    High = 3
    Auto = 4


class AirHumidifierJsqsStatus(DeviceStatus):
    

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    # Air Humidifier

    @property
    def is_on(self) -> bool:
        """Return True if device is on."""
        return self.data["power"]

    @property
    def power(self) -> str:
        """Return power state."""
        return "on" if self.is_on else "off"

    @property
    def error(self) -> int:
        """Return error state."""
        return self.data["fault"]

    @property
    def fan_level(self) -> OperationMode:
        """Return current operation fan level."""

        try:
            fan_level = OperationMode(self.data["fan_level"])
        except ValueError as e:
            _LOGGER.exception("Cannot parse fan level: %s", e)
            return OperationMode.Auto

        return fan_level

    @property
    def target_humidity(self) -> Optional[int]:
        """Return target humidity."""
        return self.data.get("target_humidity")

    # Environment

    @property
    def relative_humidity(self) -> Optional[int]:
        """Return current humidity."""
        return self.data.get("relative_humidity")

    @property
    def temperature(self) -> Optional[float]:
        """Return current temperature, if available."""
        return self.data.get("temperature")

    # Alarm

    @property
    def buzzer(self) -> Optional[bool]:
        """Return True if buzzer is on."""
        return self.data.get("buzzer")

    # Indicator Light

    @property
    def led_light(self) -> Optional[bool]:
        """Return status of the LED."""
        return self.data.get("led_light")

    # Other

    @property
    def tank_filed(self) -> Optional[bool]:
        """Return the tank filed."""
        return self.data.get("tank_filed")
    
    @property
    def water_shortage_fault(self) -> Optional[bool]:
        """Return water shortage fault."""
        return self.data.get("water_shortage_fault")

    @property
    def humi_sensor_fault(self) -> Optional[bool]:
        return self.data.get("humi_sensor_fault")

    @property
    def overwet_protect(self) -> Optional[bool]:
        """Return True if overwet mode is active."""
        return self.data.get("overwet_protect") 
    

    @property
    def overwet_protect_on(self) -> Optional[bool]:
        return self.data.get("overwet_protect_on") 
    
    @property
    def overtop_humidity(self) -> Optional[bool]:
        return self.data.get("overtop_humidity") 
    
    @property
    def temp_sensor_fault(self) -> Optional[bool]:
        return self.data.get("temp_sensor_fault") 
    


class AirHumidifierJsqs(MiotDevice):
    """Main class representing the air humidifier which uses MIoT protocol."""

    _mappings = MIOT_MAPPING

    @command(
        default_output=format_output(
            "",
            "Power: {result.power}\n"
            "Error: {result.error}\n"
            "Target Humidity: {result.target_humidity} %\n"
            "Relative Humidity: {result.relative_humidity} %\n"
            "Temperature: {result.temperature} °C\n"
            "Water tank detached: {result.tank_filed}\n"
            "Mode: {result.mode}\n"
            "LED light: {result.led_light}\n"
            "Buzzer: {result.buzzer}\n"
            "Overwet protection: {result.overwet_protect}\n",
        )
    )
    def status(self) -> AirHumidifierJsqsStatus:
        """Retrieve properties."""

        return AirHumidifierJsqsStatus(
            {
                prop["did"]: prop["value"] if prop["code"] == 0 else None
                for prop in self.get_properties_for_mapping()
            }
        )

    @command(default_output=format_output("Powering on"))
    def on(self):
        """Power on."""
        return self.set_property("power", True)

    @command(default_output=format_output("Powering off"))
    def off(self):
        """Power off."""
        return self.set_property("power", False)

    @command(
        click.argument("humidity", type=int),
        default_output=format_output("Setting target humidity {humidity}%"),
    )
    def set_target_humidity(self, humidity: int):
        """Set target humidity."""
        if humidity <= 40 or humidity >= 70:
            raise ValueError(
                "Invalid target humidity: %s. Must be between 40 and 70" % humidity
            )
        return self.set_property("target_humidity", humidity)

    @command(
        click.argument("fan_level", type=EnumType(OperationMode)),
        default_output=format_output("Setting fan_level to '{mode.value}'"),
    )
    def set_fan_level(self, fan_level: OperationMode):
        """Set working fan_level."""
        return self.set_property("fan_level", fan_level.value)

    @command(
        click.argument("light", type=bool),
        default_output=format_output(
            lambda light: "Turning on LED light" if light else "Turning off LED light"
        ),
    )
    def set_light(self, light: bool):
        """Set led light."""
        return self.set_property("led_light", light)

    @command(
        click.argument("buzzer", type=bool),
        default_output=format_output(
            lambda buzzer: "Turning on buzzer" if buzzer else "Turning off buzzer"
        ),
    )
    def set_buzzer(self, buzzer: bool):
        """Set buzzer on/off."""
        return self.set_property("buzzer", buzzer)

    @command(
        click.argument("overwet", type=bool),
        default_output=format_output(
            lambda overwet: "Turning on overwet" if overwet else "Turning off overwet"
        ),
    )
    def set_overwet_protect(self, overwet: bool):
        """Set overwet mode on/off."""
        return self.set_property("overwet_protect", overwet)
    
    

    @command(
        click.argument("overwet_protect_on", type=bool),
        default_output=format_output(
            lambda overwet: "Turning on overwet_protect_on" if overwet else "Turning off overwet_protect_on"
        ),
    )
    def set_overwet_protect_on(self, overwet_protect_on: bool):
        return self.set_property("overwet_protect_on", overwet_protect_on)
