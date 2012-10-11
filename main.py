from random import randint

def check(key, e): #e is a string (the executeable command)
#### RIGHT NOW ASSUMES THERE IS MAX ONE FOUND!!!!!
    surroundings = '[](), '
    if key in e:
        if e.index(key)==0 or e[e.index(key)-1] in surroundings:
            if e.index(key)+len(key)==len(e) or e[e.index(key)+len(key)] in surroundings:
                return True
    return False

class Warrior:
    def __init__(self, pointer, name):
        self.next_ptr_read = 0
        self.reads = [pointer]
        self.name = name
        self.variables = {}

    def evaluate(self, expr):
        try:
            result = str(eval(expr_r, self.variables))
            return result
        except:
            print 'Warning to ' + self.name + '! Expression: "'+expr+' coult not be evaluated. Turn skipped.'
        return ''

    def next_move(self, board):
        do = board[ self.read[self.next_ptr_read] ]
        
        ##### Now analyze dat language:
        goto_next = 1
        #Goto:
        if do.startswith('goto'):
            stripped = do.replace('goto','').strip()
            goto_next = self.evaluate(stripped)
        
        #Define or change variable:
        elif '=' in do:
            var = do[ :do.index('=') ]
            expr = do[ do.index('=')+1: ]
            self.variables[var] = self.evaluate(expr)


        ## And go to next statement:
        self.read += goto_next
        if self.read >= len(board):
            self.read = 0

        ##### Go to next thread:
        self.next_ptr_read += 1
        if self.next_ptr_read >= len(self.read):
            self.next_ptr_read = 0

class WarBoard:
    def __init__(self, f_warrior1, f_warrior2, N=300, m=100):
        self.N = N #Board length
        self.m = m #Warrior max lenght
        self.warrior1_list, self.warrior1_name = self.read(f_warrior1)
        self.warrior2_list, self.warrior2_name = self.read(f_warrior2)
        self.board = self.init_board()

        self.warrior1 = Warrior(0, self.warrior1_name)
        self.warrior2 = Warrior(self.warrior2_start, self.warrior2_name)

    def __str__(self):
        out = ''
        for e in self.board:
            out += e.replace('return', 'r')+'->'
        return out
                            
    def read(self, f_warrior):
        l = list()
        f = open(f_warrior)
        count = 0
        for line in f:
            if count == self.m:
                break
            elif count == 0:
                name = line.strip()
            else:
                l.append(line.strip())
            count += 1
        
        replace = dict()
        for i,e in enumerate(l):
            if ':' in e:
                label = e[:e.index(':')]
                replace[label] = i
                l[i] = e[e.index(':')+1:]
        
        for i,e in enumerate(l):
            for key in replace:
                if check(key, e):
                    l[i] = e.replace(key, str(replace[key] - i))

        return l, name

    def init_board(self):
        board = ['return']*self.N
        for i, s in enumerate(self.warrior1_list):
            board[i] = s
        self.warrior2_start = randint(self.m, self.N-self.m-1)
        for i, s in enumerate(self.warrior2_list):
            board[self.warrior2_start + i] = s
        
        return board
        
#### DEBUGGING AND TESTING:
test = WarBoard('warrior1.hlw', 'warrior2.hlw')
print test
