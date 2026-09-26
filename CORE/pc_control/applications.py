import json
import subprocess
import os


# ==============================
# LOAD APPLICATIONS
# ==============================

def load_applications():

    with open(
        "data/applications.json",
        "r",
        encoding="utf-8"
    ) as file:

        applications = json.load(file)

    return applications


# ==============================
# FIND APPLICATION
# ==============================

def find_application(application_name):

    applications = load_applications()

    application_name = application_name.lower().strip()


    for name, path in applications.items():

        if application_name in name.lower():

            return path


    return None


# ==============================
# OPEN APPLICATION
# ==============================

def open_application(application_name):

    application_path = find_application(
        application_name
    )


    # ==============================
    # APPLICATION NOT FOUND
    # ==============================

    if application_path is None:

        return f"I could not find {application_name}."


    # ==============================
    # OPEN APPLICATION
    # ==============================

    try:

        print(
            "Opening:",
            application_path
        )


        # ==============================
        # WINDOWS SHORTCUT
        # ==============================

        if application_path.lower().endswith(".lnk"):

            os.startfile(
                application_path
            )


        # ==============================
        # EXE APPLICATION
        # ==============================

        else:

            subprocess.Popen(
                application_path
            )


        return f"Opening {application_name}."


    except Exception as error:

        print(
            "Application Error:",
            error
        )

        return f"I could not open {application_name}."