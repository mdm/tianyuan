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
    
test1 = b'this is a test'

class c1:
    def __init__(self):
        self.value = None
    def m1(self, value):
        self.value = value
        
class c2:
    def m2(self, other):
        other.m1('tada!!')

test2 = c1()
