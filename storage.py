import os, csv
from exceptions import storageError
import devices, exceptions
class CSVStorage:

    def __init__(self, base_path='data'):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, filename, rows, fieldnames):
        path = os.path.join(self.base_path, filename)
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in rows:
                    writer.writerow(r)
        except Exception as e:
            raise storageError(str(e))

    def load(self, filename):
        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            return []
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
        except Exception as e:
            raise storageError(str(e))
        

    def save_all(self, device_mgr):
        self.save('devices.csv', [d.to_dict() for d in device_mgr.list_devices()],
                  ['device_name','device_type','device_status','serial_number','device_location','device_holder'])
        

    def load_all(self, device_mgr):
        device_rows = self.load('devices.csv')
        if device_rows:
            for r in device_rows:
                try:
                    device_mgr.create_device(r['device_name'], devices.DeviceType(r['device_type']),
                                              devices.DeviceStatus(r['device_status']), r['serial_number'],
                                              devices.Device_location(r['device_location']), r['device_holder'])
                except exceptions.DeviceManagerError as e:
                    print('Error loading device:', e)

    