import urllib 
from json import loads

class Communicator(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    
    def get_result(self, matrix):
        url = 'http://' + self.ip + ':' + str(self.port) +'/?' + str(matrix).replace(' ', '')        
        resp = urllib.urlopen(url).read()
        print resp
        chances = eval('[' + Communicator.__find_between(resp, '[', ']') + ']')

        if chances[0] > 0.7:
            return 2
        elif chances[0] < 0.2:
            return 1
        return None

    @staticmethod    
    def __find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
