#from disk_cache import DiskCache
import fileinput as fi
from kac_mongo import KacMongo
from datetime import timedelta
import os

class DiskQueue:
    """Klasa umozliwiajaca tworznie kolejki zadan \n
    Stan zadan:\n
    1 - nie zrobione 
    2 - w trakcie wykonywania
    3 - zakonczone \n
    """


    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, *args, **kwargs):
        self.queue = []
        if os.path.isfile('queue.txt'):
            createFile = open('queue.txt','w')
            createFile.write('Status, Argument \n')
            createFile.close()

    def __call__(self, *args, **kwargs):
        readFile = open('queue.txt','r')
        results = []
        for i in readFile.readlines():
            results.append(i)
        return results

    def push(self, item):
        writeFile = open('queue.txt','a')
        writeFile.writelines('{}, {}'.format('1',str(item)))
        writeFile.close()

    def pop(self):
        result = None
        with fi.FileInput('queue.txt') as filee:            
            for line in filee:
                if line.find('1,') != -1:
                    result = line.split(sep=',')[1]
                    line.replace('1,','2,')
                    break
        return result[:-2]

    def peek(self):
        try:
            with fi.FileInput('queue.txt') as filee:
                for line in filee:
                    if line.find('1,') != -1:
                        result = line.split(sep=',')[1]
                        break
            return result[:-2]
        except Exception as e:
            return None
        
    def complete(self, qargs):
        with fi.FileInput('queue.txt') as filee:
            for line in filee:
                if line.find(gargs) != -1:
                    result = line.split(sep=',')[1]
                    line.replace('2,','3,')
                break

    def complete_queue(self):
        os.remove('queue.txt')

    def test(self):
        appendFile = open('queue.txt','a')
        for i in range(10):
            appendFile.write('1, {} \n'.format(str(i)))
        appendFile.close()


##### stara klasa - testowa
class Queue2:

    def __init__(self, *args, **kwargs):
        l = []
        [l.append(i) for i in range(1,10)]
        self.lista = l

    def __call__(self, *args, **kwargs):
        lista2 = []
        for item in self.lista:
            lista2.append(item)
        return lista2

    def push(self,item):
        self.lista.append(item)

    def pop(self):
        x = self.lista.pop()
        return x

    def peek(self):
        try:
            ob = self.lista.pop()
            self.lista.append(ob)
            if ob:
                return ob
        except Exception as e:
            return None

class Spiders_Queue:
    """
    nazwabazy = 'test', \n
    nazwakolekcji = nazwa wybranej kolekcji
    """

    def __init__(self, *args, **kwargs):
        self.max_depth = kwargs['max_depth']
        self.db = KacMongo()
        self.db.get_database(kwargs['nazwabazy'])
        self.db.get_collection(kwargs['nazwakolekcji'])

    # def __call__(self, *args, **kwargs):
    #     lista2 = []
    #     for item in self.lista:
    #         lista2.append(item)
    #     return lista2

    # def push(self,item):
    #     self.lista.append(item)

    # def pop(self):
    #     x = self.lista.pop()
    #     return x

    def peek(self):
        dl = self.db.find(dictmatch={"downloaded": "0", "depth": {"$lt": str(self.max_depth)}})

        if self.db.find():
            if dl: return True#dl[0]
            else: return False
        else: return True