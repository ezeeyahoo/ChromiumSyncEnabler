#! /usr/local/bin/python3

import os


def get_keys(con_msg, length):

    while(True):

        key = input(con_msg).strip()

        if key is None:
            continue
        # print(len(key))
        if len(key) != length:
            print("Enter correctly")
            continue

        break
    return key


def custom_user(app_bin):

    user = os.getenv('USER')
    while(True):

        print('App not found at /Applications')
        opt = input('Do you want to install for specific user (y/n) ')

        if opt.lower() in ('n', 'no'):
            return 0

        opt = input('Current user detected as ' + user +
                    ', Do you want to change? [y/N] ').strip()

        if opt.lower() in ['y', 'n', 'yes', 'no', '']:

            if opt.lower() == 'y':
                user = input('Enter User Name: ')
            return(['/User/' + user + '/Applications/Chromium.app/'])

        print('Wrong input, Try Again')
        continue


def generate_new_launcher():

    GAK = ""
    GDCI = ""
    GDCS = ""
    app_name = ['Chromium']
    app_dir = ['/Applications/Chromium.app/']
    app_bin = [app_dir, ['Contents/MacOS/Chromium']]
    renamed_app_bin = [app_bin, '_orig_bin']
    new_launcher = os.path.join(os.getcwd(), *app_name)

    if not os.path.exists(new_launcher):
        print(new_launcher)
        return 0

    if not os.path.exists(os.path.join(*app_dir)):
        app_dir = custom_user(app_bin)

    GAK = get_keys('Enter Google API key: ', 39)

    GDCI = get_keys('Enter Google Default Client ID: ', 72)

    GDCS = get_keys('Enter Google Default Client Secret: ', 24)
    print(os.path.join(''.join(app_bin)))
    if os.path.exists(os.path.join(*app_bin)):

        if not os.path.exists(os.path.join(*renamed_app_bin)):
            try:
                os.rename(os.path.join(*app_bin),
                          os.path.join(*renamed_app_bin))
            except OSError:
                print('Cannot rename, OSError')

        if os.path.exists(os.path.join(*renamed_app_bin)):
            opt = input(
                'Do you want to overwrite previous sync activation(Y/n) '
            ).lower()

            if opt in ('no', 'n'):
                return 0

        with open(new_launcher, 'r') as read_cursor:
            data = read_cursor.read()
            data = data.replace('GAK', GAK)
            data = data.replace('GDCI', GDCI)
            data = data.replace('GDCS', GDCS)

        with open(new_launcher, 'w') as write_cursor:
            write_cursor.write(data)

        # Move new_launcher
        os.rename(new_launcher, os.path.join(app_bin))
        return True
    return -1


if __name__ == '__main__':
    status = generate_new_launcher()

    if not status:
        print('Exit')

    if status == -1:
        print('Original binary missing! Reinstall App or report bug')

    if status:
        print('Sync Activated ')
