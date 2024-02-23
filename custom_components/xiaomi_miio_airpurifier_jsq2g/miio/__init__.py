# flake8: noqa
from importlib.metadata import version  # type: ignore

# Library imports need to be on top to avoid problems with
# circular dependencies. As these do not change that often
# they can be marked to be skipped for isort runs.

# isort: off

from .device import Device
from .devicestatus import DeviceStatus
from .exceptions import (
    DeviceError,
    InvalidTokenException,
    DeviceException,
    UnsupportedFeatureException,
    DeviceInfoUnavailableException,
)
from .miot_device import MiotDevice
from .deviceinfo import DeviceInfo

# isort: on

from .cloud import CloudDeviceInfo, CloudException, CloudInterface
from .descriptorcollection import DescriptorCollection
from .descriptors import (
    AccessFlags,
    ActionDescriptor,
    Descriptor,
    EnumDescriptor,
    PropertyDescriptor,
    RangeDescriptor,
    ValidSettingRange,
)
from .devicefactory import DeviceFactory
from .integrations.airdog.airpurifier import AirDogX3
from .integrations.cgllc.airmonitor import AirQualityMonitor, AirQualityMonitorCGDN1
from .integrations.chuangmi.camera import ChuangmiCamera
from .integrations.chuangmi.plug import ChuangmiPlug
from .integrations.chuangmi.remote import ChuangmiIr
from .integrations.chunmi.cooker import Cooker
from .integrations.deerma.humidifier import AirHumidifierJsqs, AirHumidifierMjjsq
from .integrations.dmaker.airfresh import AirFreshA1, AirFreshT2017
from .integrations.dmaker.fan import Fan1C, FanMiot, FanP5
from .integrations.dreame.vacuum import DreameVacuum
from .integrations.genericmiot.genericmiot import GenericMiot
from .integrations.huayi.light import (
    Huizuo,
    HuizuoLampFan,
    HuizuoLampHeater,
    HuizuoLampScene,
)
from .integrations.ijai.vacuum import Pro2Vacuum
from .integrations.ksmb.walkingpad import Walkingpad
from .integrations.leshow.fan import FanLeshow
from .integrations.lumi.acpartner import (
    AirConditioningCompanion,
    AirConditioningCompanionMcn02,
    AirConditioningCompanionV3,
)
from .integrations.lumi.camera.aqaracamera import AqaraCamera
from .integrations.lumi.curtain import CurtainMiot
from .integrations.lumi.gateway import Gateway
from .integrations.mijia.vacuum import G1Vacuum
from .integrations.mmgg.petwaterdispenser import PetWaterDispenser
from .integrations.nwt.dehumidifier import AirDehumidifier
from .integrations.philips.light import (
    Ceil,
    PhilipsBulb,
    PhilipsEyecare,
    PhilipsMoonlight,
    PhilipsRwread,
    PhilipsWhiteBulb,
)
from .integrations.pwzn.relay import PwznRelay
from .integrations.roborock.vacuum import RoborockVacuum
from .integrations.roidmi.vacuum import RoidmiVacuumMiot
from .integrations.scishare.coffee import ScishareCoffee
from .integrations.shuii.humidifier import AirHumidifierJsq
from .integrations.tinymu.toiletlid import Toiletlid
from .integrations.viomi.vacuum import ViomiVacuum
from .integrations.viomi.viomidishwasher import ViomiDishwasher
from .integrations.xiaomi.aircondition.airconditioner_miot import AirConditionerMiot
from .integrations.xiaomi.repeater.wifirepeater import WifiRepeater
from .integrations.xiaomi.wifispeaker.wifispeaker import WifiSpeaker
from .integrations.yeelight.dual_switch import YeelightDualControlModule
from .integrations.yeelight.light import Yeelight
from .integrations.yunmi.waterpurifier import WaterPurifier, WaterPurifierYunmi
from .integrations.zhimi.airpurifier import AirFresh, AirPurifier, AirPurifierMiot
from .integrations.zhimi.fan import Fan, FanZA5
from .integrations.zhimi.heater import Heater, HeaterMiot
from .integrations.zhimi.humidifier import AirHumidifier, AirHumidifierMiot
from .integrations.zimi.powerstrip import PowerStrip
from .protocol import Message, Utils
from .push_server import EventInfo, PushServer

from .discovery import Discovery


def __getattr__(name):
    """Create deprecation warnings on classes that are going away."""
    from warnings import warn

    current_globals = globals()

    def _is_miio_integration(x):
        """Return True if miio.integrations is in the module 'path'."""
        module_ = current_globals[x]
        if "miio.integrations" in str(module_):
            return True

        return False

    deprecated_module_mapping = {
        str(x): current_globals[x] for x in current_globals if _is_miio_integration(x)
    }
    if new_module := deprecated_module_mapping.get(name):
        warn(
            f"Importing {name} directly from 'miio' is deprecated, import {new_module} or use DeviceFactory.create() instead",
            DeprecationWarning,
        )
        return globals()[new_module.__name__]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__version__ = version("python-miio")
