# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:02:58 2016

@author: ThaiSSD
"""
import re
import numpy as np
import itertools

class Hand:
    hand_history = ""
    pocket= 0
    flop = 0
    turn = 0
    river = 0
    stacks = []
    players = []
    cards = 0
#   blinds and ante amount in chips
    ante = 0
    bb = 0
    sb = 0
#   
    allinstreet = 0

#   index of players who posts blinds
    small_blind = 0
    big_blind = 0
    preflop_order = [] #чем больше число чем позже принимает решение
    PRIZE = []
    
    def __init__(self, hh):
#       todo проверка является ли строка hand history
        self.hand_history = hh
#        regex_ps =  "\s?PokerStars\s+?Hand" 
#        regex_888 = "\s?888poker\s+?Hand"
#        t = re.compile(regex_ps)
#        if t.match(self.hand_history):
#            print("poker stars hand detected")
        stacks_regex =  "Seat\s?[0-9]:\s(.*)\s\(\s?\$?(\d*,?\d*)\s(?:in\schips)?" 
        sb = "(.*)?:\sposts small"
        bb = "(.*)?:\sposts big"
        ante_regex = "the ante\s(\d)"
        blinds_regex ="Level.*\((\d*)\/(\d*)"
#        t = re.search(regex)
        
        pocket_regex = "HOLE CARDS\s\*\*\*\sDealt\sto\s\w*\s\[(.*)\]"
        allin_prf_regex = "all-in.*FLOP\s\*\*\*"
        allin_flop_regex = "all-in.*TURN\s\*\*\*"
        allin_turn_regex = "all-in.*RIVER\s\*\*\*"
        allin_river_regex = "all-in.*DOWN\s\*\*\*"
        cards_regex = "(.*):\sshows\s\[(.*)\]"
        

        self.PRIZE = np.array([0.50, 0.50])
        
        tupples = re.findall(stacks_regex,self.hand_history)

        self.players = [x[0] for x in tupples]
        self.stacks = [float(x[1].replace(",","")) for x in tupples]
#       удаление нулевых стэков
        try: 
            self.stacks.index(0.0)
            print(self.stacks.index(0.0))
            while self.stacks.index(0.0) + 1:
                n = self.stacks.index(0.0)
                self.stacks.remove(0.0)
                self.players.pop(n)
        except ValueError:
            pass
        finally:  
            pass
        res= re.search(blinds_regex, self.hand_history)
        if res:
            self.sb = res.group(1)
            self.bb = res.group(2)
        
        res = re.search(ante_regex, self.hand_history)
        if res:
            self.ante = res.group(1)
            
        res = re.search(pocket_regex, self.hand_history)
        if res:
            self.pocket = res.group(1)
        
        res = re.search(bb, self.hand_history) 
        if res:
            self.big_blind = self.players.index(res.group(1))
            self.preflop_order = self.players[self.big_blind+1:] + self.players[:self.big_blind+1]
        else:
            res = re.search(sb, self.hand_history)
            if res:
                self.small_blind = self.players.index(res.group(1))
                self.preflop_order = self.players[self.small_blind+1:] + self.players[:self.small_blind+1]
            
# в префлоп ордер теперь содержится порядок действия игроков как они сидят префлоп от утг до бб

        
#       all in street
        res = re.search(allin_prf_regex, self.hand_history, re.DOTALL)
        if res:
            self.allinstreet = 1
        else:
            res = re.search(allin_flop_regex, self.hand_history, re.DOTALL)
            if res:
                self.allinstreet = 2
            else:
                res = re.search(allin_turn_regex, self.hand_history, re.DOTALL)
                if res:
                    self.allinstreet = 3
                else:
                    res = re.search(allin_river_regex, self.hand_history, re.DOTALL)
                    if res:
                        self.allinstreet = 4
                        
#       players cards
        res = re.findall(cards_regex, self.hand_history)
        self.cards = dict(res)
    def p1p(self, ind, place):
#       вероятность place го места для игрока ind   
            
#       s - список стэков игроков
#       ind - индекс стэка для которого считаестя вероятность
#       place - место целое число, должно быть не больше чем длина списка s
                
        sz = self.getPlayersNumber()
                
#
        if place > sz: return 0
        if ind + 1 > sz: return 0
#       если стэк 0 сразу вернем 0
        
        if self.getStack(ind) == 0:
            if sz - 1 >= np.size(self.PRIZE): return 0
            else: return self.PRIZE[sz-1]
        
        p = []

        #получаем все возможные варианты распределения мест
#           индекс в списке соответствует месту игрока
        for i in itertools.permutations(range(sz), sz):
#               выбираем только те распределения где игрок ind на месте place
            if i[place-1] == ind:
#                    из списка издексов с распределением мест, 
#                    формируем список со значениями стеков
                si = []
                for j in i:
                    si.append(self.getStack(j))
#                    with Profiler() as pr:
                pi = 1
                for j in range(sz):
                    sum_ = sum(si[j:])
                    if sum_ != 0:
                        pi = pi * si[j]/sum_
                   
                p.append(pi)  
        
        result = sum(p)
        return result 
        
    def icm_eq(self, stacks=None):
        if stacks is not None:
            SZ = np.size(stacks)
        else:
            SZ = np.size(self.stacks)
            stacks = np.copy(self.stacks)
        
#        place_probe = np.zeros(SZ, 3)           
 
        
#       end p1p()
   
#       perm = itertools.permutations(range(SZ), SZ)          
            

        ind1 = range(0, SZ)
        
        min_place = min(SZ, np.size(self.PRIZE))
        p1 = np.zeros(shape=(min_place, SZ))
        ind2 = range(0, min_place)
        # p1 строка - занятое место, столбец - номер игрока
        for i in ind1:
            for j in ind2:
                p1[j, i] = self.p1p(i, j + 1) 
                # в функции место нумеруются с 1 до 3, в матрице с 0 до 2  
            
#       
        eq = np.dot(self.PRIZE[:min_place], p1)
        return eq
#   end icm_eq()
        
    def tie_factor(self):
        eq = self.icm_eq()
        st = np.array(self.stacks)
        sz = np.size(st)
        result = np.zeros((sz, sz))
        for i in range(sz):
            for j in range(sz):
                if i == j : continue
               
                stacks_win = np.copy(st)
                stacks_lose = np.copy(st)
                if st[i] > st[j]:
                    stacks_win[i] = st[i] + st[j]
                    stacks_win[j] = 0
                    stacks_lose[i] = st[i] - st[j]
                    stacks_lose[j] = st[j] * 2
                else:
                    stacks_win[i] = st[i] * 2
                    stacks_win[j] = st[j] - st[i]
                    stacks_lose[i] = 0
                    stacks_lose[j] = st[i] + st[j]
                eq_win = self.icm_eq(stacks_win)
                eq_lose = self.icm_eq(stacks_lose)
#                print(stacks_win)
#                print(stacks_lose)
#                print(eq_win)
#                print(eq_lose)
#                
#                print(i, j)   
                bubble_factor = (eq[i] - eq_lose[i]) / (eq_win[i] - eq[i]) 
                result[i, j] = bubble_factor / (1 + bubble_factor)
#                if i > 1 and j > 1: return result
        return result        
#   end tie_factor()
        
    
    def tournamentPosition(self, player):
        
        try: 
            i = self.players.index(player)
        except ValueError:
            print("no player " + player)
            return -1
        
        sp = self.stacks[i]
        result = 1
#        
        for s in self.stacks:
            if s > sp: 
                result +=1
                
        return result
#   enf tournamentPosition()
        
    
    def tablePosition(self, player):
         return(self.preflop_order)
# сколько еще игроков будут действовать на префлопе после игрока
                
#   end tablePosition()
         
    
    def isChipLeader(self, player):
        
        if self.tournamentPosition(player) == 1:
            return True
        else: return False

#end isChipLeader()

    def tournamentPositionL(self, player): 
# позиция игрока среди игроков сидящих слева т.е. действующих на префлопе после него
       
        if self.big_blind:
            if self.big_blind==self.players.index(player): return self.tournamentPosition(player)
            
        try: 
            i = self.players.index(player)
            
        except ValueError:
            print("no player " + player)
            return -1
        
        sp = self.stacks[i]
        result = 1
        
          
        i = self.preflop_order.index(player)
        for s in [self.stacks[ind1] for ind1 in [self.players.index(p) for p in self.preflop_order[i:]]]:
            if s > sp: 
                result +=1
                
        return result
#   enf tournamentPosition()
        
    def getStack(self, player):
#       возвращает стэк игрока 
#       player - номер игрока int или имя игрока str
#        
        
        if type(player) is str:
            try: 
                i = self.players.index(player)
            except ValueError:
                print("no player " + player)
                return -1
            
            sp = self.stacks[i]
        
        if type(player) is int:
            try: 
                sp = self.stacks[player]
            except IndexError:
                print("no such index " + player)
                return -1
                  
        return sp
                
#        end getStack
    
    def getStackList(self):
#       возвращает сисок стэков
#        
        return self.stacks
    
#    end getStackList
        
    def isChipLeaderL(self, player):
        
        if self.tournamentPositionL(player) == 1:
            return True
        else: return False

#end isChipLeaderL()
        
    def getPlayersNumber(self):
#   возвращает число игроков
#    
        return len(self.stacks)

#   end getPlayersNumber
    
    def getAnte(self):
        return self.ante
    
    def getBB(self):
        return self.bb
    
    
    def getSB(self):
        return self.sb
    
    def getAllinStreet(self):
        
#        return :
#       0 no all in in hand
#       1 preflop all in
#       2 flop all in
#       3 turn
#       4 river
        return self.allinstreet
        
    def getPocketCards(self):
#       returns Hero hand as string
        return self.pocket
    
    def getKnownCards(self):
#        returns list with known cards. position in the list corresponds 
#       player position
        return self.cards
        
        