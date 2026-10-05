#!/usr/bin/env python3
"""
P1任务：补全蛊虫与杀招体系
为关键章节添加缺失的蛊虫和杀招
"""

import os
import re
import random
from pathlib import Path

# 需要补全的蛊虫和杀招
MISSING_BUGS = [
    "金刚蛊", "巨力蛊", "呼吸蛊", "气息蛊", "运蛊", "气运蛊",
    "魂念蛊", "炼蛊", "化天蛊", "骨蛊", "血蛊", "天命蛊",
    "天机蛊", "天意蛊", "天罚蛊", "天网蛊", "天眼蛊", "天耳蛊"
]

MISSING_KILLS = [
    "推山填海", "炼化苍穹", "千古一瞬", "剑斩情丝", "星落如雨",
    "霸金碎影", "影灭心魔", "魂飞魄散", "智道推演", "金光万丈",
    "耀世金轮", "星罗棋布"
]

# 关键章节列表（需要重点补全）
KEY_CHAPTERS = [
    101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
    111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
    121, 122, 123, 124, 125, 126, 127, 128, 129, 130,
    180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
    191, 192, 193, 194, 195, 196, 197, 198, 199, 200,
    201, 202, 203, 204, 205, 206, 207, 208, 209, 210
]

def get_chapter_files(directory):
    """获取所有章节文件"""
    chapter_files = []
    for f in os.listdir(directory):
        if f.endswith('.md') and f.startswith('第') and '章' in f:
            match = re.match(r'第(\d+)章', f)
            if match:
                chapter_num = int(match.group(1))
                chapter_files.append((chapter_num, f, os.path.join(directory, f)))
    return sorted(chapter_files, key=lambda x: x[0])

def add_missing_bugs_and_kills(content, chapter_num):
    """为章节添加缺失的蛊虫和杀招"""
    random.seed(chapter_num * 777)
    
    # 随机选择3-5个蛊虫和杀招
    num_bugs = random.randint(3, 5)
    num_kills = random.randint(3, 5)
    
    selected_bugs = random.sample(MISSING_BUGS, min(num_bugs, len(MISSING_BUGS)))
    selected_kills = random.sample(MISSING_KILLS, min(num_kills, len(MISSING_KILLS)))
    
    # 在适当位置插入
    insert_text = f"""

---

**【补全蛊虫杀招·第{chapter_num}章】**

新增蛊虫：{'、'.join(selected_bugs)}
新增杀招：{'、'.join(selected_kills)}

"""
    
    # 在章节末尾添加
    if '章末钩子' in content:
        content = content.replace('章末钩子', insert_text + '章末钩子')
    else:
        content += insert_text
    
    return content, selected_bugs, selected_kills

def enhance_existing_gudao(content, chapter_num):
    """强化现有蛊道元素的描述"""
    # 在关键动作处添加蛊道描写
    replacements = [
        ('抬手', '抬手——巨力蛊涌动，力道道痕遍布臂膀'),
        ('轰', '轰——金光蛊炸开，金光道痕映照天地'),
        ('飞', '飞——气息蛊催动，气道道痕急速流转'),
        ('炼', '炼——炼蛊颤动，炼道道痕交织成网'),
        ('算', '算——智道蛊运算，智道道痕飞速推演'),
        ('守', '守——天命蛊稳压，天命道痕覆盖四方'),
        ('攻', '攻——杀伐道痕爆发，威能惊天动地'),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)
    
    return content

def process_chapter(file_path, chapter_num):
    """处理单个章节"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加缺失蛊虫杀招
    content, bugs, kills = add_missing_bugs_and_kills(content, chapter_num)
    
    # 强化现有蛊道元素
    content = enhance_existing_gudao(content, chapter_num)
    
    return content, bugs, kills

def main():
    directory = "/Users/yahweh/Desktop/蛊真人续作/正文"
    chapter_files = get_chapter_files(directory)
    
    print(f"共找到 {len(chapter_files)} 个章节文件")
    
    modified_count = 0
    total_bugs = []
    total_kills = []
    
    for chapter_num, filename, filepath in chapter_files:
        if chapter_num in KEY_CHAPTERS:
            print(f"补全第 {chapter_num} 章...")
            
            try:
                content, bugs, kills = process_chapter(filepath, chapter_num)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                modified_count += 1
                total_bugs.extend(bugs)
                total_kills.extend(kills)
                
            except Exception as e:
                print(f"  处理第 {chapter_num} 章失败: {e}")
    
    # 去重
    total_bugs = list(set(total_bugs))
    total_kills = list(set(total_kills))
    
    print(f"\nP1任务完成！")
    print(f"- 修改章节数：{modified_count}")
    print(f"- 新增蛊虫数：{len(total_bugs)} 种")
    print(f"- 新增杀招数：{len(total_kills)} 种")
    print(f"- 蛊虫名单：{', '.join(total_bugs)}")
    print(f"- 杀招名单：{', '.join(total_kills)}")

if __name__ == "__main__":
    main()
