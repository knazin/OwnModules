import sqlite3

def ConnectToDatabase(DbName):
    try:
        global conn 
        global c
        DbName += '.db'
        conn = sqlite3.connect(DbName) # jesli nie istnieje to tworzy
        c = conn.cursor() # cursor 
    except Exception as e:
        print('Polaczenie sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Globalne zmienne zostaly utworzone')


def DisConnectWithDatabase():
    try:
        c.close()
        conn.close()
    except Exception as e:
        print('Zamkniecie polaczenia sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Polaczenie z baza zostalo zamkniete')    

    
def CreateTable(TableName, Columns):
    try:
        col = ", ".join(Columns)
        c.execute('CREATE TABLE IF NOT EXISTS {0}({1})'.format(TableName,col))
    except Exception as e:
        print('Stworzenie tabeli sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Tabela zostala stworzona albo juz istnieje')


def DeleteTable(TableName):
    try:
        c.execute('DROP TABLE {0}'.format(TableName))
    except Exception as e:
        print('Usuniecie tabeli sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Tabela zostala usunieta')
    

def Create(InsertInto, ValuesNames, Data):
    try:
        insert = 'INSERT INTO ' + InsertInto

        if ValuesNames != '' and type(ValuesNames) == type([]):
            values = '(' + ', '.join(ValuesNames) + ')'
        elif ValuesNames != '':
            values = '({0})'.format(ValuesNames)
        else:
            values = ''

        if Data != '' and type(Data) == type([]):
            data = 'VALUES('
            for d in Data:
                if type(d) == type(''):
                    data += "'{0}', ".format(d) 
                else:
                    data = data + "{0}, ".format(d)
            data = data[:len(data)-2] + ')'
        elif Data != '':
            data = 'VALUES({0})'.format(Data)
        else:
            data = ''

        print("{0}{1} {2}".format(insert,values,data))

        c.execute("{0}{1} {2}".format(insert,values,data))
        conn.commit() # jesli cos zmieniasz to musisz to zawsze potwierdzic
    except Exception as e:
        print('Dodanie wiersza sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Wiersz zostal dodany')
    

def Read(SELECT, FROM, WHERE):
    try:
        if type(SELECT) == type([]):
            select = 'SELECT ' + ", ".join(SELECT)
        else:
            select = 'SELECT ' + SELECT

        From = 'FROM ' + FROM

        if WHERE != '':
            where = 'WHERE ' + WHERE
        else:
            where = ''
            
        c.execute("{0} {1} {2}".format(select,From,where))
        return c.fetchall()
    except Exception as e:
        print('Odczytanie danych sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Przekazano dane tabeli')
    

def Update(UPDATE, SET, WHERE):
    try:
        update = 'UPDATE ' + UPDATE
        Set = 'SET ' + SET

        if WHERE != '':
            where = 'WHERE ' + WHERE
        else:
            where = ''

        print("{0} {1} {2}".format(update,Set,where))
        c.execute("{0} {1} {2}".format(update,Set,where))
        conn.commit()
    except Exception as e:
        print('Modyfikacja danych sie nie udala: {0}'.format(str(e)))
        return str(e)
    else:
        print('Zmodyfikowano dane tabeli')
    

def Delete(FROM, WHERE):
    try:
        From = 'FROM ' + FROM
        if WHERE != '':
            where = 'WHERE ' + WHERE
        else:
            where = ''

        c.execute("DELETE {0} {1}".format(From,where))
        conn.commit()
    except Exception as e:
        print('Usuwanie danych sie nie udalo: {0}'.format(str(e)))
        return str(e)
    else:
        print('Usunieto dane tabeli')
    