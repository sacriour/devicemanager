from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Enum to represent the type of device."""
    LAPTOP = "Laptop"
    Monitor = "Desktop"
    Peripheral = "Peripheral"
    SMARTPHONE = "Smartphone"
    OTHER = "Other"

class DeviceStatus(Enum):
    """Enum to represent the status of a device."""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    MAINTENANCE = "Maintenance"
    DECOMMISSIONED = "Decommissioned"


class Device_location(Enum):
    """Enum to represent the location of a device."""
    MADRID = "Madrid"
    BUDAPEST = "Budapest"
    LONDON = "London"
    BERLIN = "Berlin"
    SWITZERLAND = "Switzerland"



class Device:
    """Class to represent the devices in the system."""

    device_name: str
    device_type: DeviceType
    device_status: DeviceStatus
    serial_number: str
    device_location: Device_location
    device_holder: str

    def __init__(self, device_name: str, device_type: DeviceType, device_status: DeviceStatus,
                 serial_number: str, device_location: Device_location, device_holder: str):
        self.device_name = device_name
        self.device_type = device_type
        self.device_status = device_status
        self.serial_number = serial_number
        self.device_location = device_location
        self.device_holder = device_holder

    def to_dict(self):
        """Convert the device object to a dictionary."""
        return {
            "device_name": self.device_name,
            "device_type": self.device_type.value,
            "device_status": self.device_status.value,
            "serial_number": self.serial_number,
            "device_location": self.device_location.value,
            "device_holder": self.device_holder
        }