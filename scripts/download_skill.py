import requests, os, sys, json, re

SKILLS_DIR = os.path.expanduser("~/Desktop/skills")
CATALOG = os.path.join(SKILLS_DIR, "skills-catalog.html")

def download(repo):
    name = repo.split("/")[-1]
    os.makedirs(SKILLS_DIR, exist_ok=True)
    for branch in ["main", "master"]:
        url = "https://github.com/" + repo + "/archive/refs/heads/" + branch + ".zip"
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and len(r.content) > 100:
            p = os.path.join(SKILLS_DIR, name + ".zip")
            with open(p, "wb") as f: f.write(r.content)
            return name, branch, len(r.content), p
    return None, None, 0, None

def fetch_readme(repo):
    for branch in ["main", "master"]:
        url = "https://raw.githubusercontent.com/" + repo + "/" + branch + "/README.md"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.text[:3000]
    return ""

def extract_cn(readme):
    lines = readme.split("\n")
    for l in lines:
        l = l.strip()
        if l and len(l) > 10 and not l.startswith("#") and not l.startswith("["):
            l = re.sub(r"[#*`\[\]\(\)]", "", l)
            if len(l) > 15:
                return l[:200]
    return "A Codex skill."

def extract_en(readme):
    for l in readme.split("\n"):
        l = l.strip()
        if l and len(l) > 10 and not l.startswith("#"):
            l = re.sub(r"[#*`\[\]\(\)]", "", l)
            if len(l) > 15:
                return l[:200]
    return "A Codex skill."

def update_catalog(repo, name, cn, en, size_kb):
    owner = repo.split("/")[0]
    html = ""
    if os.path.exists(CATALOG):
        with open(CATALOG, "r", encoding="utf-8") as f:
            html = f.read()
    if not html:
        html = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
        html += '<title>Skills Catalog</title><style>'
        html += 'body{font-family:-apple-system,"Microsoft YaHei",sans-serif;background:#f5f5f5;padding:40px}'
        html += 'h1{font-size:22px}h1 span{font-size:13px;color:#888;margin-left:10px}'
        html += 'table{width:100%;border-collapse:collapse;background:#fff;border-radius:10px}'
        html += 'th,td{padding:14px 16px;border-bottom:1px solid #eee;font-size:14px;text-align:left}'
        html += 'th{background:#f0f4ff}.name{font-size:15px;font-weight:700}'
        html += '.cn{font-size:13px;color:#444;line-height:1.6;margin-top:2px}'
        html += '.en{font-size:12px;color:#888;line-height:1.5;margin-top:6px;font-style:italic}'
        html += 'a{color:#2563eb;text-decoration:none;font-size:12px}'
        html += '</style></head><body><h1>Skills Catalog<span>Desktop/skills/ 技能仓库</span></h1>'
        html += '<table><tr><th>#</th><th>Name</th><th>Description</th><th>Source</th></tr></table></body></html>'

    if '>' + name + '<' in html or 'target=_blank>' + name + '<' in html:
        # Update existing entry - replace the row
        pass
    else:
        # Count existing rows
        count = html.count("<tr>")
        row = '<tr><td>' + str(count) + '</td>'
        row += '<td><div class=name>' + name + '</div><a href="https://github.com/' + repo + '" target=_blank>github.com/' + repo + '</a></td>'
        row += '<td><div class=cn>' + cn + '</div><div class=en>' + en + '</div></td>'
        row += '<td>' + owner + '</td></tr>'
        html = html.replace("</table>", row + "</table>")

    with open(CATALOG, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "help", "usage": "python download_skill.py <owner/repo>"}))
        sys.exit(1)
    repo = sys.argv[1]
    name, branch, size, path = download(repo)
    if not name:
        print(json.dumps({"status": "error", "message": "Download failed for " + repo}))
        sys.exit(1)
    readme = fetch_readme(repo)
    cn = extract_cn(readme)
    en = extract_en(readme)
    kb = round(size / 1024, 1)
    update_catalog(repo, name, cn, en, kb)
    print(json.dumps({"status": "ok", "name": name, "repo": repo, "branch": branch, "size_kb": kb, "desc_cn": cn, "desc_en": en, "path": path}, ensure_ascii=False))
