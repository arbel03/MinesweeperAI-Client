import urllib 
from json import loads

class Communicator(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def is_bomb(self, matrix):

        url = 'http://' + self.ip + ':' + str(self.port) +'/?' + str(matrix).replace(' ', '')        
        resp = urllib.urlopen(url).read()
        chances = eval('[' + Communicator.__find_between(resp, '[', ']') + ']')

        if chances[0] > chances[1]:
            return True
        return False 

    @staticmethod    
    def __find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
