'''
Created on 20 oct. 2014

@author: ToTaL
'''

import unittest
from domain.expenditures import BBoard, Expenditure



class Tests(unittest.TestCase):
    
    def setUp(self):
        self.board = BBoard()
        
        self.board.addExpenditure(1, 'gaz', 15, 4)
        self.board.addExpenditure(1, 'apa', 18, 4)
        
        self.board.addExpenditure(2, 'apa', 1, 5)
        self.board.addExpenditure(2, 'canal', 9, 8)
        
        self.exps = self.board.getAll()

    def testGetApsWithCostHigherThan(self):
        self.assertEqual(self.board.getApsWithCostHigherThan(16), { 1: 33 })
    
    def testGetAllInCategory(self):
        exps = self.exps
        self.assertEqual(self.board.getAllInCategory('apa'), [exps[1], exps[2]])

    def testGetExpendituresBeforeDayAndCostHigherThan(self):
        exps = self.exps
        self.assertEqual(self.board.getExpendituresBeforeDayAndCostHigherThan(5, 10), [exps[0], exps[1]])
    
    def testUndo(self):
        exps = self.exps
        
        self.board.doUndo()
        self.assertEqual(self.board.getAll(), exps[:-1])
        
    def testGetAllByApartment(self):
        exps = self.exps
        self.assertEqual(self.board.getAllByApartment(1), [{'exp':exps[0], 'id':0}, {'exp':exps[1], 'id':1}])
    
    def testUpdateExpenditure(self):
        exps = self.exps
        
        self.board.updateExpenditure(1, 1, 'incalzire', 28, 8)

        ex = Expenditure(1, 'incalzire', 28, 8, True)
        exps[1] = ex
        self.assertEqual(self.board.getAll(), exps)


    def testRemoveByAp(self):
        self.board.removeByAp(2)

        exps = [Expenditure(1, 'gaz', 15, 4, True), Expenditure(1, 'apa', 18, 4, True)]
        
        self.assertEqual(self.board.getAll(), exps)
        
    
        
        
        
        