import datetime
import json
import pymongo as pm
from bson.objectid import ObjectId
# Every operations with mongo

### metoda do testowania innych metod
def main():
    print('Proba')
    baza = KacMongo()
    db = baza.get_database('test')
    bazy = baza.show_databases()
    print(bazy)
    colection = baza.get_collection('customers')
    kolekcje = baza.show_collections() # dziala
    print(kolekcje)

    post = {"author": "Mike2",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo","test"],
            "date": str(datetime.datetime.utcnow()),
            "ar": {
                "ra": ["test1","test2"]
                }
            }

    # print(post)

    # baza.insert(post) # dziala

    # data = baza.find_one(dictmatch={"author":"Mike"}) # dziala
    # print(str(data))

    # data = baza.find()#dictmatch={"ar.ra":"test2"}) # dziala
    # for dat in data:
    #     print(str(dat))

    baza.insert(post)
    baza.update({"ar.ra": "test2"},{"author": "Zdzichu23"},True)
    
    data = baza.find()#dictmatch={"ar.ra":"test2"}) # dziala
    for dat in data:
        print(str(dat))

    baza.delete({"ar.ra": "test1"})

    data = baza.find()#dictmatch={"ar.ra":"test2"}) # dziala
    for dat in data:
        print(str(dat))

    fie = baza.show_collection_fields()
    for f in fie:
        print(f)    


    print('Koniec proby')

