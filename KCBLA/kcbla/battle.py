# -*- coding: utf-8 -*-

'''
Created on 2014/2/6

@author: romulus
'''
import math

from kcbla.data import getArmor
from kcbla.params import torpedo_bomber_power, bomber_power, HACNUM, LACNUM, use_two_bombers
from xml.etree.ElementTree import ElementTree


class Battle:
    def __init__(self, doc):
        ff = doc.find('.//FormationF')
        if not ff is None:
            self.ff = ff.text
            self.fe = doc.find('.//FormationE').text
        else:
            self.ff = u'不明'
            self.fe = u'不明'
        try:
            self.encount = doc.find('.//FormationVs').text
        except AttributeError:
            self.encount = u'不明'
#         self.stage3 = Stage3(doc)
#         self.opening = OpeningAttackPhase(doc, False)
#         self.e_opening = OpeningAttackPhase(doc, True)
        self.bbPhase = BombardPhase(doc)
        self.tpdPhase = TorpedoPhase(doc)
        self.attackers = {}
        self.extraCond = True
        for doc_ship in doc.findall('.//ShipKF/Ship'):
            attacker = Attacker(doc_ship)
            if attacker.index == -1:
                attacker.index = 1 + len(self.attackers)
            if isLegalAtIndex(attacker.index):
                self.attackers[attacker.index] = attacker
                # Extra conditions
#                 if not '瑞雲' in attacker.items or '試製晴嵐' in attacker.items:
#                     self.extraCond = False

class OpeningAttackPhase:
    def __init__(self, doc, count_enemy):
        self.attacks = []
        if count_enemy:
            doc_oa = doc.findall('.//OpeningAttackE/DirTableElm')
        else:
            doc_oa = doc.findall('.//OpeningAttackF/DirTableElm')
#         self.firstAfterHp = int(doc_oa[0].find('./AfterHp').text)
        for elm in doc_oa:
            tor = Torpedo(elm)
            if tor.isLegal:
                self.attacks.append(tor)

class TorpedoPhase:
    def __init__(self, doc):
        self.attacks = []
        # Extra check of invalid torpedo
#         try:
#             if int(doc.findall('.//RaigekiF/DirTableElm/BeforHp')[0].text) <= 12:
#                 return
#         except IndexError:
#             pass
        doc_tor = doc.findall('.//RaigekiF/DirTableElm')
        for elm in doc_tor:
#             if isLegalTargetIndex(int(elm.find('./RaiIndex').text)):
            tor = Torpedo(elm)
            if tor.isLegal:
                self.attacks.append(tor)

class Stage3:
    def __init__(self, doc):
        self.attacks = []
        doc_stage3 = doc.find('.//Stage3E')
        if doc_stage3 is None:
            return
        elms = doc_stage3.findall('./IndDfTableElm')
        bomber_count = 1
        if use_two_bombers:
            if len(elms) == 1: bomber_count = 2
        for elm in elms:
            df = elm.find('./Name').text
            torpedo = elm.find('./RaiFlag').text
            bomb = elm.find('./BakFlag').text
            if torpedo == '1' and bomb == '1': continue
            dmg = int(elm.find('Damage').text)
            st2 = int(doc.find('.//Stage2FCount').text)
            cl = int(elm.find('ClFlag').text)
            if torpedo == '1':
                self.attacks.append(ACTorpedo(df, cl, dmg, st2))
            else:
                self.attacks.append(ACBomb(df, cl, dmg, st2, bomber_count))

class Attack(object):
    flags = 0
    target = None
    HIT = 0x1
    CRTIICAL = 0x2
    FATAL = 0x4
    OUTLET = 0x8
    BOTH_MISS = 0x10
    HALF_HIT = 0x20
    BOTH_HIT = 0x40
    def __init__(self, df):
        if df is None:
            self.target = 'BUG'
        else:
            self.target = df
    def calcRange(self, armor, clx):
        pass
    def low(self, armor):
        return math.floor(armor * 2 / 3)
    def high(self, armor):
        return math.floor(armor * 4 / 3)
    def outlet(self, dmg, dmgRange, cl):
        self.flags |= Attack.OUTLET
        print 'OUTLET!'    
        print 'Damage %d in range %s where cl=%s' % (dmg, dmgRange, cl)
        print
           
