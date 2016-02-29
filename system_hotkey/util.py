'''
    system_hotkey.util

    general utilites..
'''

def unique_int(values):
    '''
    returns the first lowest integer
    that is not in the sequence passed in

    if a list looks like 3,6
    of the first call will return 1, and then 2
    and then 4 etc
    '''
    last = 0
    for num in values:
        if last not in values:
            break
        else:
            last += 1
    return last
