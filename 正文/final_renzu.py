#!/usr/bin/env python3
import re
from pathlib import Path

# 人祖传语录库
RENZU_QUOTES = {
    182: ("第一百零四则", "凤家者，华也。华者，盛也。盛者，荣也。荣者，贵也贵者，富也。富者，天地同享。"),
    184: ("第一百零五则", "镇运者，定也。定者，安也。安者，稳也。稳者，不动也。不动者，天地同定。"),
    185: ("第一百零六则", "波涛者，动也。动者，变也。变者，生也。生者，死也。生死轮回，如潮涨落。"),
    186: ("第一百零七则", "前夕者，前也。前者，先也。先者，领也。领者，导也。导者，引也。引者，入也。"),
    187: ("第一百零八则", "凤家二仙者，双也。双者，对也。对者，峙也。峙者，争也。争者，必有一伤。"),
    188: ("第一百零九则", "余波者，波也。波者，动也。动者，传也。传者，续也。续者，久也。久久不息。"),
    189: ("第一百一十则", "无声者，静也。静者，安也。安者，定也。定者，不动也。不动者，常也。常者，道也。"),
    190: ("第一百一十一则", "混沌者，浊也。浊者，乱也。乱者，无序也。无序者，天地之始也。始者，生也。"),
    191: ("第一百一十二则", "星宿在混沌者，存也。存者，在也。在者，立也。立者，住也。住者，定也。"),
    192: ("第一百一十三则", "推算者，谋也。谋者，算也。算者，知也。知者，预也。预者，先也。先者，胜也。"),
    193: ("第一百一十四则", "裂隙者，隙也。隙者，缝也。缝者，通也。通者，透也。透者，入也。入者，破也。"),
    194: ("第一百一十五则", "觉醒者，悟也。悟者，明也。明者，见也。见者，知也。知者，不惑也。"),
    195: ("第一百一十六则", "等待者，候也。候者，待也。待者，望也。望者，期也。期者，必来也。"),
    196: ("第一百一十七则", "临界者，界也。界者，分也。分者，别也。别者，择也。择者，判也。判者，定也。"),
    197: ("第一百一十八则", "最后一人者，孤也。孤者，独也。独者，强者也。强者不群，不群者胜。"),
    198: ("第一百一十九则", "发现者，见也。见者，知也。知者，觉也。觉者，醒也。醒者，悟也。悟者，道也。"),
    199: ("第一百二十则", "最后一算者，终也。终者，末也。末者，极也。极者，顶也。顶者，天也。"),
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
    
    if chapter_num not in RENZU_QUOTES:
        continue
    
    quote_num, quote_text = RENZU_QUOTES[chapter_num]
    
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
