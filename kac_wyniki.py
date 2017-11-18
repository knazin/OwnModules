import sys
import time
from kac_mongo import KacMongo

class Wyniki:

    def __init__(self, *args, wynikczego='test', **kwargs):
        self.db = KacMongo()
        self.db.get_collection(nazwakolekcji=wynikczego, nazwabazy='wyniki')

        if kwargs:
            wynik = {"czas": time.asctime()}
            listkeys = list(kwargs.keys())

            for i in range(0,len(kwargs)):
                wynik[listkeys[i]] = kwargs[listkeys[i]]

            # wyswietl wyniki
            for w in wynik:
                print(w,':',wynik[w])

            self.db.insert(dictObject=wynik)

    def wpisz(self, *args, **kwargs):
        if kwargs:
            wynik = {"czas": time.asctime()}
            listkeys = list(kwargs.keys())

            for i in range(0,len(kwargs)):
                wynik[listkeys[i]] = kwargs[listkeys[i]]

            # wyswietl wyniki
            for w in wynik:
                print(w,':',wynik[w])

            self.db.insert(dictObject=wynik)

# if __name__ == "__main__":

    #w = Wyniki(wynikczego='spiders',test='siemano', test2='dowidzenia')
    #w = Wyniki(wynikczego='spiders')
    #w.wpisz(test='siemano', test2='dowidzenia')