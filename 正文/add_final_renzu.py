#!/usr/bin/env python3
import os
import re
from pathlib import Path

# 人祖传语录库
RENZU_QUOTES = [
    ("第一百零一则", "永生者，孤也。孤者，独也。独者，强者之姿。强者不群，不群者胜。"),
    ("第一百零二则", "轮回者，转也转者，变也。变者，通也。通者，达也。达者，不迷。"),
    ("第一百零三则", "生命者，火也。火者，燃也。燃者，灭也。灭者，重生。重生者，轮回。"),
    ("第一百零四则", "平凡者，福也。福者，安也。安者，乐也。乐者，知足。知足者，常乐。"),
    ("第一百零五则", "记忆者，痕也。痕者，印也。印者，不灭。不灭者，魂。魂者，永存。"),
    ("第一百零六则", "因果者，环也。环者，连也。连者，接也接者，不断。不断者，轮回。"),
    ("第一百零七则", "天地者，炉也。炼者，蛊也。蛊者，我也。我炼天地，天地炼我。"),
    ("第一百零八则", "守望者，念也。念者，记也。记者，不忘。不忘者，永恒。永恒者，永生。"),
    ("第一百零九则", "修行者，路也。路者，悟也。悟者，通也。通者，明也。明者，见道。"),
    ("第一百一十则", "力量者，根也。根者，本也。本者，命也。命者，争也。争者，胜也。"),
    ("第一百一十一则", "智慧者，灯也。灯者，照也。照者，明也。明者，不惑。不惑者，智。"),
    ("第一百一十二则", "永生者，终点也。终点者，始点也。始点者，轮回。轮回者，无终。"),
]

chapter_files = list(Path('.').glob('*.md'))

for f in sorted(chapter_files):
    content = f.read_text(encoding='utf-8')
    
    # 检查是否已有人祖传
    if re.search(r'人祖传', content):
        continue
    
    # 提取章节号
    match = re.match(r'第(\d+)[章节]', f.stem)
    if not match:
        continue
    
    chapter_num = int(match.group(1))
    
    # 检查是否在需要处理的列表中
    missing_chapters = [117, 119, 120, 121, 122, 123, 125, 171, 172, 173, 174, 175, 178, 179, 180, 181, 182, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]
    if chapter_num not in missing_chapters:
        continue
    
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
            insert_pos = i + 1
            break
    
    if insert_pos:
        lines.insert(insert_pos, renzu_block)
        new_content = '\n'.join(lines)
        f.write_text(new_content, encoding='utf-8')
        print(f"Added renzu to chapter {chapter_num}")

print("Done!")
