# -*- coding: utf-8 -*-

'''
Created on 2014/2/6

@author: romulus
'''
from dircache import listdir
from genericpath import isfile
from ntpath import join
from xml.etree import ElementTree


dir_path = "D:/KCBLA-Data/"
xml_files = [ f for f in listdir(dir_path) if isfile(join(dir_path, f)) ]

def calc54ss(xml_files):
    sortie = 0
    boss = 0
    evasion = { '4':0, '6':0, '10':0 }
    result = { 'S':0, 'A':0, 'B':0, 'C':0, 'D':0, 'E':0 }
    casualities = [0, 0, 0, 0, 0]
    lastcell = 0
    lastxml = ''
#     debug = ''
    for fname in sorted(xml_files):
        if not '5-4-' in fname: continue
        ss = fname.split(' ')
        stage = ss[1]
        cell = stage[4:]
        if cell == '4':
            sortie += 1
        if cell == '15':
            boss += 1
            result[ss[2][0]] += 1
        if cell in ['1', '3', '4']:
            if lastcell in [ '4', '6', '10' ]:
                evasion[lastcell] += 1
#                 print debug
#             debug = ''
#         debug += cell + '-'
        lastcell = cell
        lastxml = fname
    print '出撃：%d' % sortie
    print 'ボス到達：%d (%.1f%%)' % (boss, boss * 100.0 / sortie)
    print 'ボス勝利：%d (%.1f%%)' % (result['S'] + result['A'] + result['B'], (result['S'] + result['A'] + result['B']) * 100.0 / sortie)
    print '　S：%d' % result['S']
    print '　A：%d' % result['A']
    print '　B：%d' % result['B']
    print 'ボス敗北：%d (%.1f%%)' % (result['C'] + result['D'], (result['C'] + result['D']) * 100.0 / sortie)
    print '　C：%d' % result['C']
    print '　D：%d' % result['D']
    print '１マス目撤退：%d (%.1f%%)' % (evasion['4'], evasion['4'] * 100.0 / sortie)
    print '２マス目撤退：%d (%.1f%%)' % (evasion['6'], evasion['6'] * 100.0 / sortie)
    print '３マス目撤退：%d (%.1f%%)' % (evasion['10'], evasion['10'] * 100.0 / sortie)

def calc22(xml_files):
    last = 0
    result = [-1, -1, -1, -1, 0, 0, 0, 0]  # Boss,6,4,5
    compass = [[0, 0], [0, 0], [0, 0], [0, 0]]  # Start, E, NE, NEE 
    for fname in xml_files:
        if "Practice" in fname: continue
        if not fname.endswith('xml'): continue
        ss = fname.split(" ")[1].split("-")
        stage = int(ss[0])
        smap = int(ss[1])
        cell = int(ss[2])
        if not (stage == 2 and smap == 2): continue
        print cell
        if last == 0:
            last = cell
            if cell == 1:
                compass[0][0] += 1
            elif cell == 4:
                result[4] += 1
                compass[0][1] += 1
                compass[1][0] += 1
                last = 0
                print '南東'
            elif cell == 7:
                result[7] += 1
                compass[0][1] += 1
                compass[1][1] += 1
                last = 0
                print 'BOSS'
        elif last == 1:
            last = cell
            if cell == 6:
                result[6] += 1
                compass[0][0] += 1
                compass[2][1] += 1
                compass[3][0] += 1
                last = 0
                print '北東'
            elif cell == 1:
                result[5] += 1
                compass[3][1] += 1
                compass[0][0] += 1
                print '+バーナー'
            elif cell == 4:
                result[4] += 1
                result[5] += 1
                compass[3][1] += 1
                compass[0][1] += 1
                compass[1][0] += 1
                last = 0
                print '+バーナー'
                print '南東'
            elif cell == 7:
                result[7] += 1
                result[5] += 1
                compass[3][1] += 1
                compass[0][1] += 1
                compass[1][1] += 1
                last = 0
                print '+バーナー'
                print 'BOSS'
        else:
            print "ERROR: last=%d" % last
    
    count = result[4] + result[5] + result[6] + result[7]
    print "南東:%d バーナー:%d 北東:%d ボス:%d" % (result[4], result[5], result[6], result[7])
         
def calc44(xml_files):
    last = 0
    result = [0, 0, 0]  # ボス、南、撤退@1、撤退@4、、撤退@12
    rank = {"S":0, "A":0, "B":0, "C":0, "D":0}
    for fname in xml_files:
        if "Practice" in fname: continue
        if not fname.endswith('xml'): continue
        ss = fname.split(" ")[1].split("-")
        stage = int(ss[0])
        smap = int(ss[1])
        cell = int(ss[2])
        if stage == 4 and smap == 4:
            if cell == 1:
                if last == 10:
                    result[0] += 1
                elif last == 14:
                    result[1] += 1
                else:
                    result[2] += 1
            if cell == 10:
                rank[fname.split(" ")[2][0]] += 1
            last = cell
    
    if last == 10:
        result[0] += 1
    elif last == 14:
        result[1] += 1
    else:
        result[2] += 1
    
    count = result[0] + result[1] + result[2]
    print 'Boss:%d (%d%%) - %dS %dA %dB %dC %dD\nCompass:%d (%d%%)\nWithdrawal:%d (%d%%)\n' % \
         (result[0], 100 * result[0] / count, rank['S'], rank['A'], rank['B'], rank['C'], rank['D'], result[1], 100 * result[1] / count, result[2], 100 * result[2] / count)
         
calc54ss(xml_files)
