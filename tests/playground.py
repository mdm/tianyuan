def consume(data, count):
    data = data[count:]
    return data
    
def f1(data):
    data = consume(data, 5)
    try:
        data = f2(data)
    except Exception:
        pass
    return data
    
def f2(data):
    data = consume(data, 3)
    raise Exception
    return data
    
test = b'this is a test'

