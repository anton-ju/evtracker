# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:02:58 2016

@author: ThaiSSD
"""
import re
import numpy as np
import itertools

testhand = """PokerStars Hand #157033607016: Tournament #1638818751, $13.89+$1.11 USD Hold'em No Limit - Level VIII (150/300) - 2016/08/08 23:36:07 MSK [2016/08/08 16:36:07 ET]
Table '1638818751 1' 9-max Seat #1 is the button
Seat 1: DiggErr555 (1386 in chips)
Seat 4: IAmTheDisco (3413 in chips)
Seat 7: hugo023 (2138 in chips)
Seat 9: Neo1186 (6563 in chips)
DiggErr555: posts the ante 25
IAmTheDisco: posts the ante 25
hugo023: posts the ante 25
Neo1186: posts the ante 25
IAmTheDisco: posts small blind 150
hugo023: posts big blind 300
*** HOLE CARDS ***
Dealt to DiggErr555 [8d As]
Neo1186: raises 6238 to 6538 and is all-in
DiggErr555: calls 1361 and is all-in
IAmTheDisco: folds
hugo023: folds
Uncalled bet (5177) returned to Neo1186
*** FLOP *** [8s Ks 4d]
*** TURN *** [8s Ks 4d] [Kh]
*** RIVER *** [8s Ks 4d Kh] [5h]
*** SHOW DOWN ***
Neo1186: shows [2d 4c] (two pair, Kings and Fours)
DiggErr555: shows [8d As] (two pair, Kings and Eights)
DiggErr555 collected 3272 from pot
*** SUMMARY ***
Total pot 3272 | Rake 0
Board [8s Ks 4d Kh 5h]
Seat 1: DiggErr555 (button) showed [8d As] and won (3272) with two pair, Kings and Eights
Seat 4: IAmTheDisco (small blind) folded before Flop
Seat 7: hugo023 (big blind) folded before Flop
Seat 9: Neo1186 showed [2d 4c] and lost with two pair, Kings and Fours



"""
th2 = """
***** 888poker Hand History for Game 655462938 *****
$100/$200 Blinds No Limit Holdem - *** 08 08 2016 23:03:27
Tournament #83728678 $18.30 + $1.70 - Table #1 9 Max (Real Money)
Seat 5 is the button
Total number of players : 5
Seat 1: Mr.Tatt00 ( $3,548 )
Seat 5: bilguun0226 ( $1,614 )
Seat 7: DiggErr555 ( $4,886 )
Seat 9: MatjeP ( $1,058 )
Seat 10: CerealRobber ( $2,394 )
Mr.Tatt00 posts ante [$20]
CerealRobber posts ante [$20]
MatjeP posts ante [$20]
bilguun0226 posts ante [$20]
DiggErr555 posts ante [$20]
DiggErr555 posts small blind [$100]
MatjeP posts big blind [$200]
** Dealing down cards **
Dealt to DiggErr555 [ 8c, Qs ]
CerealRobber raises [$400]
Mr.Tatt00 folds
bilguun0226 raises [$1,594]
DiggErr555 folds
MatjeP calls [$838]
CerealRobber folds
** Dealing flop ** [ 6d, 7s, Kd ]
** Dealing turn ** [ 5c ]
** Dealing river ** [ 8d ]
** Summary **
bilguun0226 shows [ Qd, Js ]
MatjeP shows [ Ac, Ad ]
MatjeP collected [ $2,676 ]
"""

th3 = """
***** Hand History for Game 15549114547 *****
NL Texas Hold'em $215 USD Buy-in Trny:128730277 Level:12  Blinds-Antes(1 200/2 400 -400) - Monday, September 26, 01:30:41 MSK 2016
Table Powerfest #193 - Main Event $500,000 Gtd (128730277) Table #83 (Real Money)
Seat 5 is the button
Total number of players : 9/9
Seat 6: Achileus34 ( 63,222 )
Seat 8: Alex0876 ( 107,844 )
Seat 9: ChickAndChipS ( 180,112 )
Seat 7: Corlusion ( 205,081 )
Seat 1: DiSTEFANO_ ( 61,490 )
Seat 4: DiggErr555 ( 53,728 )
Seat 5: KatozaForAll ( 47,649 )
Seat 2: PokerPalvo1499 ( 80,022 )
Seat 3: ihadafeeling ( 115,918 )
Trny:128730277 Level:12
Blinds-Antes(1 200/2 400 -400)
DiSTEFANO_ posts ante [400]
PokerPalvo1499 posts ante [400]
ihadafeeling posts ante [400]
DiggErr555 posts ante [400]
KatozaForAll posts ante [400]
Achileus34 posts ante [400]
Corlusion posts ante [400]
Alex0876 posts ante [400]
ChickAndChipS posts ante [400]
Achileus34 posts small blind [1,200].
Corlusion posts big blind [2,400].
** Dealing down cards **
Dealt to DiggErr555 [  Th Kh ]
Alex0876 folds
ChickAndChipS folds
DiSTEFANO_ folds
PokerPalvo1499 raises [5,280]
ihadafeeling folds
DiggErr555 will be using their time bank for this hand.
DiggErr555 is all-In  [53,328]
KatozaForAll folds
Achileus34 folds
Corlusion is all-In  [202,281]
PokerPalvo1499 folds
** Dealing Flop ** [ Qd, Td, 7s ]
** Dealing Turn ** [ 6d ]
** Dealing River ** [ 6s ]
Corlusion shows [ Jc, Jh ]two pairs, Jacks and Sixes.
DiggErr555 shows [ Th, Kh ]two pairs, Tens and Sixes.
Corlusion wins 151,353 chips from the side pot 1 with two pairs, Jacks and Sixes.
Corlusion wins 116,736 chips from the main pot with two pairs, Jacks and Sixes.
Player DiggErr555 finished in 840.
"""


class Hand:
    hand_history = ""
    card1 = 0
    card2 = 0
    flop = 0
    turn = 0
    river = 0
    stacks = []
    players = []
    ante = 0
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
        regex =  "Seat\s?[0-9]:\s(.*)\s\(\s?\$?(\d*,?\d*)\s(?:in\schips)?" 
        sb = "(.*)?:\sposts small"
        bb = "(.*)?:\sposts big"
#        t = re.search(regex)
        
        self.PRIZE = np.array([0.50, 0.50])
        
        tupples = re.findall(regex,self.hand_history)

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
        
        
        
        