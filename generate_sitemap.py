#!/usr/bin/env python3
"""
generate_sitemap.py
--------------------
data/ 폴더의 JSON 파일을 읽어 job.html?country=...&job=... URL을
sitemap_jobs.xml 로 자동 생성합니다.
"""

import json
import os
from urllib.parse import quote
from datetime import date
from xml.sax.saxutils import escape

BASE_URL = "https://www.futurejob.site"
DATA_DIR = "./data"
OUTPUT_FILE = "sitemap_jobs.xml"
TODAY = date.today().isoformat()

COUNTRY_FILE_MAP = {
    '대한민국': 'KR.json', '미국': 'US.json', '일본': 'JP.json',
    '독일': 'DE.json', '캐나다': 'CA.json', '호주': 'AU.json',
    '싱가포르': 'SG.json', '영국': 'UK.json', '중국': 'CN.json',
    '인도': 'IN.json', '베트남': 'VN.json', '태국': 'TH.json',
    '인도네시아': 'ID.json', '아랍에미리트': 'AE.json', '사우디아라비아': 'SA.json',
    '이스라엘': 'IL.json', '프랑스': 'FR.json', '이탈리아': 'IT.json',
    '스위스': 'CH.json', '튀르키예': 'TR.json', '폴란드': 'PL.json',
    '멕시코': 'MX.json', '브라질': 'BR.json', '남아프리카공화국': 'ZA.json',
    '나이지리아': 'NG.json', '러시아': 'RU.json'
}

def generate():
    urls = []
    total = 0
    skipped = 0

    for country, filename in COUNTRY_FILE_MAP.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  [건너뜀] 파일 없음: {filepath}")
            skipped += 1
            continue

        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                job = item.get('추천직업', '').strip()
                if not job:
                    continue

                # 들여쓰기 수정 구간
                encoded_country = quote(country)
                job_safe = escape(job)
                encoded_job = quote(job_safe)

                loc = f"{BASE_URL}/job.html?country={encoded_country}&amp;job={encoded_job}"

                urls.append(loc)
                total += 1
                print(f"  {country}: {total:,}개 처리 중", end='\r')

    print(f"\n총 {total:,}개 URL 수집 완료")

    CHUNK_SIZE = 49000
    chunks = [urls[i:i + CHUNK_SIZE] for i in range(0, len(urls), CHUNK_SIZE)]

    for idx, chunk in enumerate(chunks):
        if len(chunks) == 1:
            out_name = OUTPUT_FILE
        else:
            base, ext = os.path.splitext(OUTPUT_FILE)
            out_name = f"{base}_{idx+1}{ext}"

        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for loc in chunk:
            lines.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")
        lines.append('</urlset>')

        with open(out_name, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"\n✅ 생성 완료: {out_name} ({len(chunk):,}개 URL)")

    print(f"\n총 {total:,}개 URL 생성 | {skipped}개 국가 파일 없음")

if __name__ == '__main__':
    print(f"🔄 사이트맵 생성 시작 (data 폴더: {os.path.abspath(DATA_DIR)})")
    generate()