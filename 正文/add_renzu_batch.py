#!/usr/bin/env python3
import os
import re
from pathlib import Path

# 人祖传语录库
RENZU_QUOTES = [
    ("第六十二则", "尊者者，孤也。孤者，无伴。无伴者，天道不容。不容者，必亡。然永生者亡天，不亡己。"),
    ("第六十三则", "博弈者，谋也。谋者，算也。算者，知也。知者，胜也。胜者，蛊道之极。"),
    ("第六十四则", "牺牲者，弃也。弃者，失也。失者，得之始。然永生者不弃。不弃者，何以得？"),
    ("第六十五则", "背叛者，叛己也。己者，心也。心者，蛊之根。叛心者，名为魔。"),
    ("第六十六则", "执念者，锁也。锁者，困也。困者，不脱。不脱者，永在轮回。永生者执念，执念锁永生。"),
    ("第六十七则", "欲望者，火也。火者，焚也。焚者，自灭。自灭者，可燃天。永生者无欲，无欲者无敌。"),
    ("第六十八则", "时间者，蛊也。蛊者，命也。命者，限也。限者，可破。破者，永生。"),
    ("第六十九则", "天地者，炉也。炼者，蛊也。蛊者，我也。我炼天地，天地炼我。"),
    ("第七十则", "因果者，线也。线者，连也。连者，缚也。缚者，脱之始。永生者脱因果。"),
    ("第七十一则", "生死者，蛊也。蛊者，变也。变者，无常。无常者，常也。永生者超常。"),
    ("第七十二则", "命运者，戏也。戏者，观也。观者，悟也。悟者，破也。永生者自写戏本。"),
    ("第七十三则", "智慧者，刀也。刀者，割也。割者，分也。分者，明也。明者，不惑。"),
    ("第七十四则", "力量者，根也。根者，本也。本者，命也。命者，夺也。夺者，蛊道。"),
    ("第七十五则", "孤独者，寿也。寿者，长也。长者，久也。久者，离也。永生者离众。"),
    ("第七十六则", "意志者，钢也。钢者，硬也。硬者，不折。不折者，胜也。"),
    ("第七十七则", "修行者，路也。路者，通也。通者，达也。达者，尽也。尽者，新之始。"),
    ("第七十八则", "天道者，规也。规者，限也。限者，破也。破者，立也。立者，新规。"),
    ("第七十九则", "凡间者，戏台也。戏台者，演也。演者，虚也。虚者，实也。实者，蛊。"),
    ("第八十则", "爱情者，蛊也。蛊者，毒也。毒者，伤也。伤者，痛也。痛者，记也。记者，永恒。"),
]

chapter_files = list(Path('.').glob('*.md'))
renzu_count = 0
modified_count = 0

for f in sorted(chapter_files):
    content = f.read_text(encoding='utf-8')
    
    # 检查是否已有人祖传
    if '人祖传' in content:
        renzu_count += 1
        continue
    
    # 提取章节号
    match = re.match(r'第(\d+)[章节]', f.stem)
    if not match:
        continue
    
    chapter_num = int(match.group(1))
    
    # 分配人祖传编号
    quote_idx = (chapter_num - 1) % len(RENZU_QUOTES)
    quote_num, quote_text = RENZU_QUOTES[quote_idx]
    
    # 构造人祖传引用
    renzu_block = f"""
> **【人祖传·{quote_num}】**
> *{quote_text}*
"""
    
    # 在文档开头（第一个---之后）插入
    lines = content.split('\n')
    insert_pos = None
    for i, line in enumerate(lines):
        if line.strip() == '---':
            # 找到第一个---，在它之后插入
            insert_pos = i + 1
            break
    
    if insert_pos:
        lines.insert(insert_pos, renzu_block)
        new_content = '\n'.join(lines)
        f.write_text(new_content, encoding='utf-8')
        modified_count += 1

print(f"已有人祖传章节: {renzu_count}")
print(f"新增人祖传章节: {modified_count}")
print(f"总计: {renzu_count + modified_count}")
