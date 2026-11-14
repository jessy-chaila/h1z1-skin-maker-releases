# -*- coding: utf-8 -*-
"""Embed « Services status » du serveur Discord H1Z1 Skin Maker (lancé par la GitHub Action status.yml).

Vérifie la dernière release, le téléchargement des mises à jour, la liste des membres (Gist), l'état de
Discord et de GitHub, lit les incidents postés dans le salon incidents, puis crée ou modifie un seul message.
Variables : BOT_TOKEN, GIST_ID, GITHUB_TOKEN, STATUS_CHANNEL_ID, INCIDENTS_CHANNEL_ID, RELEASES_REPO.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://discord.com/api/v10"
BOT = os.environ["BOT_TOKEN"]
GIST_ID = os.environ.get("GIST_ID", "")
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
STATUS_CH = os.environ["STATUS_CHANNEL_ID"]
INCIDENTS_CH = os.environ["INCIDENTS_CHANNEL_ID"]
REPO = os.environ.get("RELEASES_REPO", "jessy-chaila/h1z1-skin-maker-releases")
GIST_OWNER = os.environ.get("GIST_OWNER", "jessy-chaila")
UA = "H1Z1-Skin-Maker-Status (https://github.com/%s, 1.0)" % REPO

OK, WARN, DOWN = 0, 1, 2
DOT = {OK: "🟢", WARN: "🟠", DOWN: "🔴"}
COLOR = {OK: 0x2ECC71, WARN: 0xE67E22, DOWN: 0xE74C3C}
HEADLINE = {OK: "All systems operational", WARN: "Degraded service", DOWN: "Service outage"}


def http(url, method="GET", body=None, headers=None, raw=False, timeout=20):
    h = {"User-Agent": UA}
    h.update(headers or {})
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = r.read()
        return (r.status, payload) if raw else json.loads(payload or b"null")


def discord(path, method="GET", body=None):
    for _ in range(3):
        try:
            return http(API + path, method, body, {"Authorization": "Bot " + BOT})
        except urllib.error.HTTPError as e:
            if e.code == 429:                                   # limite de débit : on attend et on réessaie
                time.sleep(float(json.loads(e.read() or b"{}").get("retry_after", 2)) + 0.5)
                continue
            raise
    raise RuntimeError("Discord rate limit")


def gh(url):
    """API GitHub avec le jeton de l'Action, puis sans jeton si celui-ci est refusé (ex. Gist)."""
    h = {"Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        try:
            return http(url, headers=dict(h, Authorization="Bearer " + GH_TOKEN))
        except urllib.error.HTTPError as e:
            if e.code not in (401, 403, 404):
                raise
    return http(url, headers=h)


def ts(iso):
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


# ------------------------------------------------------------------ vérifications

def check_release():
    """(niveau, texte version, niveau updater, texte updater)"""
    try:
        rel = gh(f"https://api.github.com/repos/{REPO}/releases/latest")
    except Exception as e:
        return DOWN, "Unavailable", DOWN, f"Release info unreachable ({type(e).__name__})"
    version = f"**{rel.get('tag_name', '?')}**"
    if rel.get("published_at"):
        version += f"\n<t:{ts(rel['published_at'])}:R>"
    zips = [a for a in rel.get("assets", []) if a.get("name", "").endswith(".zip")]
    if not zips:
        return OK, version, DOWN, "No download in the latest release"
    try:
        code, _ = http(zips[0]["browser_download_url"], headers={"Range": "bytes=0-0"}, raw=True)
        if code in (200, 206):
            return OK, version, OK, "Available"
        return OK, version, WARN, f"Unexpected answer ({code})"
    except Exception as e:
        return OK, version, DOWN, f"Download failed ({type(e).__name__})"


def _gist_content():
    """membres.json : d'abord l'URL brute (pas de limite d'API sur les runners partagés), sinon l'API."""
    errors = []
    try:
        _, raw = http(f"https://gist.githubusercontent.com/{GIST_OWNER}/{GIST_ID}/raw/membres.json"
                      f"?t={int(time.time())}", raw=True)
        return raw.decode("utf-8")
    except Exception as e:
        errors.append(f"raw {getattr(e, 'code', type(e).__name__)}")
    try:
        g = gh(f"https://api.github.com/gists/{GIST_ID}")
        f = g.get("files", {}).get("membres.json")
        if f:
            if not f.get("truncated"):
                return f.get("content", "")
            _, raw = http(f["raw_url"], raw=True)
            return raw.decode("utf-8")
        errors.append("api: file missing")
    except Exception as e:
        errors.append(f"api {getattr(e, 'code', type(e).__name__)}")
    raise RuntimeError(", ".join(errors))


def check_access():
    if not GIST_ID:
        return WARN, "Not checked"
    try:
        doc = json.loads(_gist_content())
        bytes.fromhex(doc["sig"])
        serial = doc["data"].get("serial", "?")
        return OK, f"Operational\n-# member list #{serial}"
    except Exception as e:
        print(f"liste des membres illisible : {e}", file=sys.stderr)
        return DOWN, "Member list unreachable"


def check_statuspage(url):
    try:
        s = http(url)["status"]
        lvl = {"none": OK, "minor": WARN, "major": DOWN, "critical": DOWN}.get(s.get("indicator"), WARN)
        return lvl, s.get("description", "?")
    except Exception as e:
        return WARN, f"Status unknown ({type(e).__name__})"


def read_incidents():
    """Messages humains du salon incidents : 🔴 = panne, 🟠/🟡 (ou rien) = dégradé."""
    out = []
    try:
        msgs = discord(f"/channels/{INCIDENTS_CH}/messages?limit=20")
    except Exception as e:
        print(f"incidents illisibles : {e}", file=sys.stderr)
        return out
    for m in reversed(msgs):                                    # du plus ancien au plus récent
        if m.get("author", {}).get("bot"):
            continue
        text = (m.get("content") or "").strip()
        if not text:
            continue
        lvl = WARN
        for mark, l in (("🔴", DOWN), ("🟠", WARN), ("🟡", WARN)):
            if text.startswith(mark):
                lvl, text = l, text[len(mark):].strip()
                break
        out.append((lvl, text[:300], ts(m["timestamp"])))
    return out


# ------------------------------------------------------------------ embed

def build_embed():
    rel_lvl, version, upd_lvl, upd_txt = check_release()
    acc_lvl, acc_txt = check_access()
    dis_lvl, dis_txt = check_statuspage("https://discordstatus.com/api/v2/status.json")
    git_lvl, git_txt = check_statuspage("https://www.githubstatus.com/api/v2/status.json")
    incidents = read_incidents()

    if dis_lvl == DOWN and acc_lvl == OK:                      # la connexion passe par Discord
        acc_lvl, acc_txt = WARN, "Discord login may fail\n" + acc_txt.split("\n", 1)[-1]

    overall = max([rel_lvl, upd_lvl, acc_lvl, dis_lvl, git_lvl] + [i[0] for i in incidents])
    now = int(time.time())
    fields = [
        {"name": "📦 Latest version", "value": version, "inline": True},
        {"name": "⬇️ Updates", "value": f"{DOT[upd_lvl]} {upd_txt}", "inline": True},
        {"name": "🔑 Login & access", "value": f"{DOT[acc_lvl]} {acc_txt}", "inline": True},
        {"name": "💬 Discord", "value": f"{DOT[dis_lvl]} {dis_txt}", "inline": True},
        {"name": "🐙 GitHub", "value": f"{DOT[git_lvl]} {git_txt}", "inline": True},
        {"name": "​", "value": "​", "inline": True},
    ]
    if incidents:
        lines = [f"{DOT[l]} {t}\n-# since <t:{s}:R>" for l, t, s in incidents]
        value = "\n".join(lines)
        if len(value) > 1024:
            value = value[:1020] + "…"
        fields.append({"name": "⚠️ Known issues", "value": value, "inline": False})
    return {
        "title": "📶 H1Z1 Skin Maker — Services status",
        "description": f"## {DOT[overall]} {HEADLINE[overall]}\nLast check <t:{now}:R>",
        "color": COLOR[overall],
        "fields": fields,
        "footer": {"text": "Checked automatically by GitHub Actions"},
        "timestamp": datetime.fromtimestamp(now, timezone.utc).isoformat(),
    }


def main():
    embed = build_embed()
    me = discord("/users/@me")["id"]
    msgs = discord(f"/channels/{STATUS_CH}/messages?limit=50")
    mine = [m for m in msgs if m.get("author", {}).get("id") == me]
    body = {"content": "", "embeds": [embed]}
    if mine:
        discord(f"/channels/{STATUS_CH}/messages/{mine[-1]['id']}", "PATCH", body)
        print("embed mis à jour")
    else:
        discord(f"/channels/{STATUS_CH}/messages", "POST", body)
        print("embed créé")


if __name__ == "__main__":
    main()
