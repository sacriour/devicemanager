import devices, exceptions
import storage
import device_manager
import tkinter as tk


def print_menu():
    print("""Device Manager
1. List Devices
2. Create Device
3. Update Device
4. Delete Device
5. Save to CSV
6. Load from CSV
7. Exit
""")
    

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



def main():
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
