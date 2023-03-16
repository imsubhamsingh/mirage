import os
import sys
import string
import random
import subprocess
import argparse

DEBUG = False


def create_environment(name):
    # Create a new virtual environment
    if sys.version_info.major >= 3:
        if DEBUG:
            print("RUNNing on python3")
        subprocess.check_call([sys.executable, "-m", "venv", name])
    else:
        if DEBUG:
            print("RUNNing on python2")
        subprocess.check_call([sys.executable, "-m", "virtualenv", name])

    # Activate the virtual environment
    if os.name == "nt":
        activate_cmd = "Scripts\\activate.bat"
    else:
        activate_cmd = "bin/activate"
    activate_script = os.path.join(name, activate_cmd)

    if not os.path.exists(activate_script):
        # Fix bash compatibility issues
        activate_cmd = activate_cmd.replace("/", "\\")
        activate_content = ""
        with open(activate_script + ".sh", "r") as f:
            for line in f.readlines():
                activate_content += line.replace("$", "").replace(
                    "{BASH_SOURCE-}", "$0"
                )

        # Create fixed bash script
        with open(activate_script, "w") as f:
            f.write(activate_content)

    subprocess.check_call(["/bin/bash", "-c", "source %s" % activate_script])

    # Install pip and setuptools
    subprocess.check_call(["python", "-m", "ensurepip"])
    subprocess.check_call(
        ["python", "-m", "pip", "install", "--upgrade", "pip", "setuptools"]
    )


def install_packages(requirements_file):
    # Install packages from the given requirements file
    subprocess.check_call(["pip", "install", "-r", requirements_file])


def uninstall_package(package):
    # Check if a requirements file was provided
    if package.endswith(".txt"):
        subprocess.check_call(["pip", "uninstall", "-y", "-r", package])
    else:
        subprocess.check_call(["pip", "uninstall", "-y", package])


def list_packages(details=False):
    # List all installed packages
    args = ["pip", "freeze"]
    if details:
        args.append("--all")
    output = subprocess.check_output(args)
    print(output.decode("utf-8"))


def run_command(command):
    # Run a command in the virtual environment
    subprocess.check_call(command, shell=True)


def shell():
    # Spawns a new shell within the newly created random virtual environment
    env_name = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])

    create_environment(env_name)
    print(env_name)

    # Activate/start  the virtual environment also
    if os.name == "nt":
        activate_cmd = "Scripts\\activate.bat"
    else:
        activate_cmd = "bin/activate"

    activate_script = os.path.join(env_name, activate_cmd)

    subprocess.call(["chmod", "+x", activate_script])  # Make activate script executable
    subprocess.call(
        ["bash", "-c", "source {}".format(activate_script)]
    )  # Activate the virtual environment

    print("Activated virtual environment")


def deactivate():
    # Exit the virtual environment
    VIRTUAL_ENV = os.environ.get("VIRTUAL_ENV")
    if VIRTUAL_ENV:
        subprocess.call("deactivate", shell=True)
    else:
        print("No virtual environment currently active.")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser(
        "create", help="Create a new virtual environment"
    )
    create_parser.add_argument("name", help="Name of the virtual environment")

    install_parser = subparsers.add_parser(
        "install", help="Install packages in the virtual environment"
    )

    # ask user for either a single package name or the requirements.txt file
    install_parser.add_argument(
        "package",
        nargs="?",
        help="Name of package to install (default: installs from requirements file)",
    )

    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall packages in the virtual environment"
    )
    uninstall_parser.add_argument(
        "package",
        nargs="?",
        help="Name of package to uninstall (default: uninstalls from requirements file)",
    )

    list_parser = subparsers.add_parser("list", help="List all the installed packages")
    list_parser.add_argument(
        "--details",
        "-d",
        action="store_true",
        help="Show details beside the package names",
    )

    shell_parser = subparsers.add_parser(
        "shell", help="Spawn a shell within the virtual environment"
    )

    deactivate_parser = subparsers.add_parser(
        "deactivate", help="Deactivate the virtual environment"
    )

    args = parser.parse_args()

    if args.command == "create":
        create_environment(args.name)
    elif args.command == "install":
        install_packages(package=args.package)
    elif args.command == "uninstall":
        uninstall_package(args.package)
    elif args.command == "list":
        list_packages(details=args.details)
    elif args.command == "run":
        run_command(args.command_line)
    elif args.command == "shell":
        shell()
    elif args.command == "deactivate":
        deactivate()
    else:
        print("Invalid command entered: %s" % args.command)


if __name__ == "__main__":
    main()
