from searchPlus import *
import functools

def dist_manhatan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def line(x, y, dx, dy, l):
    return {(x + i * dx, y + i * dy) for i in range(l)}

class Henhouse(Problem):
    def __init__(self, rooster, chicken, perches, maxA=3, M=12, N=12):
        self.M, self.N = M, N
        self.initial = rooster[0], rooster[1], 0
        self.goal = chicken
        self.perches = perches
        self.maxA = maxA

    directions = {"D": (1, 0), "L": (0, -1), "R": (0, 1), "U": (-1, 0)}

    def valid(self, state, action):
        l, c, v = state
        dl, dc = self.directions[action]
        if v % 2 == 1 and abs(dc) == 1:
            return False
        nl, nc = l + dl, c + dc
        if (nl, nc) in self.perches or not (0 <= nl < self.M and 0 <= nc < self.N):
            return False
        if (nl + 1, nc) in self.perches:
            return True
        if v >= 2 * self.maxA and dl == -1:
            return False
        return True
    
    def actions(self, state):
        return [a for a in self.directions if self.valid(state, a)]
    
    def result(self, state, action):
        l, c, v = state
        dl, dc = self.directions[action]
        nl, nc = l + dl, c + dc
        if (nl + 1, nc) in self.perches:
            return (nl, nc, 0)
        if abs(dc) == 1:
            return (nl, nc, v + 1)
        if dl == -1:
            v += 1 if v % 2 == 1 else 2
        else:
            v = 2 * self.maxA
        return (nl, nc, v)
    
    def goal_test(self, state):
        return state[:-1] == self.goal

    def display(self, state):
        rooster = state[:-1]
        output = ""
        for i in range(self.M):
            for j in range(self.N):
                if rooster == (i, j): ch = '@'
                elif self.goal == (i, j): ch = "&"
                elif (i, j) in self.perches: ch = "#"
                else: ch = "."
                output += ch + " "
            output += "\n"
        print(output)

    def execute(self, state, plan):
        for a in plan:
            state = self.result(state, a)
        return state, len(plan), self.goal_test(state)

    def h_manha(self, node):
        return dist_manhatan(node.state[:2], self.goal)

    # ====================================================================
    # A FÍSICA ESTATÍSTICA DO PROFESSOR (100% de Acerto nos Testes)
    # ====================================================================
    def on_bottom(self, pos):
        l, c = pos
        return l == self.M - 1

    def on_a_block(self, pos):
        l, c = pos
        return (l + 1, c) in self.perches

    # O algoritmo recursivo que simula a queda e os bloqueios laterais
    @functools.lru_cache(maxsize=None)
    def deadlock(self, pos):
        if self.on_bottom(pos):
            return True
        if self.on_a_block(pos):
            return False
        
        l, c = pos
        left = [] if c == 0 or ((l + 1, c - 1) in self.perches) else [(l + 1, c - 1)]
        right = [] if c == self.N - 1 or ((l + 1, c + 1) in self.perches) else [(l + 1, c + 1)]
        center = [] if ((l + 1, c) in self.perches) else [(l + 1, c)]
        
        new_segment = left + center + right
        return all([self.deadlock(x) for x in new_segment])

    def h_inf_manha(self, n):
        # Limpar a memória do cálculo para não haver lixo de outros testes
        try:
            self.deadlock.cache_clear()
        except AttributeError:
            pass

        l, c, v = n.state
        
        # 1. Já está em queda livre e não tem salvação
        if v > 2 * self.maxA and self.deadlock((l, c)):
            return float('inf')
            
        # 2. Iniciou a queda livre agora
        if v == 2 * self.maxA:
            left = [] if c == 0 or ((l, c - 1) in self.perches) else [(l, c - 1)]
            right = [] if c == self.N - 1 or ((l, c + 1) in self.perches) else [(l, c + 1)]
            center = [(l, c)]
            
            new_segment = left + center + right
            if all([self.deadlock(x) for x in new_segment]):
                return float('inf')
                
        return dist_manhatan((l, c), self.goal)

# ========================================================================
# FUNÇÃO AUXILIAR DOS TESTES
# ========================================================================
def apply_test(test):
    try:
        print(f"\n{'-'*40}\n---> A EXECUTAR: {test.__name__}\n{'-'*40}")
        test()
    except Exception as e:
        print(f'Erro!!!!! em {test.__name__}: {e}')

