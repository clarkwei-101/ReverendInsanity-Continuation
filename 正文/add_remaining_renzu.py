#!/usr/bin/env python3
import os
import re
from pathlib import Path

# 更多人祖传语录
RENZU_QUOTES = [
    ("第八十六则", "凡间者，戏也。戏者，演也。演者，假也。假中有真，真中有假。永生者看戏，戏看永生。"),
    ("第八十七则", "平凡者，真也。真者，实也。实者，不虚。不虚者，道之根。"),
    ("第八十八则", "生命者，旅也。旅者，行也。行者，远也。远者，不返。不返者，归于道。"),
    ("第八十九则", "记忆者，痕也。痕者，印也。印者，刻也。刻者，不灭。不灭者，魂。"),
    ("第九十则", "转世者，生也。生者，死也。死死生生，轮回不止。轮回者，蛊之相。"),
    ("第九十一则", "守望者，念也。念者，思也。思者，记也。记者，不忘。不忘者，永恒。"),
    ("第九十二则", "膜者，界也。界者，分也。分者，别也。别者，内外。内外者，天地之隔。"),
    ("第九十三则", "守门者，职也。职者，守也。守者，护也。护者，生。生者，凡间之根。"),
    ("第九十四则", "凡窍者，空也。空者，虚也。虚者，可造。造者，炼道。炼道者，化天地。"),
    ("第九十五则", "力量者，根也。根者，本也。本者，命也。命者，夺也。夺者，胜也。"),
    ("第九十六则", "智慧者，刃也。刃者，割也。割者，分也。分者，明也。明者，知也。"),
    ("第九十七则", "因果者，线也。线者，连也。连者，牵也。牵者，绊也。绊者，困也。"),
    ("第九十八则", "轮回者，轮也。轮者，转也。转者，变也。变者，化也。化者，道也。"),
    ("第九十九则", "前世者，往也。往者，去也。去者，逝也。逝者，不返。不返者，魂仍在。"),
    ("第一百则", "永生者，终也。终者，极也。极者，顶也。顶者，观也。观者，天地在。"),
]

chapter_files = list(Path('.').glob('*.md'))
modified_count = 0

for f in sorted(chapter_files):
    content = f.read_text(encoding='utf-8')
    
    # 检查是否已有人祖传
    if '人祖传' in content:
        continue
    
    # 提取章节号
    match = re.match(r'第(\d+)[章节]', f.stem)
    if not match:
        continue
    
    chapter_num = int(match.group(1))
    
    # 分配人祖传编号（循环使用）
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
            insert_pos = i + 1
            break
    
    if insert_pos:
        lines.insert(insert_pos, renzu_block)
        new_content = '\n'.join(lines)
        f.write_text(new_content, encoding='utf-8')
        modified_count += 1

print(f"新增人祖传章节: {modified_count}")
