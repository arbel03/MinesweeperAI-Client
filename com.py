import urllib 
from json import loads

class Communicator(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def get_result(self, matrix):
        url = 'http://' + self.ip + ':' + str(self.port) +'/?' + str(matrix).replace(' ', '')
        resp = urllib.urlopen(url).read()
        chances = eval('[' + Communicator.__find_between(resp, '[', ']') + ']')
        # print "Is a bomb?", chances[0]
        return chances[0]

    @staticmethod    
    def __find_between(s, first, last):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
