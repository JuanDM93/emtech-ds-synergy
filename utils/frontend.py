"""
Frontend module
"""
import os
from time import sleep

from .backend import directions, transported, countries


# LOCALS
SLEEPING = 0.4
PRINT_SIZE = 10
ADMINS = [['admin', 'pass'], ]

PROCESSES = ['directions', 'transports', 'countries']
EXIT_CMDS = ['return', 'logout', 'exit']


#################
#   Interface   #
#################


def clear():
    """
    Clears screen
    """
    os.system('clear')


# Login
def login(limit: int = 3):
    """
    auth starter function
    """
    def ask() -> tuple:
        """
        returns: user inputs (user, password)
        """
        user = input('Input username: ')
        password = input('Password: ')
        return (user, password)

    def print_login(limit=-1):
        """
        prints login result
        """
        if limit >= 0:
            print(f'Login failed... : {limit}\n')
        else:
            print('Login succesful!\n')
        sleep(SLEEPING)
        clear()

    while limit > 0:
        (user, password) = ask()
        for admin in ADMINS:
            if admin[0] == user and admin[-1] == password:
                print_login()
                # Start interface service
                interface()
        limit -= 1
        print_login(limit)

    # Failed logout
    print('... bye')


# Main
def interface():
    """
    Prints report options
    """
    while True:
        separator = '++++++++++'
        print(separator)
        print('\nHey, what would you like to do?\n')
        response = print_options(PROCESSES)

        # Process
        if response >= 0:
            print(separator)
            print(f'\nINFO: Running "{PROCESSES[response]}" process\n')
            sleep(SLEEPING)
            report(response)
            clear()


def print_options(options: list) -> int:
    """
    options: ids list
    returns: response id
    """
    separator = '**********'
    print(separator)
    print('\nSelect option:\n')

    size = len(options)
    options = [(i, options[i]) for i in range(size)]
    for o in options:
        print(f'{o[0]}: {o[-1]}')
    print()
    for e in EXIT_CMDS:
        print(f'"{e}"')

    answer = input('\nanswer: ')
    if exit_status(answer):
        return len(options) + 1
    print(separator)

    try:
        answer = int(answer)
        if answer < 0 or answer > size - 1:
            print(f'\nWARNING: "{answer}" is not a valid option\n')
            answer = -1
    except ValueError:
        print(f'\nERROR: Input unavailable "{answer}"\n')
        answer = -1

    print(separator)
    sleep(SLEEPING)
    clear()
    return answer


def exit_status(answer: str) -> bool:
    """
    Checks exit command behaviour
    """
    if answer == EXIT_CMDS[-1]:
        exit()
    else:
        if answer == EXIT_CMDS[1]:
            clear()
            login()
            return True
        if answer == EXIT_CMDS[0]:
            clear()
            interface()
        return False


#################
#    Reports    #
#################


def report(process_id: int = 0):
    """
    reports logic
    """
    def wait_input():
        """
        Return
        """
        input('\nInput anything to return\n')
        clear()

    print('\nReading db...\n')
    if process_id == 0:
        print('\n- Imports and Exports -\n')
        ask_direction()
        wait_input()
    elif process_id == 1:
        print('\n- Transport Mode -\n')
        ask_transport()
        wait_input()
    elif process_id == 2:
        print('\n- Country -\n')
        ask_country()
        wait_input()
    else:
        print('\n- Unknown -\n')
        wait_input()


def ask_direction():
    """
    Prints directions report
    # options = ['Imports', 'Exports']
    """
    def print_direction(results):
        totals = [int(r['total_value']) for r in results]
        print(f'{len(results):5d}: ${sum(totals):14d}.00')

    separator = '-------------------'
    print('\nThis is a directions report\n')
    print(separator)

    exports, imports = directions()

    print('Exports')
    print_direction(exports)

    print(separator)

    print('Imports')
    print_direction(imports)


def ask_transport():
    """
    Prints transports report
    """
    separator = '-------------------'
    print('\nThis is a transports report\n')
    print(separator)

    results = transported()

    toprint = []
    for r in results:
        result = sum(int(val['total_value']) for val in results[r])
        toprint.append([r, len(results[r]), result])
    toprint.sort(key=lambda p: p[-1], reverse=True)

    for t in toprint:
        print(f'{t[0]:5s} - {t[1]:5d}: ${t[-1]:14d}.00')


def ask_country():
    """
    Prints country report
    """
    def print_route(routes):
        toprint = []
        for country in routes:
            c_total = [int(r['total_value']) for r in routes[country]]
            toprint.append([country, sum(c_total)])
        toprint.sort(key=lambda i: i[-1], reverse=True)
        for p in toprint:
            print(f'{p[0]:20s} ${p[-1]:12d}.00')

    separator = '-------------------'
    print('\nThis is a countries report\n')
    print(separator)

    origin, destin = countries()

    print(f'Origins:\n')
    print_route(origin)

    print(separator)

    print(f'Destinations:\n')
    print_route(destin)