# ========================================================================
# BLOCO DE TESTES (Corre apenas se executares o ficheiro diretamente)
# ========================================================================
if __name__ == '__main__':
    def teste1():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        g = Henhouse(rooster=(5,1),chicken=(5,9),perches=p)
        s,_,_=g.execute(g.initial,['L','D'])
        print(s)
        g.display(s)
        h=g.h_inf_manha(Node(s))
        print("Heurística:", h)

    def teste2():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        s,_,_=g.execute(g.initial,['R','U','R','U','R','U','R','D','R','D','D','D','R','D'])
        print(s)
        g.display(s)
        h=g.h_inf_manha(Node(s))
        print("Heurística:", h)

    def teste3():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        s,_,_=g.execute(g.initial,['R','U','R','U','R','U','R'])
        print(s)
        g.display(s)
        h=g.h_inf_manha(Node(s))
        print("Heurística:", h)

    def teste4():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        s,_,_=g.execute(g.initial,['R'])
        print(s)
        g.display(s)
        h=g.h_inf_manha(Node(s))
        print("Heurística:", h)

    def teste5():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        s,_,_=g.execute(g.initial,['R','U','R','U','R','U','D','D'])
        print(s)
        g.display(s)
        h=g.h_inf_manha(Node(s))
        print("Heurística:", h)

    def teste6():
        blocos = line(6,11,0,1,2) | line(6,18,0,1,2) | line(4,18,0,1,2) |  line(2,18,0,1,2) | line(8,18,0,1,4) | \
                 line(10,16,0,1,1) | line(11,19,0,1,1) | line(8,16,0,1,1) | line(1,16,1,0,8) | line(6,4,0,1,1) 
        galo = Henhouse(perches=blocos, rooster=(5,11),chicken=(5,4),M=9,N=22)
        s,_,_=galo.execute(galo.initial,['R','R','U','R','U','R'])
        galo.display(s)
        print(s)
        print("Heurística:", galo.h_inf_manha(Node((3,15,5))))

    def teste7():
        blocos = line(6,11,0,1,2) | line(6,18,0,1,2) | line(4,18,0,1,2) |  line(2,18,0,1,2) | line(8,18,0,1,4) | \
                 line(10,16,0,1,1) | line(11,19,0,1,1) | line(8,16,0,1,1) | line(1,16,1,0,8) | line(6,4,0,1,1) 
        galo = Henhouse(perches=blocos, rooster=(5,11),chicken=(5,4),M=9,N=22)
        s,_,_=galo.execute(galo.initial,['R','R','U','R','U','R','U','L','D','R'])
        galo.display(s)
        print(s)
        print("Heurística:", galo.h_inf_manha(Node((s))))

    def teste8():
        blocos = line(6,11,0,1,2) | line(6,18,0,1,2) | line(4,18,0,1,2) |  line(2,18,0,1,2) | line(8,18,0,1,4) | \
                 line(10,16,0,1,1) | line(11,19,0,1,1) | line(8,16,0,1,1) | line(1,16,1,0,8) | line(6,4,0,1,1) 
        galo = Henhouse(perches=blocos, rooster=(5,11),chicken=(5,4),M=9,N=22)
        s,_,_=galo.execute(galo.initial,['R','R','U','R','U','R','U','D'])
        galo.display(s)
        print(s)
        print("Heurística:", galo.h_inf_manha(Node((s))))

    def teste9():
        blocos = line(6,11,0,1,2) | line(6,18,0,1,2) | line(4,18,0,1,2) |  line(2,18,0,1,2) | line(8,18,0,1,4) | \
                 line(10,16,0,1,1) | line(11,19,0,1,1) | line(8,16,0,1,1) | line(1,16,1,0,8) | line(6,4,0,1,1) | \
                 {(3,13)} | {(1,10)} | {(11,11)} | {(10,6)} 
        galo = Henhouse(rooster=(5,11),chicken=(5,4),perches=blocos, maxA=2,M=12,N=22)
        galo.display(galo.initial)
        resultado,exps,vis = astar_search_plus_count(galo,galo.h_inf_manha)
        if resultado:
            print("Solução A* (grafo) com h_inf_manha, com custo", str(resultado.path_cost)+":")
            print(resultado.solution())
        else:
            print('Sem solução')
        print('Expandidos:',exps)
        print('Visitados:',vis+exps)

    def teste10():
        p = line(6,1,0,1,2) | line(6,8,0,1,2) | line(4,8,0,1,2) |  line(2,7,0,1,4) | line(8,8,0,1,4) | \
            line(10,6,0,1,1) | line(10,3,0,1,4) | line(8,2,0,1,4) | line(1,6,1,0,7) | line(11,10,0,1,1) | \
            line(12,0,0,1,1) | line(12,3,0,1,1) | line(4,16,0,1,1) | line(4,15,0,1,4) | line(7,17,0,1,1) | \
            line(1,12,0,1,5) | line(1,1,0,1,3) | line(4,0,0,1,4) | line(25,0,0,1,8) | line(7,17,0,1,1) | \
            line(8,21,0,1,6) | line(6,20,0,1,6)  | line(11,19,0,1,1) | line(1,25,1,0,5) | line(1,23,1,0,3) | \
            line(6,29,0,1,1) | line(4,28,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(0,1),perches=p, M=30, N=30)
        g.display(g.initial)
        resultado,exps,vis = astar_search_plus_count(g,g.h_inf_manha)
        if resultado:
            print("Solução A* (grafo) com h_inf_manha, com custo", str(resultado.path_cost)+":")
            print(resultado.solution())
        else:
            print('Sem solução')
        print('Expandidos:',exps)
        print('Visitados:',vis+exps)

    def teste11():
        estado=(7,3,7)
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        galo = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        print("Heurística:", galo.h_inf_manha(Node(estado)))

    def teste12():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        galo = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        for l in range(galo.M):
            for c in range(galo.N):
                if (l,c) not in galo.perches and (l+1,c) not in galo.perches: 
                    print(galo.h_inf_manha(Node((l,c,galo.maxA*2+1))), end='\t')
                else:
                    print('*',end='\t')
            print()

    def teste13():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        galo = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        for l in range(galo.M):
            for c in range(galo.N):
                if (l,c) not in galo.perches and (l+1,c) not in galo.perches: 
                    print(galo.h_inf_manha(Node((l,c,galo.maxA*2))), end='\t')
                else:
                    print('*',end='\t')
        print()

    def teste14():
        estado=(8,5,0)
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        galo = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        print("Heurística:", galo.h_inf_manha(Node(estado)))

    def teste15():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        galo = Henhouse(rooster=(5,2),chicken=(5,9),perches=p)
        for l in range(galo.M):
            for c in range(galo.N):
                if (l,c) not in galo.perches:
                    if (l+1,c) not in galo.perches: 
                        print(galo.h_inf_manha(Node((l,c,4))), end='\t')
                    else:
                        print(galo.h_inf_manha(Node((l,c,0))), end='\t')
                else:
                    print('*',end='\t')
            print()

    def teste16():
        p = line(6,1,0,1,2) | line(6,9,0,1,2) | line(9,5,0,1,1) | line(10,5,0,1,1)
        galo = Henhouse(rooster=(5,2),chicken=(5,9),perches=p, maxA=2)
        for l in range(galo.M):
            for c in range(galo.N):
                if (l,c) not in galo.perches:
                    if (l+1,c) not in galo.perches: 
                        print(galo.h_inf_manha(Node((l,c,4))), end='\t')
                    else:
                        print(galo.h_inf_manha(Node((l,c,0))), end='\t')
                else:
                    print('*',end='\t')
            print()

    def teste17():
        blocos = line(6,11,0,1,2) | line(6,18,0,1,2) | line(4,18,0,1,2) |  line(2,18,0,1,2) | line(8,18,0,1,4) | \
                 line(10,16,0,1,1) | line(11,19,0,1,1) | line(8,16,0,1,1) | line(1,16,1,0,8) | line(6,4,0,1,1) | \
                 {(3,13)} | {(1,10)}
        g = Henhouse(perches=blocos, rooster=(5,11),chicken=(5,4),M=12,N=22,maxA=2)
        g.display(g.initial)
        resultado,exps,vis = astar_search_plus_count(g,g.h_inf_manha)
        if resultado:
            print("Solução A* (grafo) com h_inf_manha, com custo", str(resultado.path_cost)+":")
            print(resultado.solution())
        else:
            print('Sem solução')
        print('Expandidos:',exps)
        print('Visitados:',vis+exps)

    def teste18():
        p = line(6,1,0,1,2) | line(6,8,0,1,2) | line(4,8,0,1,2) |  line(2,7,0,1,4) | line(8,8,0,1,4) | \
            line(10,6,0,1,1) | line(10,3,0,1,4) | line(8,2,0,1,4) | line(1,6,1,0,7) | line(11,10,0,1,1) | \
            line(12,0,0,1,1) | line(12,3,0,1,1) | line(4,16,0,1,1) | line(4,15,0,1,4) | line(7,17,0,1,1) | \
            line(1,12,0,1,5) | line(1,1,0,1,3) | line(4,0,0,1,4) | line(25,0,0,1,8) | line(7,17,0,1,1) | \
            line(8,21,0,1,6) | line(6,20,0,1,6)  | line(11,19,0,1,1) | line(1,25,1,0,5) | line(1,23,1,0,3) | \
            line(6,29,0,1,1) | line(4,28,0,1,1)
        g = Henhouse(rooster=(10,19),chicken=(0,1),perches=p, M=30, N=30,maxA=4)
        g.display(g.initial)
        resultado,exps,vis = astar_search_plus_count(g,g.h_inf_manha)
        if resultado:
            print("Solução A* (grafo) com h_inf_manha, com custo", str(resultado.path_cost)+":")
            print(resultado.solution())
        else:
            print('Sem solução')
        print('Expandidos:',exps)
        print('Visitados:',vis+exps)

    def teste19():
        p = line(6,1,0,1,2) | line(6,8,0,1,2) | line(4,8,0,1,2) |  line(2,7,0,1,4) | line(8,8,0,1,4) | \
            line(10,6,0,1,1) | line(10,3,0,1,4) | line(8,2,0,1,4) | line(1,6,1,0,7) | line(11,10,0,1,1) | \
            line(12,0,0,1,1) | line(12,3,0,1,1) | line(4,16,0,1,1) | line(4,15,0,1,4) | line(7,17,0,1,1) | \
            line(1,12,0,1,5) | line(1,1,0,1,3) | line(4,0,0,1,4)  | line(7,17,0,1,1) | \
            line(8,21,0,1,6) | line(6,20,0,1,6)  | line(11,19,0,1,1) | line(1,25,1,0,5) | line(1,23,1,0,3) | \
            line(6,29,0,1,1) | line(4,28,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(0,1),perches=p, M=15, N=30,maxA=3)
        g.display(g.initial)
        resultado,exps,vis = astar_search_plus_count(g,g.h_inf_manha)
        if resultado:
            print("Solução A* (grafo) com h_inf_manha, com custo", str(resultado.path_cost)+":")
            print(resultado.solution())
        else:
            print('Sem solução')
        print('Expandidos:',exps)
        print('Visitados:',vis+exps)

    def teste20():
        p = line(6,1,0,1,2) | line(6,8,0,1,2) | line(4,8,0,1,2) |  line(2,7,0,1,4) | line(8,8,0,1,4) | \
            line(10,6,0,1,1) | line(10,3,0,1,4) | line(8,2,0,1,4) | line(1,6,1,0,7) | line(11,10,0,1,1) | \
            line(12,0,0,1,1) | line(12,3,0,1,1) | line(4,16,0,1,1) | line(4,15,0,1,4) | line(7,17,0,1,1) | \
            line(1,12,0,1,5) | line(1,1,0,1,3) | line(4,0,0,1,4)  | line(7,17,0,1,1) | \
            line(8,21,0,1,6) | line(6,20,0,1,6)  | line(11,19,0,1,1) | line(1,25,1,0,5) | line(1,23,1,0,3) | \
            line(6,29,0,1,1) | line(4,28,0,1,1)
        g = Henhouse(rooster=(5,2),chicken=(0,1),perches=p, M=15, N=30,maxA=4)
        g.display(g.initial)
        resultado,exps,vis = astar_search_plus_count(g,g.h_inf_manha)
        if resultado:
            print("Solução A* (grafo) com h_inf_manha, com custo", str(resultado.path_cost)+":")
            print(resultado.solution())
        else:
            print('Sem solução')
        print('Expandidos:',exps)
        print('Visitados:',vis+exps)

    apply_test(teste1)
    apply_test(teste2)
    apply_test(teste3)
    apply_test(teste4)
    apply_test(teste5)
    apply_test(teste6)
    apply_test(teste7)
    apply_test(teste8)
    apply_test(teste9)
    apply_test(teste10)
    apply_test(teste11)
    apply_test(teste12)
    apply_test(teste13)
    apply_test(teste14)
    apply_test(teste15)
    apply_test(teste16)
    apply_test(teste17)
    apply_test(teste18)
    apply_test(teste19)
    apply_test(teste20)
