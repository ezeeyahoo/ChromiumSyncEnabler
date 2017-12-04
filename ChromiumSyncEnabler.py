"""
GitHub Repo> https://github.com/ezeeyahoo/ChromiumSyncEnabler

Summary: Secured way to enable sync for official/non-official and
stable/non-stable version of Chromium on Mac while keeping APIs safe,
wihtout globally exposing keys.

How to run:-
------------
Check repo for clear instructions.

"""
from __future__ import print_function

from getpass import getpass as input_h

import os
import stat

try:
    if raw_input:
        input = raw_input
except NameError:
    pass


def get_keys(con_msg, length):
    """Acquire Keys and validation

    Args:
        con_msg (string): console message
        length (int): required length of the keys

    Returns:
        key: Google API keys
    """
    while(True):

        key = input_h(prompt=con_msg).strip()

        if key is None:
            continue

        if len(key) != length:
            print("Enter correctly")
            continue

        break
    return key


def custom_install(app_bin):
    """For user specific installation

    Args:
        app_bin (string): absolute path to app binary.

    Returns:
        app_dir: path to app
    """
    user = os.getenv('USER')
    print('App not found at /Applications')

    while(True):
        opt = input('Did you install Chromium for specific user? (y/n) '
                    ).strip()

        if opt.lower() in ('n', 'no'):
            return 0

        if opt.lower() in ('y', 'yes'):
            break

        print('Wrong input, Try Again')
        continue

    opt = input('Current user detected as ' + user +
                ', Do you want to continue [y/N] ').strip()

    if opt.lower() in ['y', 'yes']:
        return(['/Users/' + user + '/Applications/Chromium.app/'])
    return 0


def generate_new_launcher():
    """generate a custom launcher and place it next to app binary

    Returns:
        status: return or exit status
    """
    GAK = ""
    GDCI = ""
    GDCS = ""
    app_name = 'Chromium'
    template_name = 'Chromium_template'
    app_dir = ['/Applications/Chromium.app/']
    bin_rel_path = ['Contents/MacOS/Chromium']
    app_bin = [app_dir, bin_rel_path]
    rename_app_bin = [app_bin, '_orig_bin']
    launcher_format = os.path.join(os.getcwd(), template_name)
    new_launcher = os.path.join(os.getcwd(), *[app_name])

    # Check if not application is installed at root i.e /Applications
    if not os.path.exists(os.path.join(*app_dir)):
        app_dir = custom_install(app_bin)  # Provide custom user

        if app_dir == 0:
            return 0

        app_bin = [app_dir, bin_rel_path]
        rename_app_bin = [app_bin, '_orig_bin']

    renamed_app_bin = os.path.join(
        *[x for sublist in rename_app_bin[0] for x in sublist]
    ) + rename_app_bin[1]

    if os.path.exists(renamed_app_bin):
        opt = input(
            'Do you want to overwrite previous sync activation(Y/n) '
        ).lower()

        if opt in ('no', 'n'):
            return 0

    # Enter required keys
    GAK = get_keys('Enter Google API key: ', 39)

    GDCI = get_keys('Enter Google Default Client ID: ', 72)

    GDCS = get_keys('Enter Google Default Client Secret: ', 24)

    app_bin = os.path.join(*[x for sublist in app_bin for x in sublist])

    # Check if original binary exists
    if os.path.exists(app_bin):

        if not os.path.exists(renamed_app_bin):
            try:
                os.rename(app_bin, renamed_app_bin)
            except IOError:
                print('Cannot rename, OSError')
                return None
        # Preparing template
        with open(launcher_format, 'r') as read_cursor:
            data = read_cursor.read()
            data = data.replace('GAK', GAK)
            data = data.replace('GDCI', GDCI)
            data = data.replace('GDCS', GDCS)
            data = data.replace(
                'INSTALL_PATH', os.path.dirname(app_bin))

        with open(new_launcher, 'w') as write_cursor:
            write_cursor.write(data)

        os.chmod(new_launcher, stat.S_IRWXU)

        if 'User' not in app_bin:
            os.chmod(new_launcher, stat.S_IRWXU | stat.S_IXGRP | stat.S_IXOTH)

        # Move new_launcher
        os.rename(new_launcher, app_bin)
        return True
    return -1


if __name__ == '__main__':

    print('''
    NOTE:-
    1) If app is installed both User level and system level, only system level\
 is activated

    2) If you move Chromium.app from /Applications to $HOME/Applications or \
vice versa. Re-run for re-activation!
        ''')

    status = generate_new_launcher()

    if status is None:
        print('Close App and retry')
        exit(1)

    if not status:
        print('Exit')
        exit(0)

    if status == -1:
        print('Original binary missing! Reinstall App or report bug')
        exit(1)

    if status:
        print('Sync Activated ')
