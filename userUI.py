'''
Created on 20 oct. 2014

@author: ToTaL
'''
from expenditures import BBoard, Expenditure
from tableGenerator import tableGenerator

def printMenu():
    
    print("""
1. Adauga cheltuiala
2. Afiseaza apartamentele cu costul mai mare de
3. Afiseaza cheltuielile dinainte de o zi si cu suma mai mare de
4. Modifica cheltuiala
5. Sterge toate cheltuielile asociate unui apartament
6. Sterge cheltuieli de la ap consecutive
7. Sterge toate cheltuielile dintr-o categorie
8. Suma totala pentru un tip de cheltuiala
9. Suma totala pentru un apartament
10. Apartamentele sortate dupa un tip de cheltuiala
11. Filtreaza dupa tip cheltuiala
12. Filtreaza dupa costul maxim

u. Undo
x. Exit
""")
    

def readInt(msg, err_msg):
    """
        Citeste un numar intreg, in caz ca utilizatorul
        introduce o valoare gresita, este rugat sa introduca
        din nou.
        
        Parametrii:
            msg - mesajul care e afisat inainte sa introduca
            err_msg - mesajul de eroare in cazul in care
                      valoarea nu este acceptata
        
        Returneaza: valoarea introdusa de utilizator
    """
    val = 0
    parsed = False
    while not parsed:
        try:
            val = int(input(msg))
            parsed = True
        except ValueError:
            print(err_msg)
    
    return val


def readCategory(msg, err_msg, cats):
    """
        Citeste o valoarea, care trebuie sa fie intr-o lista
        introduce o valoare gresita, este rugat sa introduca
        din nou.
        
        Parametrii:
            msg - mesajul care e afisat inainte sa introduca, string
            err_msg - mesajul de eroare in cazul in care
                      valoarea nu este acceptata, string
            cats - lista de valori permise
            
        Returneaza: valoarea introdusa de utilizator
    """
    
    while True:
        val = input(msg)
        
        if val not in cats:
            print(err_msg)
        else:
            return val

def readCommand():
    return input("Comanda >: ")


