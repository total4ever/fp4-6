'''
Created on 20 oct. 2014

@author: ToTaL
'''

import unittest
from expenditures import BBoard
from copy import deepcopy



class Tests(unittest.TestCase):
    
    def testAddExpenditure(self):
        
        board = BBoard()
        board.addExpenditure(1, 'gaz', 15, 4)
        board.addExpenditure(1, 'apa', 18, 4)
        
        board.addExpenditure(2, 'apa', 1, 5)
        board.addExpenditure(2, 'canal', 9, 8)
        
        exps = board.getAll()
        self.assertEqual(len(exps), 4)
        
    
        self.assertEqual(board.getApsWithCostHigherThan(16), { 1: 33 })
        self.assertEqual(board.getAllInCategory('apa'), [exps[1], exps[2]])
        self.assertEqual(board.getExpendituresBeforeDayAndCostHigherThan(5, 10), [exps[0], exps[1]])
        
        board.doUndo()
        self.assertEqual(board.getAll(), exps[:-1])
        
        exps = exps[:-1]
        
        tmp = deepcopy(exps)
        
        tmp[0]['id'] = 0
        tmp[1]['id'] = 1
        self.assertEqual(board.getAllByApartment(1), [tmp[0], tmp[1]])
        
        board.updateExpenditure(1, 1, 'incalzire', 28, 8)
        
        exps[1]['ap'] = 1
        exps[1]['cat'] = 'incalzire'
        exps[1]['cost'] = 28
        exps[1]['day'] = 8
        
        self.assertEqual(board.getAll(), exps)
        
        
        board.removeByAp(2)
        exps = [{'cat': 'gaz', 'ap': 1, 'cost': 15, 'day': 4}, {'cat': 'incalzire', 'ap': 1, 'cost': 28, 'day': 8}]
        
        self.assertEqual(board.getAll(), exps)
        
        
        
        