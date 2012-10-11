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
        self.alive = True

    def evaluate(self, expr):
        try:
            result = str(eval(expr, self.variables))
            return result
        except:
            print '1: Warning to ' + self.name + '! Expression: "'+expr+'" coult not be evaluated. Turn skipped.'
        return ''

    def next_move(self, board):
        do = board[ self.reads[self.next_ptr_read] ]

        print 'Now doing: '+do+' for warrior '+self.name+'.'
        
        ##### Now analyze dat language:
        goto_next = 1
        next_ptr = 1
        #Goto:
        if do.startswith('goto'):
            stripped = do.replace('goto','').strip()
            try:
                goto_next = int(self.evaluate(stripped))
            except:
                print '2: Warning to ' + self.name + '! Expression: "'+do+'" coult not be evaluated. Turn skipped.'
        
        #Define or change variable:
        elif '=' in do.replace('==',''):
            var = do[ :do.index('=') ].strip()
            expr = do[ do.index('=')+1: ]
            self.variables[var] = int(self.evaluate(expr))

        #Copy:
        elif do.startswith('copy'):
            stripped = do.replace(' ','').replace('copy(','').strip().rstrip(')')
            expr1 = ''
            expr2 = ''
            paren = 0
            bracket = 0
            first = True
            for s in stripped:
                if first:
                    if s == ',' and paren == 0 and bracket == 0:
                        first = False
                    else:
                        expr1 += s
                else:
                    expr2 += s
            
            from_index = ( self.reads[self.next_ptr_read] + int(self.evaluate(expr1)) ) % len(board)
            to_index = ( self.reads[self.next_ptr_read] + int(self.evaluate(expr2)) ) % len(board)
            board[to_index] = board[from_index]

        #Something else counts as return:
        else:
            del self.reads[self.next_ptr_read]
            next_ptr = 0
            if len(self.reads) == 0:
                alive = False
                return False


        ## And go to next statement:
        self.reads[self.next_ptr_read] += goto_next
        if self.reads[self.next_ptr_read] >= len(board):
            self.reads[self.next_ptr_read] = 0

        ##### Go to next thread:
        self.next_ptr_read += next_ptr
        if self.next_ptr_read >= len(self.reads):
            self.next_ptr_read = 0

        return True

class WarBoard:
    def __init__(self, f_warrior1, f_warrior2, N=300, m=100):
        self.N = N #Board length
        self.m = m #Warrior max lenght
        self.warrior1_list, self.warrior1_name = self.read(f_warrior1)
        self.warrior2_list, self.warrior2_name = self.read(f_warrior2)
        self.board = self.init_board()

        self.warrior1 = Warrior(0, self.warrior1_name)
        self.warrior2 = Warrior(self.warrior2_start, self.warrior2_name)

        self.turn = randint(1,2)

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
    
    def next_move(self):
        if self.turn == 1:
            if not self.warrior1.next_move(self.board):
                print '\n\nWarrior 2 wins!\n\n'
                exit()
        if self.turn == 2:
            if not self.warrior2.next_move(self.board):
                print '\n\nWarrior 1 wins!\n\n'
                exit()
        
        self.turn = 1 if self.turn == 2 else 2
        
        print self, len(self.board)

#### DEBUGGING AND TESTING:
test = WarBoard('warrior1.hlw', 'warrior2.hlw')
for i in range(1,500):
    test.next_move()
