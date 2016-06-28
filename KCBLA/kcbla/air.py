# -*- coding: utf-8 -*-
from sre_parse import isdigit

SEIKU = [ '互角', '優勢', '確保', '劣勢', '喪失' ]

class Air:
    def __init__(self, doc):
        if doc.find('.//Stage1Flag').text == '1':
#             hit = False
#             for name in doc.findall('.//Ship/Name'):
#                 if name.text == '鳳翔改':
#                     hit = True
#                     break
#             if hit:
            self.stage1 = Stage1(doc)
            self.stage2 = Stage2(doc)

class Stage1:
    def __init__(self, doc):
        seiku = doc.find('.//Stage1Seiku').text
        if isdigit(seiku):
            self.seiku = SEIKU[int(seiku)]
        else:
            self.seiku = seiku
        self.fcount = int(doc.find('.//Stage1FCount').text)
        self.lost = int(doc.find('.//Stage1FLostCount').text)
        self.ecount = int(doc.find('.//Stage1ECount').text)
        self.elost = int(doc.find('.//Stage1ELostCount').text)

class Stage2:
    def __init__(self, doc):
        self.fcount = int(doc.find('.//Stage2FCount').text)
        self.lost = int(doc.find('.//Stage2FLostCount').text)

