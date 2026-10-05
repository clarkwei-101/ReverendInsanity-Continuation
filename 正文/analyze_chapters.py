#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

# 黑名单词（AI词）
BLACKLIST_WORDS = ['眼眸中闪过', '眼中闪过', '他知道', '决然', '缓缓', '静静', '仿佛', '似乎', '宛如', '忽然', '骤然', '蓦然', '悄然', '低声', '这一生', '傲然', '眉头', '微微一笑', '沉声']

# 蛊道元素关键词
GUDAO_KEYWORDS = [
    '蛊', '杀招', '道痕', '境界', '蛊仙', '仙蛊', '蛊虫', '炼道', '智道', '金道', '力道', 
    '宙道', '律道', '信道', '魂道', '偷道', '运道', '变形道', '血道', '阵道', '剑道',
    '仙窍', '真元', '天庭', '五域', '两天', '南疆', '东海', '西漠', '北原', '中洲',
    '九转', '八转', '七转', '六转', '五转', '四转', '三转', '二转', '一转',
    '尊者', '仙尊', '魔尊', '散仙', '地灾', '天劫', '万劫',
    '蛊阵', '蛊屋', '蛊方', '蛊材', '道主', '道祖', '道痕'
]

# 蛊虫名
GUCHONG_NAMES = [
    '永生蛊', '气功果核', '衍化蛊', '星宿罗网蛊', '先天一气蛊', '星散营', '削运金刀',
    '天炼', '衍化之力', '金道', '智道', '炼道', '气种', '天意', '衍化', '衍'
]

# 人祖传相关
RENZU_PATTERNS = ['人祖传', '人祖']

chapter_files = list(Path('.').glob('*.md'))
results = []

for f in sorted(chapter_files):
    content = f.read_text(encoding='utf-8')
    
    # 提取章节号和标题
    match = re.match(r'第(\d+)[章节]', f.stem)
    if not match:
        continue
    chapter_num = int(match.group(1))
    
    # 检查人祖传引用
    renzu_count = len(re.findall(r'人祖传', content))
    has_renzu = renzu_count > 0
    
    # 检查蛊道元素密度
    gudao_count = 0
    for keyword in GUDAO_KEYWORDS:
        gudao_count += len(re.findall(keyword, content))
    
    # 检查蛊虫名出现次数
    guchong_count = 0
    for name in GUCHONG_NAMES:
        guchong_count += len(re.findall(name, content))
    
    # 检查AI词
    ai_words_found = []
    for word in BLACKLIST_WORDS:
        if word in content:
            ai_words_found.append(word)
    
    # 蛊道元素密度评估
    gudao_density = 'high' if gudao_count > 30 else ('medium' if gudao_count > 10 else 'low')
    
    # 人祖传覆盖率评估
    renzu_status = 'covered' if has_renzu else 'missing'
    
    results.append({
        'chapter': chapter_num,
        'file': f.name,
        'renzu_count': renzu_count,
        'has_renzu': has_renzu,
        'renzu_status': renzu_status,
        'gudao_count': gudao_count,
        'guchong_count': guchong_count,
        'gudao_density': gudao_density,
        'ai_words': ai_words_found,
        'ai_count': len(ai_words_found)
    })

# 统计分析
total_chapters = len(results)
renzu_missing = [r for r in results if not r['has_renzu']]
renzu_covered = [r for r in results if r['has_renzu']]
gudao_low = [r for r in results if r['gudao_density'] == 'low']
gudao_medium = [r for r in results if r['gudao_density'] == 'medium']
gudao_high = [r for r in results if r['gudao_density'] == 'high']

print("=" * 60)
print("蛊真人续作 - 章节分析报告")
print("=" * 60)
print(f"\n总章节数: {total_chapters}")
print(f"\n【人祖传覆盖】")
print(f"  有引用: {len(renzu_covered)} ({len(renzu_covered)*100//total_chapters}%)")
print(f"  无引用: {len(renzu_missing)} ({len(renzu_missing)*100//total_chapters}%)")
print(f"\n【蛊道元素密度】")
print(f"  高密度(>30次): {len(gudao_high)}")
print(f"  中密度(10-30次): {len(gudao_medium)}")
print(f"  低密度(≤10次): {len(gudao_low)}")
print(f"\n【AI词检测】")
total_ai = sum(r['ai_count'] for r in results)
chapters_with_ai = len([r for r in results if r['ai_count'] > 0])
print(f"  含AI词章节: {chapters_with_ai}")
print(f"  总AI词出现: {total_ai}")

print("\n" + "=" * 60)
print("缺少人祖传的章节 (前50个)")
print("=" * 60)
for r in sorted(renzu_missing, key=lambda x: x['chapter'])[:50]:
    print(f"  第{r['chapter']:04d}章 - 蛊道元素:{r['gudao_count']}次")

print("\n" + "=" * 60)
print("蛊道元素低密度章节 (前50个)")
print("=" * 60)
for r in sorted(gudao_low, key=lambda x: x['gudao_count'])[:50]:
    print(f"  第{r['chapter']:04d}章 - 蛊道元素:{r['gudao_count']}次, 人祖传:{r['renzu_count']}次")

# 输出JSON供后续使用
with open('analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': total_chapters,
        'renzu_missing': [r['chapter'] for r in renzu_missing],
        'renzu_covered_count': len(renzu_covered),
        'gudao_low': [{'chapter': r['chapter'], 'count': r['gudao_count']} for r in gudao_low]
    }, f, ensure_ascii=False, indent=2)

print("\n分析结果已保存到 analysis_results.json")
