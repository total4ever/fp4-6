'''
Created on 17 oct. 2014

@author: ToTaL
'''

class tableGenerator:

    headers = []
    rows = []
    row = []
    
    maxLen = 0
    
    def __init__(self):
        self.headers = []
        self.rows = []
        self.row = []
    
    def pushHeader(self, title):
        title = str(title)
        self.headers.append(title)
        self.updateMax(title)
        
    def pushItem(self, title):
        title = str(title)
        self.row.append(title)
        self.updateMax(title)
    
    def pushRow(self):
        self.rows.append(self.row)
        self.row = []
        
    def updateMax(self, title):
        if len(title) > self.maxLen:
            self.maxLen = len(title)
    
    def render(self):
        self.maxLen += 2
        self.print_separator()
        
        for item in self.headers:
            self.print_item(item)
            
        print('|', sep='')
        
        self.print_separator()
        
        for row in self.rows:
            for item in row:
                self.print_item(item)
            print('|', sep='')
        
        self.print_separator()

        
    def print_item(self, title):
        print('|', title.center(self.maxLen) , sep='', end='')
        
    
    def print_separator(self):
        for i in range(self.maxLen * len(self.headers) + len(self.headers) + 1):
            if i % (self.maxLen + 1) == 0:
                print('+', sep='', end='')
            else:
                print('-', sep='', end='')
    
        print()
    
        