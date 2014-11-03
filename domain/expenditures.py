'''
Created on 20 oct. 2014

@author: ToTaL
'''
from copy import deepcopy


class BBoard(object):

    """
        Avizier, folosit pentru adaugare, filtrare, stergere, etc.
        a cheltuielilor.
    """
    
    def __init__(self):
        self.exps = []
        self.undo = []

    def addUndo(self):
        self.undo.append(deepcopy(self.exps))

    def doUndo(self):
        self.exps = self.undo[-1]

        if len(self.undo) > 0:
            self.undo = self.undo[:-1]

    def addExpenditure(self, ap, cat, cost, day):
        """
            Adauga o cheltuiala la avizier.

            Parametrii:
                ap - apartamentul, nr. nat.
                cat - categoria (din cele specificate)
                cost - valoarea cheltuielii, nr. nat.
                day - ziua, nr. nat.
        """
        self.addUndo()

        exp = Expenditure(ap, cat, cost, day, True)
        self.exps.append(exp)

    def getAll(self):
        """
            Returneaza lista cu toate cheltuielile
        """
        return self.exps

    def getApsWithCostHigherThan(self, cost):
        """
            Calculeaza apartamentele cu costul total al cheltuielilor mai mare
            decat parametrul cost.

            Parametrii:
                cost - nr. nat.

            Returneaza:
                Un dictionar care are ca si cheie numarul apartamentului si ca si valoare
                suma totala a cheltuielilor asociate.
        """
        aps = {}
        final = {}

        for e in self.exps:
            if e.getApartment() in aps:
                aps[e.getApartment()] += e.getCost()
            else:
                aps[e.getApartment()] = e.getCost()

        for ap in aps:
            if aps[ap] > cost:
                final[ap] = aps[ap]

        return final

    def getAllInCategory(self, cat):
        """
            Returneaza toate cheltuielile din categoria specificata in parametru.

            Parametrii:
                cat - categorie (din cele specificate)

            Returneaza:
                O lista de dicionare care au categoria specificata.
        """

        final = []

        for e in self.exps:
            if e.getCategory() == cat:
                final.append(e)

        return final

    def getExpendituresBeforeDayAndCostHigherThan(self, day, cost):
        """
            Returneaza toate cheltuielile care au ziua mai mica decat parametrul specificat
            si suma mai mare decat parametrul specificat.

            Parametrii:
                day - ziua, nr. nat.
                cost - suma, nr. nat.

            Returneaza:
                O lista de dicionare care respecta cerintele.
        """

        final = []

        for e in self.exps:
            if e.getDay() < day and e.getCost() > cost:
                final.append(e)

        return final

    def getAllByApartment(self, ap):
        """
            Returneaza toate cheltuielile care apartin unui apartament

            Paratemtrii:
                ap - numarul apartamentului (nr. natural)

            Returneaza:
                O lista de dictionare care respecta cerintele
        """

        final = []

        i = 0

        while i < len(self.exps):
            if self.exps[i].getApartment() == ap:
                tmp = {}
                tmp['exp'] = deepcopy(self.exps[i])
                tmp['id'] = i

                final.append(tmp)

            i = i + 1

        return final

    def removeById(self, id):
        """
            Sterge o cheltuiala dupa numarul ei de ordine.

            Parametrii:
                id - numarul de ordine (nr. nat.)
        """
        self.addUndo()
        self.exps.pop(id)

    def updateExpenditure(self, id, ap, cat, cost, day):
        """
            Modifica o cheltuiala din avizier.

            Parametrii:
                id - numarul de ordine, nr. nat.
                ap - apartamentul, nr. nat.
                cat - categoria (din cele specificate)
                cost - valoarea cheltuielii, nr. nat.
                day - ziua, nr. nat.
        """
        self.addUndo()

        self.exps[id] = Expenditure(ap, cat, cost, day, True)
        

    def removeByAp(self, ap, undo=True):
        """
            Sterge toate cheltuielile asociate unui apartament

            Parametrii:
                ap - numar apartament, nr. nat.
        """
        if undo:
            self.addUndo()

        final = []

        for exp in self.exps:
            if exp.getApartment() != ap:
                final.append(exp)

        b = len(self.exps)
        self.exps = final

        return b - len(final)

    def removeConsecutive(self, start, stop):
        self.addUndo()
        for i in range(start, stop + 1):
            self.removeByAp(i, False)

    def removeByCat(self, cat):
        self.addUndo()

        final = []

        for exp in self.exps:
            if exp.getCategory() != cat:
                final.append(exp)

        self.exps = final

    def getCostByCat(self, cat):
        total = 0

        for exp in self.exps:
            if exp.getCategory() == cat:
                total += exp.getCost()

        return total

    def sortByCat(self, cat):
        tmp = {}

        for exp in self.exps:
            if exp.getCategory() == cat:
                if exp.getApartment() in tmp:
                    tmp[exp.getApartment()] += exp.getCost()
                else:
                    tmp[exp.getApartment()] = exp.getCost()

        aps = []
        costs = []

        for ap in tmp:
            aps.append(ap)
            costs.append(tmp[ap])

        # sorting -- buble sort
        ok = True
        while ok:
            ok = False

            for i in range(len(costs) - 1):
                if costs[i] < costs[i + 1]:
                    # swap
                    x = costs[i + 1]
                    costs[i + 1] = costs[i]
                    costs[i] = x

                    x = aps[i + 1]
                    aps[i + 1] = aps[i]
                    aps[i] = x

                    ok = True

        return [aps, costs]

    def getCostByAp(self, ap):
        total = 0

        for exp in self.exps:
            if exp.getApartment() == ap:
                total += exp.getCost()

        return total

    def filterByNotCat(self, cat):
        final = []

        for exp in self.exps:
            if exp.getCategory() != cat:
                final.append(exp)

        return final

    def fiterByMaxCost(self, maxcost):
        final = []

        for exp in self.exps:
            if exp.getCost() <= maxcost:
                final.append(exp)

        return final


class Expenditure():

    """
        Clasa pentru cheltuieli
    """

    categories = ['apa', 'canal', 'incalzire', 'gaz', 'altele']
    fields = ['ap', 'cost', 'cat', 'day', 'paid']
    
    def __init__(self, ap, cat, cost, day, paid):

        self.exp = {}
        self.exp['ap'] = ap
        self.exp['cost'] = cost
        self.exp['cat'] = cat
        self.exp['day'] = day
        self.exp['paid'] = paid
        

    def getApartment(self):
        return self.exp['ap']

    def getCost(self):
        return self.exp['cost']

    def getCategory(self):
        return self.exp['cat']

    def getDay(self):
        return self.exp['day']
    
    def getPaid(self):
        return self.exp['paid']
    
    def __str__(self):
        return str(self.exp)
    
    def __eq__(self, ot):
        for field in Expenditure.fields:
            if self.exp[field] != ot.exp[field]:
                return False
        
        return True
