"""
Frontend module
"""
import os
from time import sleep

from .backend import get_directions, get_transported, get_countries, custom_sort


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
    """
    def print_direction(items: list):
        for c in items[:PRINT_SIZE]:
            route = f"{c[0]:27s}"
            cont = f"{c[-1]['cont']:3d}"
            value = f"{c[-1]['value']:12d}"
            print(f"{route}: {cont} - ${value}")

    separator = '-------------------'
    print('\nThis is a directions report\n')
    print(separator)

    # Directions loop
    options = ['Imports', 'Exports']
    response = print_options(options)
    while response < 0 or response > len(options):
        clear()
        response = print_options(options)
    response = options[response]
    print(f'\n{response} report\n')
    print(separator)
    res_routes = get_directions(response)

    conts = custom_sort(res_routes, 'cont')
    print('Count sorted\n')
    print_direction(conts)

    print(separator)

    print('Value sorted\n')
    values = custom_sort(res_routes, 'value')
    print_direction(values)


def ask_transport():
    """
    Prints transports report
    """
    def print_transport(items):
        for i in items:
            travel = f"{i[0]:5s}"
            cont = f"{i[-1]['cont']:6d}"
            value = f"{i[-1]['value']:14d}"
            print(f"{travel} ({cont}) - ${value}")

    separator = '-------------------'
    print('\nThis is a transports report\n')
    print(separator)
    transported = get_transported()

    print('Count sorted\n')
    conts = custom_sort(transported, 'cont')
    print_transport(conts)

    print(separator)

    print('Value sorted\n')
    values = custom_sort(transported, 'value')
    print_transport(values)


def ask_country():
    """
    Prints country report
    """
    LIM = 0.8
    separator = '-------------------'
    print('\nThis is a countries report\n')
    print(separator)
    count_countries = get_countries()

    result = custom_sort(count_countries, 't_count')

    total_v = sum([r[-1]['t_value'] for r in result])
    total_c = sum([r[-1]['t_count'] for r in result])
    acum_val, acum_cont = 0, 0
    for r in result:
        orig = r[-1]['origin']
        dest = r[-1]['dest']
        t_count = r[-1]['t_count']
        acum_cont += t_count
        t_value = r[-1]['t_value']
        acum_val += t_value
        s_value = round(t_value/total_v, 2)
        p_value = round(acum_val/total_v, 2)
        s_cont = round(t_count/total_c, 2)
        p_cont = round(acum_cont/total_c, 2)

        o = f"Org: {orig['cont']:4d}, ${orig['value']:12d}"
        d = f"Dst: {dest['cont']:4d}, ${dest['value']:12d}"
        msg = f"{r[0]:18s} - {o}, {d}, C: {t_count:4d} - {s_cont:.02f}% :{p_cont:.02f}%, V: {t_value:12d} - {s_value:.02f}%: {p_value:.02f}%"
        print(msg)

        if p_value > LIM:
            break
