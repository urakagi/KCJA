# -*- coding: utf-8 -*-

import codecs

'''
Created on 2014/4/11

@author: romulus
'''

f = codecs.open("C:\Users\Romulus\Documents\Dropbox\GreenSofts\KCRDB\KCRDB-missionresult.log", "r", "shift-jis")
line = f.readline()

normal = 0
extreme = 0

while len(line) > 0:
    ss = line.split(',')
    date = ss[0]
    exp = ss[1].replace('"', '')
    result = int(ss[2])
    ships = []
    equips = []
    lvs = []
    kira = 0
    drum = 0
    for x in range(0, 6):
        if len(ss) > x * 8 + 4:
            ships.append(ss[x * 8 + 4])
            lvs.append(int(ss[x * 8 + 5]))
            if int(ss[x * 8 + 6]) > 49:
                kira += 1
            for y in range(0, 4):
                if ss[x * 8 + 7 + y].replace('"', '') == u'ドラム缶(輸送用)':
                    drum += 1
    
    if exp == u'北方鼠輸送作戦' and kira == 2 and drum >= 4:
        if result == 1:
            res = '成功'
            normal += 1
        elif result == 2:
            res = '大成功'
            extreme += 1
        else:
            res = '失敗'
        print '%s: キラ%d ドラム缶%d' % (res, kira, drum)
    line = f.readline()

print '大成功 %d/%d' % (extreme, normal + extreme)
 
f.close()