def startUI():
    board = BBoard()
    categories = Expenditure.categories
    
    board.addExpenditure(1, 'gaz', 15, 4)
    board.addExpenditure(1, 'apa', 18, 4)
    
    board.addExpenditure(2, 'apa', 1, 5)
    board.addExpenditure(2, 'canal', 9, 8)
        
    while True:
        printMenu()
        cmd = readCommand()
        
        if cmd == '1': # Adaugare cheltuiala
            ap = readInt('Apartament: ', 'Apartamentul trebuie sa fie numar natural.')
            cat = readCategory('Categorie: ', 'Categorie invalida.', categories)
            cost = readInt('Suma: ', 'Suma trebuie sa fie numar natural.')
            day = readInt('Ziua: ', 'Ziua trebuie sa fie numar natural.')
            
            board.addExpenditure(ap, cat, cost, day)
            print('Cheltuiala a fost adaugata.')
        
        if cmd == '2': # Apartamentele cu total mai mare decat o suma
            cost = readInt('Suma: ', 'Suma trebuie sa fie numar natural.')
            l = board.getApsWithCostHigherThan(cost)
            
            table = tableGenerator()
            table.pushHeader('Apartament')
            table.pushHeader('Suma')
            
            for item in l:
                table.pushItem(item)
                table.pushItem(l[item])
                table.pushRow()
            
            table.render()
            
        if cmd == '3': # Cheltuieli cu suma mai mare de, si ziua inainte de
            cost = readInt('Suma: ', 'Suma trebuie sa fie numar natural.')
            day = readInt('Ziua: ', 'Ziua trebuie sa fie numar natural.')
            
            table = tableGenerator()
            table.pushHeader('Apartament')
            table.pushHeader('Categorie')
            table.pushHeader('Suma')
            table.pushHeader('Zi')
            table.pushHeader('Platit')
            
            l = board.getExpendituresBeforeDayAndCostHigherThan(day, cost)
            
            for exp in l:
                table.pushItem(exp.getApartment())
                table.pushItem(exp.getCategory())
                table.pushItem(exp.getCost())
                table.pushItem(exp.getDay())
                table.pushItem(exp.getPaid())
                
                table.pushRow()
                
            table.render()
        
        if cmd == '4': # Modifica cheltuiala
            ap = readInt('Apartament: ', 'Apartamentul trebuie sa fie numar natural.')
            
            table = tableGenerator()
            table.pushHeader('ID')
            table.pushHeader('Apartament')
            table.pushHeader('Categorie')
            table.pushHeader('Suma')
            table.pushHeader('Zi')
            
            l = board.getAllByApartment(ap)
            
            for item in l:
                exp = item['exp']
                table.pushItem(item['id'])
                table.pushItem(exp.getApartment())
                table.pushItem(exp.getCategory())
                table.pushItem(exp.getCost())
                table.pushItem(exp.getDay())
                
                table.pushRow()
                
            table.render()
            
            print("Introduceti ID pentru modificare: ")
            id = readInt('ID (-1 pt iesire): ', 'ID-ul trebuie sa fie numar natural.')
            if id != -1:
                
                ap = readInt('Apartament: ', 'Apartamentul trebuie sa fie numar natural.')
                cat = readCategory('Categorie: ', 'Categorie invalida.', categories)
                cost = readInt('Suma: ', 'Suma trebuie sa fie numar natural.')
                day = readInt('Ziua: ', 'Ziua trebuie sa fie numar natural.')
                
                board.updateExpenditure(id, ap, cat, cost, day)
                print('Cheltuiala a fost modificata.')
            
        if cmd == '5': # Sterge cheltuielile asociate unui apartament
            ap = readInt('Apartament: ', 'Apartamentul trebuie sa fie numar natural.')
            
            c = board.removeByAp(ap)
            
            print(c,"cheltuieli au fost sterse.")
        
        if cmd == '6': # Sterge cheltuieli de la ap consecutive
            start = readInt('Apartament inceput: ', 'Apartamentul trebuie sa fie numar natural.')
            stop = readInt('Apartament sfarsit: ', 'Apartamentul trebuie sa fie numar natural.')
            
            board.removeConsecutive(start, stop)
        
        if cmd == '7': # Sterge toate cheltuielile dintr-o categorie
            cat = readCategory('Categorie: ', 'Categorie invalida.', categories)
            
            board.removeByCat(cat)
        
        if cmd == '8': # Suma totala pentru un tip de cheltuiala
            cat = readCategory('Categorie: ', 'Categorie invalida.', categories)
            
            print("Suma totala este: ", board.getCostByCat(cat))
        
        if cmd == '9': # Suma totala pentru un apartament
            ap = readInt('Apartament: ', 'Apartamentul trebuie sa fie numar natural.')
            
            print("Suma totala este: ", board.getCostByAp(ap))
        
        if cmd == '10': # Apartamentele sortate dupa un tip de cheltuiala
            cat = readCategory('Categorie: ', 'Categorie invalida.', categories)
            
            aps, costs = board.sortByCat(cat)
            
            table = tableGenerator()
            table.pushHeader('Apartament')
            table.pushHeader('Total (' + cat + ')')
            
            for i in range(len(aps)):
                
                table.pushItem(aps[i])
                table.pushItem(costs[i])
                table.pushRow()
                
            table.render()
            
        if cmd == '11': # Filtru dupa categorie
            cat = readCategory('Categorie: ', 'Categorie invalida.', categories)
            
            l = board.filterByCat(cat)
            
            table = tableGenerator()
            table.pushHeader('Apartament')
            table.pushHeader('Categorie')
            table.pushHeader('Suma')
            table.pushHeader('Zi')
            table.pushHeader('Platit')
            
            for exp in l:
                table.pushItem(exp.getApartment())
                table.pushItem(exp.getCategory())
                table.pushItem(exp.getCost())
                table.pushItem(exp.getDay())
                table.pushItem(exp.getPaid())
                table.pushRow()
            
            table.render()
        
        if cmd == '12': # Filtru dupa cost maxim, adica cheltuieli cu costul mai mic de
                cost = readInt('Suma: ', 'Suma trebuie sa fie numar natural.')
                
                l = board.fiterByMaxCost(cost)
                
                table = tableGenerator()
                table.pushHeader('Apartament')
                table.pushHeader('Categorie')
                table.pushHeader('Suma')
                table.pushHeader('Zi')
                table.pushHeader('Platit')
                
                for exp in l:
                    table.pushItem(exp.getApartment())
                    table.pushItem(exp.getCategory())
                    table.pushItem(exp.getCost())
                    table.pushItem(exp.getDay())
                    table.pushItem(exp.getPaid())
                    table.pushRow()
                
                table.render()
                
            
        if cmd == 'u': # Undo
            board.doUndo()
            print("Undo OK!") 
        if cmd == 'x':
            break
        
startUI()
        