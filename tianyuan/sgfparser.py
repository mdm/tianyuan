class TokenIterator:
    def __init__(self, filename):
        f = open(filename, 'rb')
        self.bytes = iter(f.read())
        f.close()
        self.token = ''
        
    def __iter__(self):
        return self
        
    def __next__(self):
        try:
            byte = self.bytes.next()
        except StopIteration:
            if(self.token):
                last_token = self.token
                self.token = ''
                return last_token
            else:
                raise StopIteration
                
