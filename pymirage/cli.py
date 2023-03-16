import os
import sys
import subprocess
import argparse

def create_environment(name):
    # Create a new virtual environment
    if sys.version_info.major >= 3:
        subprocess.check_call([sys.executable, '-m', 'venv', name])
    else:
        subprocess.check_call([sys.executable, '-m', 'virtualenv', name])

    # Activate the virtual environment
    if os.name == 'nt':
        activate_cmd = 'Scripts\\activate.bat'
    else:
        activate_cmd = 'bin/activate'
    activate_script = os.path.join(name, activate_cmd)

    if not os.path.exists(activate_script):
        # Fix bash compatibility issues
        activate_cmd = activate_cmd.replace('/', '\\')
        activate_content = ''
        with open(activate_script + '.sh', 'r') as f:
            for line in f.readlines():
                activate_content += line.replace('$', '').replace('{BASH_SOURCE-}', '$0')
    
        # Create fixed bash script
        with open(activate_script, 'w') as f:
            f.write(activate_content)

    subprocess.check_call(["/bin/bash", "-c", "source %s" % activate_script])


    # Install pip and setuptools
    subprocess.check_call(['python', '-m', 'ensurepip'])
    subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools'])

def install_packages(requirements_file):
    # Install packages from the given requirements file
    subprocess.check_call(['pip', 'install', '-r', requirements_file])

def uninstall_package(package):
    subprocess.check_call(['python', '-m', 'pip', 'uninstall', '-y', package])

def list_packages(details=None):
    # List all installed packages
    _ = details
    output = subprocess.check_output(['pip', 'freeze'])
    print(output.decode('utf-8'))

def run_command(command):
    # Run a command in the virtual environment
    subprocess.check_call(command, shell=True)

def deactivate():
    # Exit the virtual environment 
    env_name = os.environ.get('VIRTUAL_ENV')
    if env_name:
        activate_script = os.path.join(env_name, 'bin', 'deactivate')
        subprocess.check_call(['source', activate_script], shell=True)
    else:
        print("Error: No active virtual environment found.")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser('create', help='Create a new virtual environment')
    create_parser.add_argument('name', help='Name of the virtual environment')

    install_parser = subparsers.add_parser('install', help='Install packages in the virtual environment')
    install_parser.add_argument('requirements_file', help='Path to the requirements file')

    list_parser = subparsers.add_parser('list', help='List all the installed packages')
    list_parser.add_argument('--details', '-d', action='store_true',
                             help='Show details beside the package names')


    deactivate_parser = subparsers.add_parser('deactivate', help='Deactivate the virtual environment')


    args = parser.parse_args()

    if args.command == 'create':
        create_environment(args.name)
    elif args.command == 'install':
        install_packages(args.requirements_file)
    elif args.command == 'list':
        list_packages(details=args.details)
    elif args.command == 'deactivate':
        deactivate()

if __name__ == '__main__':
    main()

