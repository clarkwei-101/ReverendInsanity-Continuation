#!/usr/bin/env python3
import os
import re
from pathlib import Path

chapter_files = list(Path('.').glob('*.md'))
renzu_count = 0
no_renzu = []

for f in sorted(chapter_files):
    content = f.read_text(encoding='utf-8')
    
    # 检查是否已有人祖传（忽略格式）
    if re.search(r'人祖传', content):
        renzu_count += 1
    else:
        match = re.match(r'第(\d+)[章节]', f.stem)
        if match:
            no_renzu.append(int(match.group(1)))

print(f"有人祖传章节: {renzu_count}")
print(f"无人祖传章节: {len(no_renzu)}")
print(f"无人祖传章节列表: {no_renzu}")
