

import devices, exceptions
import storage
import device_manager
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk



class DeviceManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Manager")
        self.root.geometry("800x600")
        self.storer = storage.CSVStorage(base_path='data')
        self.device_mgr = device_manager.DeviceManager(self.storer)
        self.storer.load_all(self.device_mgr)
        self.create_widgets()
        self.refresh_device_list()

    def create_widgets(self):
        # Device list
        self.tree = ttk.Treeview(self.root, columns=("Name", "Type", "Status", "Serial", "Location", "Holder", "Value"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="Add Device", command=self.add_device).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Update Device", command=self.update_device).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Device", command=self.delete_device).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save to CSV", command=self.save_devices).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load from CSV", command=self.load_devices).pack(side=tk.LEFT, padx=5)

    def refresh_device_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for d in self.device_mgr.list_devices():
            dev = d.to_dict()
            self.tree.insert("", tk.END, values=(dev["device_name"], dev["device_type"], dev["device_status"], dev["serial_number"], dev["device_location"], dev["device_holder"], dev["value"]))

    def add_device(self):
        try:
            fields = self.prompt_device_fields()
            if not fields:
                return
            self.device_mgr.create_device(**fields)
            self.refresh_device_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        try:
            self.storer.save_all(self.device_mgr)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_device(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Device", "Please select a device to update.")
            return
        serial = self.tree.item(selected[0])["values"][3]
        device = self.device_mgr.read_device(serial)
        fields = self.prompt_device_fields(device)
        if not fields:
            return
        try:
            # Remove serial_number from fields to avoid passing it twice
            if 'serial_number' in fields:
            
                del fields['serial_number']
                
            self.device_mgr.update_device(serial, **fields)
            self.refresh_device_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        try:
            self.storer.save_all(self.device_mgr)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_device(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Device", "Please select a device to delete.")
            return
        serial = self.tree.item(selected[0])["values"][3]
        if messagebox.askyesno("Delete Device", f"Delete device with serial {serial}?"):
            try:
                self.device_mgr.delete_device(serial)
                self.refresh_device_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_devices(self):
        try:
            self.storer.save_all(self.device_mgr)
            messagebox.showinfo("Saved", "Devices saved to CSV.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_devices(self):
        try:
            self.device_mgr.devices.clear()
            self.storer.load_all(self.device_mgr)
            self.refresh_device_list()
            messagebox.showinfo("Loaded", "Devices loaded from CSV.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def prompt_device_fields(self, device=None):
        # Custom dialog for device fields with dropdowns for enums
        dialog = tk.Toplevel(self.root)
        dialog.title("Device Fields")
        dialog.grab_set()
        result = {}

        # Helper to add a label and widget
        def add_row(row, label, widget):
            tk.Label(dialog, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=5)
            widget.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        # Device Name
        name_var = tk.StringVar(value=getattr(device, 'device_name', ''))
        name_entry = tk.Entry(dialog, textvariable=name_var)
        add_row(0, "Device Name", name_entry)

        # Device Type (Enum)
        dtype_var = tk.StringVar(value=(getattr(device, 'device_type', None) and getattr(device.device_type, 'value', None)) or list(e.value for e in devices.DeviceType)[0])
        dtype_combo = ttk.Combobox(dialog, textvariable=dtype_var, values=[e.value for e in devices.DeviceType], state="readonly")
        add_row(1, "Device Type", dtype_combo)

        # Device Status (Enum)
        status_var = tk.StringVar(value=(getattr(device, 'device_status', None) and getattr(device.device_status, 'value', None)) or list(e.value for e in devices.DeviceStatus)[0])
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=[e.value for e in devices.DeviceStatus], state="readonly")
        add_row(2, "Device Status", status_combo)

        # Serial Number
        serial_var = tk.StringVar(value=getattr(device, 'serial_number', ''))
        serial_entry = tk.Entry(dialog, textvariable=serial_var)
        add_row(3, "Serial Number", serial_entry)

        # Device Location (Enum)
        location_var = tk.StringVar(value=(getattr(device, 'device_location', None) and getattr(device.device_location, 'value', None)) or list(e.value for e in devices.Device_location)[0])
        location_combo = ttk.Combobox(dialog, textvariable=location_var, values=[e.value for e in devices.Device_location], state="readonly")
        add_row(4, "Device Location", location_combo)

        # Device Holder
        holder_var = tk.StringVar(value=getattr(device, 'device_holder', ''))
        holder_entry = tk.Entry(dialog, textvariable=holder_var)
        add_row(5, "Device Holder", holder_entry)

        # Value
        value_var = tk.StringVar(value=getattr(device, 'value', ''))
        value_entry = tk.Entry(dialog, textvariable=value_var)
        add_row(6, "Value (Price + Currency)", value_entry)

        # Buttons
        def on_ok():
            try:
                result['device_name'] = name_var.get()
                result['device_type'] = devices.DeviceType(dtype_var.get())
                result['device_status'] = devices.DeviceStatus(status_var.get())
                result['serial_number'] = serial_var.get()
                result['device_location'] = devices.Device_location(location_var.get())
                result['device_holder'] = holder_var.get()
                result['value'] = value_var.get()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}", parent=dialog)

        def on_cancel():
            result.clear()
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="OK", width=10, command=on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()
        return result if result else None


if __name__ == '__main__':
    root = tk.Tk()
    app = DeviceManagerGUI(root)
    root.mainloop()

def print_menu():
    print("\nDevice Manager")
    print("1. List devices")
    print("2. Add device")
    print("3. Update device")
    print("4. Delete device")
    print("5. Save to CSV")
    print("6. Load from CSV")
    print("7. Exit")
    
def submenu(title, actions):
    while True:
        print(f"\n{title}")
        for k,v in actions.items():
            print(f"{k}. {v['label']}")
        choice = input("Choose: ").strip()
        if choice in actions:
            actions[choice]['func']()
        else:
            print("Invalid choice")
        if choice == '0':
            break
"""def main():
    storer = storage.CSVStorage(base_path='data')
    device_mgr = device_manager.DeviceManager(storer)

    print("teeeeeeeeeeeeeeeaaAáaaaaaast")
    storer.load_all(device_mgr)
    try:
        while True:
            
            print_menu()
            choice = input('Select: ').strip()
            if choice == '1':
                print('\n'.join(str(d.to_dict()) for d in device_mgr.list_devices()) or 'No devices')
            elif choice == '2':
                device_mgr.create_device_interactive()
            elif choice == '3':
                device_mgr.update_device_interactive()
            elif choice == '4':
                device_mgr.delete_device_interactive()
            elif choice == '5':
                storer.save_all(device_mgr)
                print('Saved to CSV')
            elif choice == '6':
                storer.load_all(device_mgr)
                print('Loaded from CSV')
            elif choice == '7':
                break
            else:
                print('Invalid choice')
    except exceptions.DeviceManagerError as e:
        print('Error:', e)
    storer.save_all(device_mgr)

if __name__ == '__main__':
    main()
"""