class KacMongo:
    """Klasa pozwalajaca obslugiwac interakcje pomiedzy kodem a baza danych MongoDB."""

    def __init__(self):
        """Inicjalizuje polaczenie z baza MongoDB"""
        try: self.client = pm.MongoClient('localhost', 27017,connect=False) # connect=False - dla spiders2
        except Exception as e: print('Nie mozna sie polaczyc z serwerem MongoDB, blad: {}'.format(str(e)))

    ### pobierz baze danych
    def get_database(self, nazwabazy):
        """Daje dostep do bazy danych o wybranej nazwie \n
        nazwabazy - nazwa bazy danych w MongoDB \n\n
        Tworzy pole baza w klasie - nie trzeba non stop otrzymywac do niej dostepu, raz wystarczy
        """
        try:
            self.db = self.client[nazwabazy]
            return self.client[nazwabazy]
        except Exception as e:
            print('Nie mozna polaczyc sie z baza danych {} blad: {}'.format(nazwabazy,str(e)))
            return None
        
    ### pokaz wszystkie bazy danych
    def show_databases(self):
        """Pokaz wszystkie bazy na serwerze MongoDB \n
        Zwraca liste stringow"""
        try: return self.client.database_names()
        except Exception as e: print('Nie mozna zobaczyc dostepnych baz na serwerze MongoDB')

    ### usuwa baze danych
    def drop_database(self, nazwabazy):
        """Usun baze danych
        Jesli nie podano nazwy bazy - zostanie usunieta baza przechowywana w klasie"""
        try:
            if nazwabazy != None:
                self.client.drop_database(nazwabazy)
            else:
                self.client.drop_database(self.db.name)
        except Exception as e:
            print(str(e))
        

    ### pobierz kolekcje
    def get_collection(self, nazwakolekcji, nazwabazy=None):
        """Zwraca kolekcje z bazy danych \n
        nazwakolekcji - nazwa kolekcji znajdujacej sie w danej bazie danych \n
        nazwabazy - wybrana baza w ktorej znajduje sie poszukiwana kolekcja"""
        try:
            if nazwabazy == None:
                self.collection = self.db[nazwakolekcji]
                return self.collection
            else:
                self.collection = self.client[nazwabazy][nazwakolekcji]
                return self.collection
        except Exception as e:
            print(str(e))

    ### pokaz wszystkie kolekcje w bazie
    def show_collections(self):
        """Pokaz wszystkie kolekcje w bazie \n
        Zwraca liste stringow"""
        try: return self.db.collection_names()
        except Exception as e: print('Nie mozna zobaczyc dostepnych baz na serwerze MongoDB')

    ### usuwa kolekcje
    def drop_collection(self, nazwakolekcji=None):
        """Usun kolekcje klasy
        Jesli nie podano nazwy kolekcji - zostanie usunieta kolekcja przechowywana w klasie"""
        try:
            if nazwakolekcji != None:
                self.db[nazwakolekcji].drop()
            else:
                self.collection.drop()
        except Exception as e:
            print(str(e))
        
    ### polacz z baza i kolekcja
    def conn_to_db(self,nazwabazy='test',nazwakolekcji='test', nowakolekcja=False):
        mongodb = KacMongo()
        mongodb.get_database(nazwabazy) # 'queue'
        if nowakolekcja:
            mongodb.drop_collection(nazwakolekcji) # 'spider'
        mongodb.get_collection(nazwakolekcji=nazwakolekcji) # 'spider'

        return mongodb

    ### wprowadz dokument
    def insert(self, dictObject):
        """Wprowadz element typu dict do kolekcji
        Jesli chcesz wprowadzic pare obiektow -> wprowadz dictobjects do listy -> przekaz ta liste \n"""
        try:
            if type(dictObject) == list:
                self.collection.insert_many(dictObject)
            else:
                self.collection.insert_one(dictObject)
        except Exception as e:
            print(str(e))

    ### znajdz dokument/y wg id lub porownania
    def find(self, id=None, dictmatch=None):
        """Szukaj obiektu po id albo posiadanych cechach(dictmatch) \n
        Metoda zwraca liste objektow"""
        try:
            listOfObjects = []
            if id != None:
                listOfObjects.append(self.collection.find_one({"_id": ObjectId(id)}))
            elif dictmatch != None:
                [listOfObjects.append(obj) for obj in self.collection.find(dictmatch)]
            else:
                [listOfObjects.append(obj) for obj in self.collection.find()]
            return listOfObjects
        except Exception as e:
            print(str(e))

    ### znajdz najwieksza/najmniejsza wartosc sposrod dokumentow
    def find_extremum(self, sorted_value='test', sort=1 , limit=1):
        """
        sorted_value = podlug jakiej wartosci sortowac \n
        sort -> rosnaco = 1, malejaco = -1 \n
        limit = ile pierwszych dokumentow podlug sortowania \n
        zwaraca liste obiektow
        """
        try:
            listOfObjects = []
            [listOfObjects.append(obj) for obj in self.collection.find().sort([(sorted_value,sort)]).limit(limit)]
            return listOfObjects
        except Exception as e:
            print(str(e))

    ### zmodyfikuj dokument
    def update(self, dictmatch, dictmodify, many=False):
        """Modyfikuje dokuemnt \n
        dictmatch - wzor zawierajacy elementy szukane w dokumentach w postaci slownika \n
        dictmodify - jak/co modyfikowac w znalezionych dokumentach \n
        Metoda nic nie zwraca"""
        try:
            if many == False:
                self.collection.update_one(dictmatch,{"$set": dictmodify},upsert=True)
            else:
                self.collection.update_many(dictmatch,{"$set": dictmodify})
        except Exception as e:
            print(str(e))
        
        
    ### usun dokumenty wg wzoru
    def delete(self, dictmatch):
        """Usuwa dokumenty zawierajace pola i wartosci pasujace do podanego wzoru \n
        Metoda zwraca (w razie powodzenia ilosc usunietych dokumentow"""
        try:
            results = self.collection.delete_many(dictmatch)
            return results.deleted_count()
        except Exception as e:
            print(str(e))

    ### usun powtarzajace sie dokumenty
    def delete_duplicats(self):
        """Usuwa dokumenty ktore powtarzaja sie w kolekcji"""
        for obj in self.collection.find():
            if self.collection.find({"url": obj['url']}).count() > 1:
                self.collection.delete_one({"url": obj['url']})

        
    ### tworzy unikalny index dla kolekcji
    def create_index(self, nameofindex):
        try:
            self.collection.create_index([(nameofindex),pymongo.ASCENDING],unique=True)
        except Exception as e:
            print('Nieudana proba stworzenia unikalnego indexu, blad: {}'.format(str(e)))

    ### kasuje unikalny index dla kolekcji
    def drop_index(self, nameofindex):
        try:
            self.collection.drop_index([(nameofindex),pymongo.ASCENDING],unique=True)
        except Exception as e:
            print('Nieudana proba skasowania unikalnego indexu, blad: {}'.format(str(e)))

    ### Pokaz nazwy pol
    def show_collection_fields(self, nr=None):
        try:
            fields = []
            cursor = self.collection.find()
            if nr != None:
                fields.append(cursor[nr].keys())
                return fields
            else:
                for docum in cursor:
                    print(docum.keys())
                    fields.append(docum.keys())
                return fields
        except Exception as e:
            print(str(e))

# main()