import os
import xml.etree.ElementTree as ET
from datetime import datetime

# ✅ sitemap.xml이 있는 디렉토리 지정
SITEMAP_DIR = r"E:\시외버스\html_outputs"  # 📌 sitemap.xml이 있는 폴더 경로 지정
SITEMAP_FILE = os.path.join(SITEMAP_DIR, "sitemap.xml")  # 절대 경로로 지정
RSS_FILE = os.path.join(SITEMAP_DIR, "rss.xml")  # RSS도 같은 폴더에 저장

# ✅ 현재 날짜 (RFC 822 형식)
NOW = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")

# ✅ RSS 기본 구조 생성
rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>전국 시외버스 시간표</title>
        <link>https://time.issue-manager.co.kr</link>
        <description>최신 시외버스 시간표 및 요금 정보를 확인하세요.</description>
        <language>ko-KR</language>
        <lastBuildDate>{NOW}</lastBuildDate>
"""

# ✅ sitemap.xml 파일 확인
if not os.path.exists(SITEMAP_FILE):
    print(f"❌ 오류: {SITEMAP_FILE} 파일을 찾을 수 없습니다.")
    exit()

# ✅ sitemap.xml을 읽어 RSS <item> 태그 추가
try:
    tree = ET.parse(SITEMAP_FILE)
    root = tree.getroot()

    # ✅ loc 태그를 찾아 RSS 항목으로 변환
    for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc_elem = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        lastmod_elem = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")

        if loc_elem is None or loc_elem.text is None:
            continue  # URL이 없으면 건너뛰기

        loc = loc_elem.text  # 페이지 URL
        lastmod = lastmod_elem.text if lastmod_elem is not None and lastmod_elem.text else None  # lastmod 값 가져오기

        # ✅ lastmod를 RFC 822 형식으로 변환
        if lastmod:
            try:
                lastmod_date = datetime.strptime(lastmod, "%Y-%m-%d")
                pub_date = lastmod_date.strftime("%a, %d %b %Y 00:00:00 +0900")  # RFC 822 형식 변환
            except ValueError:
                pub_date = NOW  # 변환 실패 시 현재 시간 사용
        else:
            pub_date = NOW  # lastmod가 없으면 현재 시간 사용

        # ✅ URL에서 제목 추출 (예: "incheon-seoul-bus" → "Incheon Seoul Bus 시간표")
        title = loc.split("/")[-1].replace("-", " ").title().strip()
        if not title or title.lower() == "index":  # index.html 예외 처리
            continue

        # ✅ RSS 항목 추가
        rss_content += f"""
        <item>
            <title>{title} 시간표</title>
            <link>{loc}</link>
            <description>{title} 정보를 확인하세요.</description>
            <pubDate>{pub_date}</pubDate>
        </item>
        """

except Exception as e:
    print(f"❌ 사이트맵 로드 오류: {e}")
    exit()

# ✅ RSS 종료 태그 추가
rss_content += """
    </channel>
</rss>
"""

# ✅ RSS 파일 저장
with open(RSS_FILE, "w", encoding="utf-8") as f:
    f.write(rss_content)

print(f"✅ RSS 피드 생성 완료: {RSS_FILE}")
