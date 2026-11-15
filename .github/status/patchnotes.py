# -*- coding: utf-8 -*-
"""Patch note Discord pour chaque release de H1Z1 Skin Maker (lancé par la GitHub Action patch-notes.yml).

Sur une release publiée : lit la release dans l'évènement GitHub. En lancement manuel : lit la release
du tag demandé (ou la dernière). Poste ensuite un embed dans #patch-notes via un webhook.
Variables : WEBHOOK_URL, GITHUB_TOKEN, GITHUB_EVENT_PATH, GITHUB_EVENT_NAME, RELEASES_REPO, TAG.
"""
import json
import os
import re
import urllib.error
import urllib.request

WEBHOOK = os.environ["WEBHOOK_URL"]
REPO = os.environ.get("RELEASES_REPO", "jessy-chaila/h1z1-skin-maker-releases")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UA = "H1Z1-Skin-Maker-PatchNotes (https://github.com/%s, 1.0)" % REPO
COLOR = 0x9B59B6


def http(url, body=None, headers=None):
    h = {"User-Agent": UA}
    h.update(headers or {})
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def get_release():
    if os.environ.get("GITHUB_EVENT_NAME") == "release":
        with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
            return json.load(f)["release"]
    tag = (os.environ.get("TAG") or "").strip()
    path = f"tags/{tag}" if tag else "latest"
    h = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = "Bearer " + TOKEN
    return http(f"https://api.github.com/repos/{REPO}/releases/{path}", headers=h)


def discord_markdown(text):
    """Notes GitHub → Discord : titres ### réduits, lignes vides en trop retirées."""
    text = (text or "").replace("\r\n", "\n").strip()
    text = re.sub(r"^#{4,}\s*", "### ", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main():
    rel = get_release()
    tag = rel.get("tag_name", "")
    version = tag.lstrip("vV")
    notes = discord_markdown(rel.get("body")) or "_No notes for this release._"
    if len(notes) > 3800:
        notes = notes[:3790].rsplit("\n", 1)[0] + "\n…"
    zips = [a for a in rel.get("assets", []) if a.get("name", "").endswith(".zip")]
    links = f"[Release page]({rel.get('html_url')})"
    if zips:
        size = zips[0].get("size", 0) / 1024 / 1024
        links = f"[Download the zip]({zips[0]['browser_download_url']}) ({size:.0f} MB) · " + links
    embed = {
        "title": f"🩹 H1Z1 Skin Maker {version}",
        "url": rel.get("html_url"),
        "description": notes,
        "color": COLOR,
        "fields": [
            {"name": "⬆️ Update", "value": "Open Skin Maker → **Home → Install update**", "inline": False},
            {"name": "🔗 Links", "value": links, "inline": False},
        ],
        "footer": {"text": "H1Z1 Skin Maker"},
        "timestamp": rel.get("published_at") or rel.get("created_at"),
    }
    try:
        http(WEBHOOK + ("&" if "?" in WEBHOOK else "?") + "wait=true",
             {"embeds": [embed], "allowed_mentions": {"parse": []}})
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Discord a refusé le message : {e.code} {e.read()[:300]!r}")
    print(f"patch note publié : {tag}")


if __name__ == "__main__":
    main()
