# -*- coding: utf-8 -*-

'''
Created on 2014/2/6

@author: romulus
'''

# [Armor, Evasion]
SHIPS = {u'雷巡チ級ｅ': [34, 30], u'重巡リ級Ｆ':[70, 50], u'駆逐ニ級ｅ':[18, 40], u'軽巡ヘ級Ｆ':[39, 46],
         u'駆逐ロ級Ｆ':[24, 52], u'輸送ワ級':[10, 1], u'重巡リ級':[28, 12], u'雷巡チ級':[22, 18],
         u'駆逐ロ級':[6, 15], u'駆逐イ級':[5, 14], u'戦艦ル級':[70, 3], u'重巡リ級ｅ':[60, 20],
         u'軽巡ト級':[20, 15], u'軽巡ヘ級':[18, 15], u'駆逐ハ級':[7, 16], '軽巡ト級ｅ':[36, 28],
         u'空母ヲ級ｅ':[55, 12], u'駆逐ニ級':[9, 18], u'軽巡ト級ｅ':[36, 28], u'軽巡ヘ級ｅ':[32, 26],
         u'軽巡ホ級':[15, 15], u'駆逐ロ級ｅ':[14, 30], u'駆逐ハ級ｅ':[16, 35], u'軽巡ホ級Ｆ':[36, 44],
         u'駆逐イ級ｅ':[12, 30], u'軽巡ホ級ｅ':[30, 24], u'潜水カ級ｅ':[27, 5], u'駆逐ハ級Ｆ':[47, 54],
         u'軽母ヌ級ｅ':[70, 10], u'空母ヲ級Ｆ':[96, 45], u'戦艦タ級Ｆ':[90, 55], u'戦艦ル級Ｆ':[98, 40],
         u'輸送ワ級Ｆ':[130, 10]}

def getEvasion(name):
    fixed_name = name.split("/")[0]
    if fixed_name in SHIPS:
        return SHIPS[fixed_name][1]
    else:
        if '級' in name:
            print "Missing %s" % fixed_name
        return 0
    
def getArmor(name):
    fixed_name = name.split("/")[0]
    if fixed_name in SHIPS:
        return SHIPS[fixed_name][0]
    else:
        if '級' in name:
            #print "Missing %s" % fixed_name
            pass
        return 0
