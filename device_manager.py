import devices
import exceptions

class DeviceManager:


    def __init__(self, storage):
        self.storage = storage
        self.devices = {}

    def create_device(self, device_name: str, device_type: devices.DeviceType, device_status: devices.DeviceStatus,
                      serial_number: str, device_location: devices.Device_location, device_holder: str):
        """Create a new device and add it to the storage."""
        if serial_number in self.devices:
            raise exceptions.DeviceAlreadyExistsError(f"Device with serial number {serial_number} already exists.")
        device = devices.Device(device_name, device_type, device_status, serial_number, device_location, device_holder)
        self.devices[serial_number] = device
        return device
        

    def read_device(self, serial_number: str):
        """Read a device from the storage."""
        if serial_number not in self.devices:
            raise exceptions.DeviceNotFoundError(f"Device with serial number {serial_number} not found.")
        return self.devices[serial_number]

    def update_device(self, serial_number: str, **kwargs):
        """Update an existing device."""
        if serial_number not in self.devices:
            raise exceptions.DeviceNotFoundError(f"Device with serial number {serial_number} not found.")
        device = self.devices[serial_number]
        for key, value in kwargs.items():
            if hasattr(device, key) and key != "serial_number" :
                setattr(device, key, value)
            elif key == "serial_number" and value != serial_number:
                setattr(device, key, value)
                
            
            else:
                raise exceptions.ValidationError(f"Invalid attribute {key} for device.")
        return device 
    def delete_device(self, serial_number: str):
        """Delete a device from the storage."""
        if serial_number not in self.devices:
            raise exceptions.DeviceNotFoundError(f"Device with serial number {serial_number} not found.")
        else:
            self.devices.pop(serial_number)
    
    def list_devices(self):
        """List all devices in the storage."""
        return list(self.devices.values())

# interactive helpers
    def create_device_interactive(self):
        device_name = input('Device name: ').strip()
        device_type = input('Device type (Laptop, Monitor, Peripheral, Smartphone, Other): ').strip()
        device_status = input('Device status (Active, Inactive, Maintenance, Decommissioned): ').strip()
        serial_number = input('Serial number: ').strip()
        device_location = input('Device location (Madrid, Budapest, London, Berlin; Switzerland): ').strip()
        device_holder = input('Device holder: ').strip()
        try:
            device = self.create_device(device_name, devices.DeviceType(device_type), devices.DeviceStatus(device_status),
                                        serial_number, devices.Device_location(device_location), device_holder)
            print('Created', device.to_dict())
        except exceptions.DeviceManagerError as e:
            print('Error:', e)

    def update_device_interactive(self):
        serial_number = input('Serial number of device to update: ').strip()
        try:
            device = self.read_device(serial_number)
            device_name = input(f'Device name [{device.device_name}]: ').strip() or device.device_name
            device_type = input(f'Device type [{device.device_type.value}]: ').strip() or device.device_type.value
            device_status = input(f'Device status [{device.device_status.value}]: ').strip() or device.device_status.value
            device_location = input(f'Device location [{device.device_location.value}]: ').strip() or device.device_location.value
            device_holder = input(f'Device holder [{device.device_holder}]: ').strip() or device.device_holder
            updated_device = self.update_device(serial_number, device_name=device_name, 
                                               device_type=devices.DeviceType(device_type), 
                                               device_status=devices.DeviceStatus(device_status),
                                               device_location=devices.Device_location(device_location),
                                               device_holder=device_holder)
            print('Updated', updated_device.to_dict())
        except exceptions.DeviceManagerError as e:
            print('Error:', e)

    def delete_device_interactive(self):
        serial_number = input('Serial number of device to delete: ').strip()
        try:
            self.delete_device(serial_number)
            print(f'Device with serial number {serial_number} deleted.')
        except exceptions.DeviceManagerError as e:
            print('Error:', e)