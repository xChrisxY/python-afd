class SQLInjectionAFD:
      
    def __init__(self):
          
        self.final_states = {21, 29, 40, 45, 76, 93, 109}

        self.transitions = {
            (0, "'"): 1,
            (1, " "): 2,
            (2, " "): 2,
            (2, "o"): 3,
            (3, "r"): 4,
            (4, " "): 5,
            (5, " "): 5,
            (5, "'"): 6,
            (6, "[a-z]"): 6,
            (6, "'"): 46,
            (6, "1"): 7,
            (7, "'"): 8,
            (8, "="): 9,
            (9, "'"): 10,
            (10, "1"): 37,
            (37, " "): 38,
            (37, "-"): 38, # prueba 1 
            (38, " "): 38,
            (38, "-"): 39,
            (39, " "): 39, # prueba 2
            (39, "-"): 40,
            (0, "o"): 3,
            (0, "a"): 22,
            (22, "d"): 23,
            (23, "m"): 24,
            (24, "i"): 25,
            (25, "n"): 26,
            (26, "'"): 27,
            (27, "-"): 28,
            (28, "-"): 29,
            (27, " "): 30,
            #(27, " "): 5,
            (5, "1"): 11,
            (11, "="): 10,
            (30, " "): 30,
            (30, "a"): 31,
            (31, "n"): 32,
            (32, "d"): 33,
            (33, " "): 34,
            (34, " "): 34,
            (34, "[1-9]"): 35,
            (35, "="): 36,
            (36, "[1-9]"): 37,
            (46, "="): 47,
            (47, " "): 47,
            (47, "'"): 48,
            (47, "[1-9]"): 35,
            (48, "[a-z]"): 48,
            (48, "'"): 37,
            (4, "d"): 67,
            (67, "e"): 68,
            (68, "r"): 69,
            (69, " "): 70,
            (70, " "): 70,
            (70, "b"): 71,
            (71, "y"): 72,
            (72, " "): 73,
            (73, " "): 73,
            (73, "[1-9]"): 74,
            (74, "[1-9]"): 74,
            (74, " "): 75, # poner o no poner espacio#
            (74, "-"): 75,
            (75, "-"): 76,
            (5, "d"): 12,
            (12, "e"): 49,
            (49, "l"): 50,
            (50, "e"): 51,
            (51, "t"): 52,
            (52, "e"): 53,
            (53, " "): 54,
            (54, " "): 54,
            (54, "f"): 55,
            (55, "r"): 56,
            (56, "o"): 57,
            (57, "m"): 58,
            (58, " "): 59,
            (59, " "): 59,
            (59, "[a-z]"): 60,
            (60, "[a-z]"): 60,
            (60, " "): 61,
            (61, " "): 61,
            (61, "w"): 62,
            (62, "h"): 63,
            (63, "e"): 64,
            (64, "r"): 65,
            (65, "e"): 66,
            (66, " "): 47,
            (12, "r"): 13,
            (13, "o"): 14,
            (14, "p"): 15,
            (15, " "): 16,
            (16, " "): 16,
            (16, "t"): 17,
            (17, "a"): 18,
            (18, "b"): 19,
            (19, "l"): 20,
            (20, "e"): 21,
            (21, " "): 41,
            (41, " "): 41,
            (41, "[a-z]"): 42,
            (42, "[a-z]"): 42,
            (42, " "): 43,
            (43, " "): 43,
            (43, "-"): 44,
            (44, "-"): 45,
            (2, "u"): 77,
            (77, "n"): 78,
            (78, "i"): 79,
            (79, "o"): 80,
            (80, "n"): 81,
            (81, " "): 82,
            (82, " "): 82,
            (82, "s"): 83,
            (83, "e"): 84,
            (84, "l"): 85,
            (85, "e"): 86,
            (86, "c"): 87,
            (87, "t"): 88,
            (88, " "): 89,
            (89, " "): 89,
            (89, "[1-9]"): 91,
            (89, "[a-z]"): 90,
            (90, "[a-z],-"): 90,
            (90, "("): 94,
            (90, " "): 91,
            (90, "-"): 91, # de prueba # 
            (94, ")"): 91,
            (91, " "): 91,
            (91, "-"): 92,
            (92, "-"): 93,
            (92, " "): 92, # de prueba #
            (2, "a"): 95,
            (95, "n"): 96,
            (96, "d"): 97,
            (97, " "): 98,
            (98, " "): 98,
            (98, "s"): 99,
            (99, "l"): 100,
            (100, "e"): 101,
            (101, "e"): 102,
            (102, "p"): 103,
            (103, "("): 104,
            (104, "[0-9]"): 105,
            (105, "[0-9]"): 105,    
            (105, ")"): 106,
            (106, " "): 107,
            (106, "-"): 107,
            (107, " "): 107,
            (107, "-"): 108,
            (108, " "): 108,
            (108, "-"): 109,
        }
        
        self.add_range_transitions()
        
    def add_range_transitions(self):
       
        for char in "abcdefghijklmnopqrstuvwxyz":
            self.transitions[(6, char)] = 6 #
            self.transitions[(48, char)] = 48 #
            self.transitions[(59, char)] = 60 #
            self.transitions[(60, char)] = 60 #
            self.transitions[(41, char)] = 42
            self.transitions[(42, char)] = 42
            self.transitions[(89, char)] = 90
            self.transitions[(90, char)] = 90

        for char in "0123456789":
            self.transitions[(34, char)] = 35 #
            self.transitions[(36, char)] = 37 #
            self.transitions[(47, char)] = 35 #
            self.transitions[(73, char)] = 74 #
            self.transitions[(74, char)] = 74 #
            self.transitions[(89, char)] = 91
            self.transitions[(104, char)] = 105
            self.transitions[(105, char)] = 105

    def process(self, text):
        
        current_state = 0  
        
        text = text.lower()
        print(text)
        for char in text:
            transition = (current_state, char)
            if transition in self.transitions:
                current_state = self.transitions[transition]
                print(f"[{current_state}]", end=" -> ")

            else:
                current_state = 0  

            if current_state in self.final_states:
                return True
                            
        return False
    
    def process_of_text(self, text):
        current_state = 0  
        patterns_found = []
        extracted_sql = ""
        
        text = text.lower()
        print(text)
        for char in text:
            transition = (current_state, char)
            if transition in self.transitions:
                current_state = self.transitions[transition]
                #print(f"[{current_state}]", end=" -> ")
                extracted_sql += char
            else:
                current_state = 0  
                extracted_sql = ""

            if current_state in self.final_states:
                patterns_found.append(extracted_sql)                
                print(extracted_sql)
                extracted_sql = ""
                
        if patterns_found:
            return True, patterns_found                            
        return False
    
  
afd = SQLInjectionAFD()
#text_to_check = "Hola esta es mi cadena de texto ' OR '1'='1-- - ahora si ' and sleep(5)-- - probando probando ' union select database()-- -"
#text_to_check = "Esto es un texto de ejemplo 1' order by 100-- - nada más"
text_to_check = "' union select database()-- -"
#if afd.process(text_to_check):
#    print("Posible SQL Injection detectado.")
#else:
#    print("No se detectó SQL Injection.")
