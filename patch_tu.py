# -*- coding: utf-8 -*-
p = 'G:/mingli-site/make_longxue_tu.py'
s = open(p, encoding='utf-8').read()

old = '''    pw = max(tw, sw)
    if plate:
        pad = 14
        d.rounded_rectangle([(x0 - pad - (26 if num else 0)) * S, (y0 - 10) * S,
                             (x0 + pw + pad) * S, (y0 + (52 if sub else 34)) * S],
                            radius=10 * S, fill="#FAF7EE", outline="#E3DCC9", width=2 * S)'''
new = '''    pw = max(tw, sw)
    if plate:
        pad = 14
        nw = 26 if num else 0
        if anchor == "rt":
            bx0 = x - pw - pad - nw
            bx1 = x + pad
        elif anchor == "ct":
            bx0 = x - pw / 2 - pad
            bx1 = x + pw / 2 + pad
        else:
            bx0 = x0 - pad - nw
            bx1 = x0 + pw + pad
        d.rounded_rectangle([bx0 * S, (y0 - 10) * S, bx1 * S, (y0 + (52 if sub else 34)) * S],
                            radius=10 * S, fill="#FAF7EE", outline="#E3DCC9", width=2 * S)'''
assert old in s
s = s.replace(old, new)
s = s.replace('label(1880, 470, "朝山"', 'label(1862, 468, "朝山"')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