class ACTorpedo(Attack):
    def __init__(self, df, cl, dmg, st2):
        super(ACTorpedo, self).__init__(df)
        clx = 1.5 if cl == 1 else 1           
        dmgRange = self.calcRange(getArmor(df), clx)
        if dmg > 0:
            if cl > 0:
                self.flags |= Attack.CRTIICAL
            if dmg > 0:
                self.flags |= Attack.HIT
            if dmg > dmgRange[1][1] or dmg < dmgRange[0][0]:
                if st2 == 2 * HACNUM:
                    self.outlet(dmg, dmgRange, cl)
                    return
                else:
                    if dmg > dmgRange[0][1]:
                        self.flags |= Attack.FATAL
            elif dmg >= dmgRange[1][0] and dmg <= dmgRange[1][1]:
                self.flags |= Attack.FATAL
            
    def calcRange(self, armor, clx):
        low = self.low(armor)
        high = self.high(armor)
        base = 25 + math.sqrt(HACNUM) * torpedo_bomber_power
        lbase = 25 + math.sqrt(LACNUM) * torpedo_bomber_power
        mbase = base * 0.8
        sbase = base * 1.5
        mbase = 150 + math.sqrt(mbase - 150) if mbase > 150 else mbase
        sbase = 150 + math.sqrt(sbase - 150) if sbase > 150 else sbase
        lmbase = lbase * 0.8
        lsbase = lbase * 1.5
        lmbase = 150 + math.sqrt(lmbase - 150) if lmbase > 150 else lmbase
        lsbase = 150 + math.sqrt(lsbase - 150) if lsbase > 150 else lsbase
        power = math.floor(mbase * clx)
        lpower = math.floor(lmbase * clx)
        spower = math.floor(sbase * clx)
        lspower = math.floor(lsbase * clx)
        return ((lpower - high, power - low), (lspower - high, spower - low))

        
class ACBomb(Attack):
    def __init__(self, df, cl, dmg, st2, bomber_count):
        super(ACBomb, self).__init__(df)
        clx = 1.5 if cl == 1 else 1           
        dmgRange = self.calcRange(getArmor(df), clx)
        if bomber_count == 1:
            if dmg > 0:
                if cl > 0:
                    self.flags |= Attack.CRTIICAL
                if dmg > 0:
                    self.flags |= Attack.HIT
                if dmg > dmgRange[1] or dmg < dmgRange[0]:
                    if st2 == 2 * HACNUM:
                        self.outlet(dmg, dmgRange, cl)
                        return
        elif bomber_count == 2:
            if cl > 0:
                self.flags |= Attack.CRTIICAL
            if dmg == 0:
                self.flags |= Attack.BOTH_MISS
            elif dmg >= dmgRange[0] * 2:
                self.flags |= Attack.BOTH_HIT
            elif dmg >= dmgRange[0]:
                self.flags |= Attack.HALF_HIT
            else:
                self.outlet(dmg, dmgRange, cl)
                return
            
    def calcRange(self, armor, clx):
        low = self.low(armor)
        high = self.high(armor)
        base = 25 + math.sqrt(HACNUM) * bomber_power
        lbase = 25 + math.sqrt(LACNUM) * bomber_power
        base = 150 + math.sqrt(base - 150) if base > 150 else base 
        power = math.floor(base * clx)
        lbase = 150 + math.sqrt(lbase - 150) if lbase > 150 else lbase 
        lpower = math.floor(lbase * clx)
        return (lpower - high, power - low)

class Torpedo(Attack):
    def __init__(self, elm):
        target = elm.find('./RaiName').text
        self.isLegal = not target is None
        super(Torpedo, self).__init__(target)
        self.oat = elm.find('./Name').text
        self.dmg = int(elm.find('./YDam').text)
        if self.dmg > 0:
            self.flags |= Attack.HIT
        if int(elm.find('./Cl').text) == 2:
            self.flags |= Attack.CRTIICAL

class BombardPhase:
    def __init__(self, doc):
        doc_bombards = doc.find('./BattlePhaseList/DayPhase/HougekiTable')
        self.attacks = []
        if doc_bombards is None:
            return
        for doc_turn in doc_bombards.findall('./Hougeki'):
            for doc_bombard in doc_turn.findall('.//SequenceElm'):
                b = Bombard(doc_bombard)
#                 if b.beforeHp >= 15 and isLegalAtIndex(b.atIndex):
#                 if b.attacker == '戦艦レ級 elite':
                self.attacks.append(b)
        
class Bombard(Attack):
    def __init__(self, doc_bb):
        super(Bombard, self).__init__(doc_bb.find('.//DfName').text)
        self.beforeHp = int(doc_bb.find('.//BeforHp').text)
        self.atIndex = int(doc_bb.find('./AtIndex').text)
        self.attacker = doc_bb.find('./AtName').text        
        self.damage = int(doc_bb.find('.//Damage').text)
        if self.damage > 0:
            self.flags |= Attack.HIT
        if int(doc_bb.find('.//Cl').text) == 2:
            self.flags |= Attack.CRTIICAL

class Attacker:
    def __init__(self, doc_ship):
        try:
            self.index = int(doc_ship.find('./Index').text)
        except:
            self.index = -1
        self.name = doc_ship.find('./Name').text
        self.lv = int(doc_ship.find('./Lv').text)
        self.items = []
        for doc_item in doc_ship.findall('./SlotItem/Name'):
            self.items.append(doc_item.text)
            
    def toString(self):
        ret = self.name
        for eq in self.items:
            if not eq is None:
                ret += '/' + eq
        return ret
    
    def __hash__(self):
        return hash(self.toString())
    
    def __eq__(self, another):
        return self.toString() == another.toString()

def isLegalAtIndex(index):
    return index <= 6

