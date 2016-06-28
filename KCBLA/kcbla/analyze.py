# -*- coding: utf-8 -*-

import os, sys
from kcbla.air import Air
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
import codecs
from dircache import listdir
from genericpath import isfile
import math
from ntpath import join
from xml.etree import ElementTree

from kcbla.battle import Battle, Attack, ACTorpedo, ACBomb
from kcbla.data import getEvasion

PRINT_THRESHOLD = 1
FORMATIONS = [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']

battles = []

pow0s = [u'瑞雲',u'甲標的','empty',u'ドラム缶(輸送用)',u'61cm四連装魚雷',u'三式爆雷投射機',u'三式水中探信儀',u'25mm連装機銃'
         ,u'61cm三連装魚雷',u'零式水上偵察機',u'61cm四連装(酸素)魚雷',u'瑞雲(六三四空)',u'改良型艦本式タービン',u'32号対水上電探'
         ,u'61cm五連装(酸素)魚雷']
pow1s = [u'12cm単装砲']
pow2s = [u'10cm連装高角砲', u'12.7cm連装砲',u'14cm単装砲',u'12.7cm連装高角砲(後期型)']
pow3s = [u'12.7cm連装砲B型改二',u'10cm連装高角砲+高射装置']
pow4s = [u'15.2cm連装砲']
outs = [u'流星改',u'流星',u'5inch単装砲',u'深海棲艦偵察機',u'5inch単装砲',u'5inch単装高射砲',u'5inch連装砲'
        ,u'12.7cm連装高角砲',u'20.3cm連装砲',u'15.5cm三連装砲','21inch魚雷前期型',u'烈風',u'彗星一二型甲',u'彩雲'
        ,u'零式艦戦62型(爆戦)',u'15.5cm三連装副砲',u'8cm高角砲']

def main():
    data = {}        
    dir_path = "D:\KCBLA-Data"
    xml_files = [ f for f in listdir(dir_path) if isfile(join(dir_path, f)) ]
    for fname in xml_files:
        index = xml_files.index(fname)
        if index % 5000 == 0:
            print "%d/%d\r" % (index, len(xml_files)),
#             pass
        if not fname.endswith('xml'):
            continue
        
        # Extra conditions
        if not '2-2-4' in fname and not '2-2-6' in fname:
            continue
        
        fpath = dir_path + "\\" + fname
#         stage = fpath.split(' ')[1][0:3]
        doc = ElementTree.parse(fpath)
        try:
            battle = Battle(doc)
            if len(battle.bbPhase.attacks) > 0:
                attack = battle.bbPhase.attacks[0]
                if attack.target == u'輸送ワ級':
                    if attack.damage == 0:
                        continue
                    pow = int(doc.find('.//Value').text)
                    eq = ''
                    legal = True
                    c = 0
                    for v in doc.findall('.//ShipKF/Ship/SlotItem/Name'):
                        c += 1
                        if c == 4:
                            break
                        eq += v.text + ' '
                        if v.text in outs:
                            legal = False
                            break
                        elif v.text in pow1s:
                            pow += 1
                        elif v.text in pow2s:
                            pow += 2
                        elif v.text in pow3s:
                            pow += 3
                        elif v.text in pow4s:
                            pow += 4
                        elif v.text in pow0s or v.text is None:
                            pow += 0
                        else:
                            print v.text
                    if pow < 70 and legal:
                        apow = pow + 5
                        cri = ''
                        if battle.encount == u'反航戦':
                            apow = apow * 4 / 5
                        elif battle.encount == u'Ｔ有利':
                            apow = apow * 6 / 5
                        elif battle.encount == u'Ｔ不利':
                            apow = apow * 3 / 5
                        if apow < attack.damage:
                            apow = apow * 3 / 2
                            cri = 'Cri'
                        arm = apow - attack.damage
                        print '%d - %s %d->%d %d %s %s %s %s' % \
                            (arm, attack.attacker, pow, apow, attack.damage, battle.encount, eq, cri, fname)
                        if not arm in data:
                            data[arm] = 0
                        data[arm] += 1
        except AttributeError:
            continue

#         try:
#             air = Air(doc)
#         except AttributeError:
#             continue
#         if hasattr(air, 'stage1'):
#             if not air.stage1.seiku in data:
#                 data[air.stage1.seiku] = []
#             data[air.stage1.seiku].append(air.stage1.elost)

#             print '%s,%d,%d,(%s)' % (air.stage1.seiku, air.stage1.ecount, air.stage1.elost, fname)
#         for a in battle.stage3.attacks:
#             if a.flags & Attack.OUTLET == Attack.OUTLET:
#                 print fname
#         battles.append(battle)
        
#         ec = battle.encount
#         if not ec in data:
#             data[ec] = {}
#         for at in battle.opening.attacks + battle.tpdPhase.attacks:
#             if at.flags == 0:
#                 continue
#             if not u'駆逐' in at.target:
#                 continue
#             if not at.target in data[ec]:
#                 data[ec][at.target] = {}
#                 data[ec][at.target][1] = { 'min': 9999, 'max': -9999, 'count': 0 }
#                 data[ec][at.target][3] = { 'min': 9999, 'max': -9999, 'count': 0 }
#             sto = data[ec][at.target][at.flags]
#             if at.dmg > sto['max']:
#                 sto['max'] = at.dmg
#             if at.dmg < sto['min']:
#                 sto['min'] = at.dmg
#             sto['count'] += 1
#             
#     for enc in [u'同航戦', u'反航戦', u'Ｔ有利', u'Ｔ不利' ]:
#         print '--- %s ---' % enc
#         for target in data[enc]:
#             d = data[enc][target]
#             print target
#             print "　通常 %d 回 %d～%d\n　急所 %d 回 %d～%d" % (d[1]['count'], d[1]['min'], d[1]['max'],
#                                                    d[3]['count'], d[3]['min'], d[3]['max'])
#     for k, v in sorted(total.items(), key=lambda x:x[1]):
#         for stage in res[k]:
#             print '%s %d %s' % (k, res[k][stage], stage)
#     for k, v in sorted(total.items(), key=lambda x:x[1]):
        
#     for k in data:
#         min = 999
#         max = -1
#         total = 0
#         size = len(data[k])
#         for v in data[k]:
#             if v < min:
#                 min = v
#             if v > max:
#                 max = v
#             total += v
# #             print v
#         mean = total / size
#         variancettl = 0
#         for v in data[k]:
#             variancettl += (v - mean) * (v - mean)
#         variance = variancettl / size
#         
#         print '%s' % k
#         print 'Total: %d' % size
#         print 'Min: %d' % min
#         print 'Max: %d' % max
#         print 'Mean: %d' % mean
#         print 'SD: %d' % math.sqrt(variance)
#         print 
               
#     out = codecs.open("..\output.html", "w", "utf-8-sig")
#     out.write('''
#     <html><head><style type="text/css">
#         table { border: solid 1px; }
#         th { padding: 2px; border: solid 1px; }
#         td { padding: 2px; border: solid 1px; text-align: center; }
#         .hit { background-color: #E0FFE0; }
#         .miss { background-color: #FFE0E0; }
#         .blue { background-color: #E0E0FF; }
#     </style></head><body>
#     ''')
#     output(out)
#     out.write('</body></html>')
#     out.close()
#     
    
    for k in data:
        print '%d\t%d' % (k, data[k])    
    
    print "Done."
    
def output(out):
#     writeStage3(out)
#     writeOpeningAttacks(out)
    writeEnemyOpeningAttacks(out)
    writeBombards(out)
    writeTorpedos(out)
#     writeTorpedoed(out)
#     statOpeningAttacks(out)

def writeStage3(out):
    out.write('<h1>航空戦集計</h1>')
    
    t_total = 0
    t_miss = 0
    t_normal = 0
    t_fatal = 0
    t_critical = 0
    t_fatal_critical = 0
    b_total = 0
    b_miss = 0
    b_normal = 0
    b_critical = 0
    o_hit = {}
    o_miss = {}
    
    torpedoHit = {}
    bombHit = {}

    for b in battles:
        if not b.extraCond: continue
        for a in b.stage3.attacks:
            df = a.target
            if isinstance(a, (ACTorpedo)):
                if not df in torpedoHit:
                    torpedoHit[df] = {'total':0}
                    for i in range(0, 0x10):
                        torpedoHit[df][i] = 0
                torpedoHit[df]['total'] += 1
                torpedoHit[df][a.flags] += 1
            elif isinstance(a, (ACBomb)):
                if not df in bombHit:
                    bombHit[df] = {'total':0}
                    for i in range(0, 0x10):
                        bombHit[df][i] = 0
                if a.flags & Attack.BOTH_HIT == Attack.BOTH_HIT:
                    bombHit[df]['total'] += 2
                    a.flags &= 0xFF8F
                    a.flags |= Attack.HIT
                    bombHit[df][a.flags] += 2
                elif a.flags & Attack.HALF_HIT == Attack.HALF_HIT:
                    bombHit[df]['total'] += 2
                    a.flags &= 0xFF8F
                    a.flags |= Attack.HIT
                    bombHit[df][a.flags] += 1
                    bombHit[df][0] += 1
                elif a.flags & Attack.BOTH_MISS == Attack.BOTH_MISS:
                    bombHit[df]['total'] += 2
                    bombHit[df][0] += 2
                else:
                    bombHit[df]['total'] += 1
                    bombHit[df][a.flags] += 1
                    
    for target in sorted(torpedoHit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
        total = torpedoHit[target]['total']
        miss = torpedoHit[target][0]
        normal = torpedoHit[target][Attack.HIT]
        fatal = torpedoHit[target][Attack.FATAL | Attack.HIT]
        critical = torpedoHit[target][Attack.CRTIICAL | Attack.HIT]
        fatal_critical = torpedoHit[target][Attack.FATAL | Attack.CRTIICAL | Attack.HIT]
        t_total += total
        t_miss += miss
        t_normal += normal
        t_fatal += fatal
        t_critical += critical
        t_fatal_critical += fatal_critical
        hit = normal + fatal + critical + fatal_critical
        o_hit[target] = hit
        o_miss[target] = miss
    
    for target in sorted(bombHit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
        total = bombHit[target]['total']
        miss = bombHit[target][0]
        normal = bombHit[target][Attack.HIT]
        critical = bombHit[target][Attack.CRTIICAL | Attack.HIT]
        b_total += total
        b_miss += miss
        b_normal += normal
        b_critical += critical
        if not target in o_hit:
            o_hit[target] = 0
        if not target in o_miss:
            o_miss[target] = 0
        o_hit[target] += critical + normal
        o_miss[target] += miss

    out.write('<h2>攻撃別</h2>')
    out.write('<table>')
    out.write('<tr><th>攻撃種類</th><th class="blue">総数</th><th class="hit">命中</th><th class="miss">ミス</th><th class="blue">命中率</th><th>貫通弾</th><th>貫通率</th><th>急所弾</th><th>急所率</th></tr>')
    t_hit = t_normal + t_fatal + t_critical + t_fatal_critical
    t_fatal_rate = 0
    t_critical_rate = 0
    t_rate = 0
    if t_total > 0:
        t_rate = 100 * t_hit / t_total
    b_hit = b_normal + b_critical
    b_rate = 0
    if b_total > 0:
        b_rate = 100 * b_hit / b_total
    b_critical_rate = 0
    if t_hit > 0:
        t_fatal_rate = 100 * (t_fatal + t_fatal_critical) / t_hit
        t_critical_rate = 100 * (t_critical + t_fatal_critical) / t_hit
    if b_hit > 0:
        b_critical_rate = 100 * b_critical / b_hit
    out.write('<tr><td>雷撃</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d</td><td>%d%%</td><td>%d</td><td>%d%%</td></tr>' % \
        (t_total, t_hit, t_miss, t_rate, \
         t_critical + t_fatal_critical, t_critical_rate, t_fatal + t_fatal_critical, t_fatal_rate))
    out.write('<tr><td>爆撃</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d</td><td>%d%%</td><td>-</td><td>-</td></tr>' % \
        (b_total, b_hit, b_miss, b_rate, b_critical, b_critical_rate))
    out.write('</table>')
    
    cal = 40
    out.write('<h2>目標別</h2>')
    out.write('<table>')
    out.write('<tr><th>目標</th><th>回避値</th><th class="blue">総数</th><th class="hit">命中</th><th class="miss">ミス</th><th class="blue">命中率</th><th>95%区間</th><th>推定命中</th></tr>')
    for target in sorted(o_hit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
        o_total = o_hit[target] + o_miss[target]
        if o_total < PRINT_THRESHOLD: continue
        rate = (100 * o_hit[target] / o_total)
        delta = 192 * math.sqrt((rate / 100.0) * (1 - rate / 100.0) / o_total)
        out.write('<tr><td>%s</td><td>%d</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d%%～%d%%</td><td>%d%%</td></tr>' % \
            (target, getEvasion(target), o_total, o_hit[target], o_miss[target], rate, rate - delta, rate + delta, 100 * cal / (cal + getEvasion(target))))
    out.write('</table>')
    
def statOpeningAttacks(out):
    out.write('<h1>先制雷撃分析</h1>')
    otmaps = {}
    for enc in {u'同航戦':{}, u'反航戦':{}, u'Ｔ有利':{}, u'Ｔ不利':{}}:
        otmaps[enc] = {u'単縦':{}, u'複縦':{}, u'輪形':{}, u'梯形':{}, u'単横':{}}
    for b in battles:
        af = b.ff
        enc = b.encount
        for a in b.e_opening.attacks:
            dmg = a.dmg
            if not dmg in otmaps[enc][af]:
                otmaps[enc][af][dmg] = 0
            otmaps[enc][af][dmg] += 1
    for enc in [u'同航戦', u'反航戦', u'Ｔ有利', u'Ｔ不利']:
        t = {}
        out.write('<h2>%s</h2>' % enc)
        print'<h2>%s</h2>' % enc
        for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
            out.write('<table>')
            out.write('<tr><td>ダメージ</td><td>回数</td></tr>')
            out.write('<h3>%s陣</h3>' % ff)
            print '<h3>%s陣</h3>' % ff
            for dmg in otmaps[enc][ff]:
                out.write('<tr><td>%d</td><td>%d</td></tr>' % (dmg , otmaps[enc][ff][dmg]))
                print '%d %d' % (dmg , otmaps[enc][ff][dmg])
                if not dmg in t:
                    t[dmg] = 0
                t[dmg] += otmaps[enc][ff][dmg]
            out.write('</table>')
        print '総合'
        for dmg in t:
            print '%d %d' % (dmg, t[dmg])

def writeEnemyOpeningAttacks(out):
    out.write('<h1>先制雷撃集計</h1>')
    otmaps = {u'単縦':{}, u'複縦':{}, u'輪形':{}, u'梯形':{}, u'単横':{}}
    for b in battles:
        af = b.ff
        for a in b.e_opening.attacks:
            df = a.target
            if not df in otmaps[af]:
                otmaps[af][df] = {'total':0}
                for i in range(0, 0x10):
                    otmaps[af][df][i] = 0
            otmaps[af][df]['total'] += 1
            otmaps[af][df][a.flags] += 1
    
    for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
        a_total = 0
        a_miss = 0
        a_normal = 0
        a_critical = 0
        o_hit = {}
        o_miss = {}
        o_critical = {}
        otmap = otmaps[ff]
        if otmap == {}: continue
        for target in sorted(otmap, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            # Extra conditions
#             if getEvasion(target) < 45: continue
            total = otmap[target]['total']
            miss = otmap[target][0]
            normal = otmap[target][Attack.HIT]
            critical = otmap[target][Attack.CRTIICAL | Attack.HIT]
            a_total += total
            a_miss += miss
            a_normal += normal
            a_critical += critical
            if not target in o_hit:
                o_hit[target] = 0
            if not target in o_miss:
                o_miss[target] = 0
            if not target in o_critical:
                o_critical[target] = 0
            o_hit[target] += critical + normal
            o_miss[target] += miss
            o_critical[target] += critical
        
        out.write('<h2>%s陣</h2>' % ff)
        out.write('<table>')
        out.write('<tr><th>目標</th><th>回避値</th><th class="blue">総数</th><th class="hit">命中</th><th class="miss">ミス</th><th class="blue">命中率</th><th>95%区間</th><th>貫通弾</th></tr>')
        for target in sorted(o_hit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            o_total = o_hit[target] + o_miss[target]
            if o_total < PRINT_THRESHOLD: continue
            o_rate = (100 * o_hit[target] / o_total)
            o_delta = 192 * math.sqrt((o_rate / 100.0) * (1 - o_rate / 100.0) / o_total)
            out.write('<tr><td>%s</td><td>%d</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d%%～%d%%</td><td>%d</td></tr>' % \
                (target, getEvasion(target), o_total, o_hit[target], o_miss[target], o_rate, o_rate - o_delta, o_rate + o_delta, o_critical[target]))
        if a_total > 0:
            a_hit = a_normal + a_critical
            a_rate = 100 * a_hit / a_total
            out.write('<tr><td>総計</td><td>-</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>-</td></tr>' % \
                (a_total, a_hit, a_miss, a_rate))
        out.write('</table>')
    
def writeOpeningAttacks(out):
    out.write('<h1>先制雷撃集計</h1>')
    otmaps = {u'単縦':{}, u'複縦':{}, u'輪形':{}, u'梯形':{}, u'単横':{}}
    for b in battles:
        for a in b.opening.attacks:
            df = a.target
            if not df in otmaps[b.ff]:
                otmaps[b.ff][df] = {'total':0}
                for i in range(0, 0x10):
                    otmaps[b.ff][df][i] = 0
            otmaps[b.ff][df]['total'] += 1
            otmaps[b.ff][df][a.flags] += 1
    
    for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
        a_total = 0
        a_miss = 0
        a_normal = 0
        a_critical = 0
        o_hit = {}
        o_miss = {}
        o_critical = {}
        otmap = otmaps[ff]
        if otmap == {}: continue
        for target in sorted(otmap, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            # Extra conditions
#             if getEvasion(target) < 45: continue
            total = otmap[target]['total']
            miss = otmap[target][0]
            normal = otmap[target][Attack.HIT]
            critical = otmap[target][Attack.CRTIICAL | Attack.HIT]
            a_total += total
            a_miss += miss
            a_normal += normal
            a_critical += critical
            if not target in o_hit:
                o_hit[target] = 0
            if not target in o_miss:
                o_miss[target] = 0
            if not target in o_critical:
                o_critical[target] = 0
            o_hit[target] += critical + normal
            o_miss[target] += miss
            o_critical[target] += critical
        
        out.write('<h2>%s陣</h2>' % ff)
        out.write('<table>')
        out.write('<tr><th>目標</th><th>回避値</th><th class="blue">総数</th><th class="hit">命中</th><th class="miss">ミス</th><th class="blue">命中率</th><th>95%区間</th><th>貫通</th><th>貫通率</th></tr>')
        for target in sorted(o_hit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            o_total = o_hit[target] + o_miss[target]
            if o_total < PRINT_THRESHOLD: continue
            o_rate = 100 * o_hit[target] / o_total
            o_critical_rate = 0
            if o_hit[target] > 0:
                o_critical_rate = 100 * o_critical[target] / o_hit[target]
            o_delta = 192 * math.sqrt((o_rate / 100.0) * (1 - o_rate / 100.0) / o_total)
            out.write('<tr><td>%s</td><td>%d</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d%%～%d%%</td><td>%d</td><td>%d%%</td></tr>' % \
                (target, getEvasion(target), o_total, o_hit[target], o_miss[target], o_rate, o_rate - o_delta, o_rate + o_delta, o_critical[target], o_critical_rate))
        if a_total > 0:
            a_hit = a_normal + a_critical
            a_rate = 100 * a_hit / a_total
            a_critical_rate = 100 * a_critical / a_hit
            out.write('<tr><td>総計</td><td>-</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>-</td><td>%d</td><td>%d%%</td></tr>' % \
                (a_total, a_hit, a_miss, a_rate, a_critical, a_critical_rate))
        out.write('</table>')

def writeBombards(out):
    dt = {}
    for b in battles:
        ff = b.ff
        enc = b.encount
        key = '%s・%s' % (ff, enc)
        if not key in dt:
            dt[key] = {}
        for a in b.bbPhase.attacks:
            if not a.attacker == u'大井改二':
                continue
            if a.flags | Attack.CRTIICAL == Attack.CRTIICAL:
                continue
            if not a.damage in dt[key]:
                dt[key][a.damage] = 0
            dt[key][a.damage] += 1
    for st in dt:
        print st
        for dmg in sorted(dt[st], lambda x, y : x - y):
            bar = ''
            for i in range(dt[st][dmg]):
                bar = bar + '|'
            print '%d: %s' % (dmg, bar)
    
    out.write('<h1>砲撃戦集計</h1>')
    dataMap = {u'単縦':{}, u'複縦':{}, u'輪形':{}, u'梯形':{}, u'単横':{}}
    for battle in battles:
        dm1 = dataMap[battle.ff]
        for attack in battle.bbPhase.attacks:
            attacker = battle.attackers[attack.atIndex]
            target = attack.target
            if not attacker in dm1:
                dm1[attacker] = {}
            dm2 = dm1[attacker]
            if not target in dm2:
                dm2[target] = { 'total': 0, 0: 0, 1: 0, 2: 0, 3: 0 }
            dm3 = dm2[target]
            dm3['total'] += 1
            if not attack.flags in dm3:
                dm3[attack.flags] = 0
            dm3[attack.flags] += 1
           
    ffs = {u'単縦':[0, 0, 0], u'複縦':[0, 0, 0], u'輪形':[0, 0, 0], u'梯形':[0, 0, 0], u'単横':[0, 0, 0]}
    for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
        dm1 = dataMap[ff]
        if dm1 == {}: continue
        out.write('<h2>%s陣</h2>' % ff)
        attackers = []
        for attacker in dm1:
            attackers.append(attacker)
        for attacker in sorted(attackers, lambda x, y: 1 if x.toString() > y.toString() else -1):
            dm2 = dm1[attacker]
            # Extra conditions
#             if not attacker.toString()[0:2] in ['瑞鶴', '摩耶', '武蔵', '鳥海', '島風', '雪風'
#                                            ]: continue
            atstat = [0, 0, 0]
            eva_sum = 0
            eva_count = 0
            attacker_color = 'red' if '電探' in attacker.toString() else 'black'
            out.write('<h3><font color="%s">攻撃者：%s</font></h3>' % (attacker_color, attacker.toString()))
            out.write('<table>')
            out.write('''<tr><th>目標</th><th>回避値</th><th class="blue">総数</th>
            <th class="hit">命中</th><th class="miss">ミス</th>
            <th class="blue">命中率</th><th>95%区間</th><th>貫通弾</th><th>貫通率</th></tr>''')
            for target in sorted(dm2, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
                # Extra conditions
#                 if getEvasion(target) < 45: continue
                total = dm2[target]['total']
                miss = dm2[target][0]
                normal = dm2[target][Attack.HIT]
                cl = dm2[target][Attack.CRTIICAL | Attack.HIT]
                hit = cl + normal
                atstat[0] += hit
                atstat[1] += miss
                atstat[2] += cl
                if total < PRINT_THRESHOLD: continue
                rate = 100 * hit / total
                delta = 192 * math.sqrt((rate / 100.0) * (1 - rate / 100.0) / total)
                clrate = 0
                if hit > 0:
                    clrate = 100 * cl / hit
                eva_sum += getEvasion(target)
                eva_count += 1
                out.write('''<tr><td>%s</td><td>%d</td><td class="blue">%d</td>
                <td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td>
                <td>%d%%～%d%%</td><td>%d</td><td>%d%%</td></tr>''' 
                   % (target, getEvasion(target), total, hit, miss, \
                      rate, rate - delta, rate + delta, cl, clrate))
            at_clrate = 0
            if atstat[0] > 0:
                at_clrate = 100 * atstat[2] / atstat[0]
            ffs[ff][0] += atstat[0]
            
            ffs[ff][1] += atstat[1]
            ffs[ff][2] += atstat[2]
            out.write('''<tr><td>総計</td><td>%.1f</td><td class="blue">%d</td>
                <td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td>
                <td>-</td><td>%d</td><td>%d%%</td></tr>''' 
                   % (1.0 * eva_sum / eva_count, atstat[0] + atstat[1], atstat[0], atstat[1], \
                      100 * atstat[0] / (atstat[0] + atstat[1]), atstat[2], at_clrate))
            out.write('</table>')
    out.write('<h2>陣形総計</h2>')
    out.write('<table>')
    out.write('''<tr><th>陣形</th><th class="blue">総数</th>
    <th class="hit">命中</th><th class="miss">ミス</th>
    <th class="blue">命中率</th><th>貫通弾</th><th>貫通率</th></tr>''')
    for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
        ff_hit = ffs[ff][0]
        ff_miss = ffs[ff][1]
        ff_total = ff_hit + ff_miss
        ff_cl = ffs[ff][2]
        ff_rate = 0
        if ff_total > 0:
            ff_rate = 100 * ff_hit / ff_total
        ff_clrate = 0
        if ff_hit > 0:
            ff_clrate = 100 * ff_cl / ff_hit
        out.write('''<tr><td>%s</td><td class="blue">%d</td><td class="hit">%d</td>
        <td class="miss">%d</td><td class="blue">%d%%</td><td>%d</td><td>%d%%</td></tr>'''
            % (ff, ff_total, ff_hit, ff_miss, ff_rate, ff_cl, ff_clrate))
    out.write('</table>')

def writeTorpedos(out):
    out.write('<h1>雷撃集計</h1>')
    otmaps = {u'単縦':{}, u'複縦':{}, u'輪形':{}, u'梯形':{}, u'単横':{}}
    for b in battles:
        af = b.ff
        for a in b.tpdPhase.attacks:
            df = a.target
            if not df in otmaps[af]:
                otmaps[af][df] = {'total':0}
                for i in range(0, 0x10):
                    otmaps[af][df][i] = 0
            otmaps[af][df]['total'] += 1
            otmaps[af][df][a.flags] += 1
    
    for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
        a_total = 0
        a_miss = 0
        a_normal = 0
        a_critical = 0
        o_hit = {}
        o_miss = {}
        o_critical = {}
        otmap = otmaps[ff]
        if otmap == {}: continue
        for target in sorted(otmap, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            # Extra conditions
#             if getEvasion(target) < 45: continue
            total = otmap[target]['total']
            miss = otmap[target][0]
            normal = otmap[target][Attack.HIT]
            critical = otmap[target][Attack.CRTIICAL | Attack.HIT]
            a_total += total
            a_miss += miss
            a_normal += normal
            a_critical += critical
            if not target in o_hit:
                o_hit[target] = 0
            if not target in o_miss:
                o_miss[target] = 0
            if not target in o_critical:
                o_critical[target] = 0
            o_hit[target] += critical + normal
            o_miss[target] += miss
            o_critical[target] += critical
        
        out.write('<h2>%s陣</h2>' % ff)
        out.write('<table>')
        out.write('<tr><th>目標</th><th>回避値</th><th class="blue">総数</th><th class="hit">命中</th><th class="miss">ミス</th><th class="blue">命中率</th><th>95%区間</th><th>貫通</th><th>貫通率</th></tr>')
        for target in sorted(o_hit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            o_total = o_hit[target] + o_miss[target]
            if o_total < PRINT_THRESHOLD: continue
            o_rate = 100 * o_hit[target] / o_total
            o_critical_rate = 0
            if o_hit[target] > 0:
                o_critical_rate = 100 * o_critical[target] / o_hit[target]
            o_delta = 192 * math.sqrt((o_rate / 100.0) * (1 - o_rate / 100.0) / o_total)
            out.write('<tr><td>%s</td><td>%d</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d%%～%d%%</td><td>%d</td><td>%d%%</td></tr>' % \
                (target, getEvasion(target), o_total, o_hit[target], o_miss[target], o_rate, o_rate - o_delta, o_rate + o_delta, o_critical[target], o_critical_rate))
        if a_total > 0:
            a_hit = a_normal + a_critical
            a_rate = 100 * a_hit / a_total
            a_critical_rate = 100 * a_critical / a_hit
            out.write('<tr><td>総計</td><td>-</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>-</td><td>%d</td><td>%d%%</td></tr>' % \
                (a_total, a_hit, a_miss, a_rate, a_critical, a_critical_rate))
        out.write('</table>')


def writeTorpedoed(out):
    out.write('<h1>雷撃総集計</h1>')
    otmaps = {u'単縦':{}, u'複縦':{}, u'輪形':{}, u'梯形':{}, u'単横':{}}
    for b in battles:
        af = b.ff
        for a in b.e_opening.attacks:
            df = a.target
            if not df in otmaps[af]:
                otmaps[af][df] = {'total':0}
                for i in range(0, 0x10):
                    otmaps[af][df][i] = 0
            otmaps[af][df]['total'] += 1
            otmaps[af][df][a.flags] += 1
        for a in b.tpdPhase.attacks:
            df = a.target
            if not df in otmaps[af]:
                otmaps[af][df] = {'total':0}
                for i in range(0, 0x10):
                    otmaps[af][df][i] = 0
            otmaps[af][df]['total'] += 1
            otmaps[af][df][a.flags] += 1
    
    out.write('<table>')
    out.write('<tr><th>目標</th><th class="blue">総数</th><th class="hit">命中</th><th class="miss">ミス</th><th class="blue">命中率</th><th>95%区間</th></tr>')
    for ff in [u'単縦', u'複縦', u'輪形', u'梯形', u'単横']:
        a_total = 0
        a_miss = 0
        a_normal = 0
        a_critical = 0
        o_hit = {}
        o_miss = {}
        otmap = otmaps[ff]
        if otmap == {}: continue
        for target in sorted(otmap, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            # Extra conditions
#             if getEvasion(target) < 45: continue
            total = otmap[target]['total']
            miss = otmap[target][0]
            normal = otmap[target][Attack.HIT]
            critical = otmap[target][Attack.CRTIICAL | Attack.HIT]
            a_total += total
            a_miss += miss
            a_normal += normal
            a_critical += critical
            if not target in o_hit:
                o_hit[target] = 0
            if not target in o_miss:
                o_miss[target] = 0
            o_hit[target] += critical + normal
            o_miss[target] += miss
        
        for target in sorted(o_hit, lambda x, y: getEvasion(x) - getEvasion(y), reverse=True):
            o_total = o_hit[target] + o_miss[target]
            if o_total < PRINT_THRESHOLD: continue
            o_rate = (100 * o_hit[target] / o_total)
            o_delta = 192 * math.sqrt((o_rate / 100.0) * (1 - o_rate / 100.0) / o_total)
            out.write('<tr><td>%s陣</td><td class="blue">%d</td><td class="hit">%d</td><td class="miss">%d</td><td class="blue">%d%%</td><td>%d%%～%d%%</td></tr>' % \
                (ff, o_total, o_hit[target], o_miss[target], o_rate, o_rate - o_delta, o_rate + o_delta))
    out.write('</table>')
    
main()
