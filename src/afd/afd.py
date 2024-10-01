class SQLInjectionAFD:
    def __init__(self):
        
        self.states = {
            0: {'found': False},
            1: {'found': False},
            2: {'found': False},
            3: {'found': True},  
            4: {'found': False},
            5: {'found': True},  
            6: {'found': False},
            7: {'found': True},  
            8: {'found': True},  
            9: {'found': True},  
            10: {'found': False},
            11: {'found': True}, 
            12: {'found': True}, 
            13: {'found': True}, 
            14: {'found': True}, 
            15: {'found': True}, 
            16: {'found': True}, 
            17: {'found': True}, 
        }

        self.transitions = {
            0: {"'": 1, '"': 1, "O": 2, "U": 4, "D": 6, "-": 8, "/": 10, ";": 16, "#": 17}, 
            1: {" ": 2},  
            2: {"O": 2, "R": 3, "1": 3, "=": 3}, 
            3: {},  
            4: {"N": 4, "I": 4, "O": 5},  
            5: {},  
            6: {"R": 6, "O": 7, "P": 7},  
            7: {},  
            8: {"R": 9},  
            9: {},  
            10: {"*": 11}, 
            11: {},
            12: {" ": 12},
            13: {" ": 13},  
            14: {"A": 15},  
            15: {},
            16: {},  
            17: {},  
        }

    def process(self, text):
        current_state = 0
        for char in text:
            if char in self.transitions[current_state]:
                current_state = self.transitions[current_state][char]
            else:
                current_state = 0  

            if self.states[current_state]['found']:
                return True  
        return False


