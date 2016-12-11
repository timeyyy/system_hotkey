from system_hotkey import SystemHotkey, \
                          SystemRegisterError, \
                          UnregisterError, \
                          InvalidKeyError

def test_errors_raised_in_main():
    hk = SystemHotkey()
    key = ('5',)
    cb = lambda e: print('hi')

    hk.register(key, callback=cb)
    try:
        hk.register(key, callback=cb)
    except SystemRegisterError:
        pass
    else:
        raise Exception('fail')

    hk.unregister(key)
    try:
        hk.unregister(key)
    except UnregisterError:
        pass
    else:
        raise Exception('fail')

    bad_key = ('badkey ..',)
    try:
        hk.register(bad_key, callback=cb)
    except InvalidKeyError:
        pass
    else:
        raise Exception('fail')

    try:
        hk.unregister(bad_key)
    except:
        pass
    else:
        raise Exception('fail')

    # input() # Hold program open until you press enter

test_errors_raised_in_main()
