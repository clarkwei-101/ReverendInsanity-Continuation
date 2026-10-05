#!/usr/bin/env python3
import re
from pathlib import Path

# 人祖传语录库
RENZU_QUOTES = [
    ("第一百零二则", "影子者，幻也。幻者，虚也虚者，不实也。不实者，可变也。可变者，通也。"),
    ("第一百零三则", "分身者，别也。别者，异也。异者，离也。离者，独也。独者，孤也。"),
    ("第一百零四则", "气者，动也。动者，变也。变者，生也。生者，活也。活着，气在。"),
    ("第一百零五则", "觉醒者，悟也。悟者，明也。明者，见也。见者，知也。知者，不惑。"),
    ("第一百零六则", "等待者，候也。候者，待也。待者，望也。望者，期也。期者，必来。"),
    ("第一百零七则", "临界者，界也。界者，分也。分者，别也。别者，择也。择者，判也。"),
    ("第一百零八则", "最后者，终也。终者，末也。末者，极也。极者，顶也。顶者，天也。"),
    ("第一百零九则", "发现者，见也。见者，知也。知者，觉也。觉者，醒也。醒者，悟也。"),
    ("第一百一十则", "推算者，谋也。谋者，算也。算者，知也。知者，预也。预者，不惑。"),
    ("第一百一十一则", "裂隙者，隙也。隙者，缝也。缝者，通也。通者，透也。透者，入也。"),
    ("第一百一十二则", "混沌者，浊也。浊者，乱也。乱者，无序也。无序者，天地之始。"),
    ("第一百一十三则", "波涛者，动也。动者，变也。变者，生也。生者，死也。生死轮回。"),
    ("第一百一十四则", "镇运者，定也。定者，安也。安者，稳也。稳者，不动也。不动者，胜。"),
    ("第一百一十五则", "前夕者，前也。前者，先也。先者，领也。领者，导也。导者，引也。"),
    ("第一百一十六则", "登场者，登也。登者，升也。升者，高也。高者，绝也。绝者，独也。"),
    ("第一百一十七则", "余波者，波也。波者，动也。动者，传也。传者，续也。续者，久也。"),
    ("第一百一十八则", "无声者，静也。静者，安也。安者，定也。定者，不动也。不动者，常。"),
    ("第一百一十九则", "永恒者，久也。久者，长也。长者，永也。永者，不灭也。不灭者，存。"),
]

# 需要处理的章节列表
target_chapters = {
    182: 0, 184: 1, 185: 2, 186: 3, 187: 4, 188: 5, 189: 6, 190: 7,
    191: 8, 192: 9, 193: 10, 194: 11, 195: 12, 196: 13, 197: 14, 198: 15, 199: 16
}

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
    
    if chapter_num not in target_chapters:
        continue
    
    # 分配人祖传
    idx = target_chapters[chapter_num]
    quote_num, quote_text = RENZU_QUOTES[idx]
    
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
