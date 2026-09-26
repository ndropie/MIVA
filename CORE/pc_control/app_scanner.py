import os
import json
import winreg


# ==============================
# APPLICATION DATABASE
# ==============================

applications = {}


# ==============================
# ADD APPLICATION
# ==============================

def add_application(name, path):

    if not name:
        return

    if not path:
        return

    if not os.path.exists(path):
        return

    name = name.lower().strip()

    if name not in applications:

        applications[name] = path


# ==============================
# SCAN EXE FOLDERS
# ==============================

def scan_folder(location):

    if not os.path.exists(location):
        return

    print("Scanning:", location)

    for root, folders, files in os.walk(location):

        for file in files:

            if file.lower().endswith(".exe"):

                application_name = file[:-4]

                application_path = os.path.join(
                    root,
                    file
                )

                add_application(
                    application_name,
                    application_path
                )


# ==============================
# SCAN START MENU
# ==============================

def scan_start_menu():

    locations = [

        os.path.expandvars(
            r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
        ),

        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        )
    ]

    for location in locations:

        if not os.path.exists(location):
            continue

        print("Scanning Start Menu:", location)

        for root, folders, files in os.walk(location):

            for file in files:

                if file.lower().endswith(".lnk"):

                    name = file[:-4]

                    shortcut_path = os.path.join(
                        root,
                        file
                    )

                    # Store the shortcut.
                    # Windows can launch the shortcut directly.

                    add_shortcut(
                        name,
                        shortcut_path
                    )


# ==============================
# ADD SHORTCUT
# ==============================

def add_shortcut(name, path):

    if not name:
        return

    if not os.path.exists(path):
        return

    name = name.lower().strip()

    if name not in applications:

        applications[name] = path


# ==============================
# SCAN REGISTRY
# ==============================

def scan_registry():

    registry_locations = [

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ),

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ),

        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        )
    ]

    for hive, location in registry_locations:

        try:

            key = winreg.OpenKey(
                hive,
                location
            )

        except:

            continue


        for i in range(winreg.QueryInfoKey(key)[0]):

            try:

                subkey_name = winreg.EnumKey(
                    key,
                    i
                )

                subkey = winreg.OpenKey(
                    key,
                    subkey_name
                )


                try:

                    display_name = winreg.QueryValueEx(
                        subkey,
                        "DisplayName"
                    )[0]

                except:

                    continue


                try:

                    install_location = winreg.QueryValueEx(
                        subkey,
                        "InstallLocation"
                    )[0]

                except:

                    continue


                if install_location:

                    find_exe_in_folder(
                        display_name,
                        install_location
                    )


            except:

                continue


# ==============================
# FIND EXE IN INSTALL LOCATION
# ==============================

def find_exe_in_folder(
    application_name,
    location
):

    if not os.path.exists(location):
        return

    for root, folders, files in os.walk(location):

        for file in files:

            if file.lower().endswith(".exe"):

                path = os.path.join(
                    root,
                    file
                )

                add_application(
                    application_name,
                    path
                )

                return


# ==============================
# SAVE DATABASE
# ==============================

def save_applications():

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        "data/applications.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            applications,
            file,
            indent=4
        )


# ==============================
# RUN SCANNER
# ==============================

print()
print("==============================")
print("MIVA APPLICATION SCANNER")
print("==============================")
print()


# Start Menu

scan_start_menu()


# Program Files

scan_folder(
    r"C:\Program Files"
)

scan_folder(
    r"C:\Program Files (x86)"
)


# Local Programs

scan_folder(
    os.path.expandvars(
        r"%LOCALAPPDATA%\Programs"
    )
)


# Registry

scan_registry()


# Save

save_applications()


print()
print(
    f"Found {len(applications)} applications."
)

print(
    "Application database created."
)