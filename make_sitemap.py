import os
import datetime

# ✅ 사이트 기본 URL
BASE_URL = "https://time.issue-manager.co.kr"

# ✅ 현재 날짜 가져오기 (YYYY-MM-DD 형식)
today_date = datetime.date.today().isoformat()

# ✅ 사이트맵 초기화
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

# ✅ index.html (홈페이지) → priority 1.0
sitemap_content += f"""    <url>
        <loc>{BASE_URL}/</loc>
        <lastmod>{today_date}</lastmod>
        <priority>1.0</priority>
    </url>
"""

# ✅ HTML 파일 자동 탐색 및 추가 (index.html 제외)
HTML_DIRECTORY = r"E:\시외버스\html_outputs"  # 📌 HTML 파일이 있는 경로 지정

for file_name in os.listdir(HTML_DIRECTORY):
    if file_name.endswith(".html") and file_name != "index.html":
        file_path = os.path.join(HTML_DIRECTORY, file_name)

        # ✅ 실제 수정 날짜 가져오기
        last_modified_timestamp = os.path.getmtime(file_path)
        last_modified_date = datetime.datetime.fromtimestamp(last_modified_timestamp).strftime('%Y-%m-%d')

        # ✅ 페이지 URL 생성
        page_url = f"{BASE_URL}/{file_name.replace('.html', '')}"

        # ✅ priority 설정 (파일명에 "출발하는" 또는 "시외버스터미널" 포함 여부에 따라 설정)
        if "출발하는" in file_name or "시외버스터미널" in file_name:
            priority = "0.9"
        else:
            priority = "0.8"

        # ✅ 사이트맵에 추가
        sitemap_content += f"""    <url>
        <loc>{page_url}</loc>
        <lastmod>{last_modified_date}</lastmod>
        <priority>{priority}</priority>
    </url>
"""

sitemap_content += "</urlset>"

# ✅ sitemap.xml 파일 저장
sitemap_path = os.path.join(HTML_DIRECTORY, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"✅ sitemap.xml 파일 생성 완료: {sitemap_path}")
