# -*- coding: utf-8 -*-
p = 'G:/mingli-site/make_guoxia_tu.py'
s = open(p, encoding='utf-8').read()
pairs = [
 ('label(470, 545, "过峡"', 'label(600, 545, "过峡"'),
 ('dashed((620, 770), (590, 610), LEAD)', 'dashed((620, 770), (640, 610), LEAD)'),
 ('label(690, 640, "蜂腰"', 'label(700, 600, "蜂腰"'),
 ('label(860, 700, "鹤膝"', 'label(905, 715, "鹤膝"'),
 ('label(370, 852, "护砂"', 'label(455, 855, "护砂"'),
 ('dashed((520, 842), (450, 855), LEAD)', 'dashed((520, 845), (500, 852), LEAD)'),
 ('''label(1200, 830, "水须绕行", "水从峡外绕，忌直冲峡口", anchor="rt")
d.arc([(700) * S, (855) * S, (1060) * S, (945) * S], 40, 140, fill=WATER, width=3 * S)
dashed((1000, 880), (1100, 858), WATER)''',
  '''label(1235, 870, "水须绕行", "水从峡外绕，忌直冲峡口", anchor="rt")
dashed((950, 866), (1090, 880), WATER)'''),
]
for a, b in pairs:
    assert a in s, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
