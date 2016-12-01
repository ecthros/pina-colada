def base_test():
    pass

def padding_tests():
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[0:-ord(s[-1])]
    print repr(pad("test"))
    print pad("")
    print pad("123456789876")
    print pad("a")
    pass
padding_tests()
