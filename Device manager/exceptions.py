class DeviceManagerError(Exception):pass
class ValidationError(DeviceManagerError):pass
class DeviceNotFoundError(DeviceManagerError):pass
class DeviceAlreadyExistsError(DeviceManagerError):pass
class storageError(DeviceManagerError):pass