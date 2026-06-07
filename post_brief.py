#!/usr/bin/env python
"""Post daily briefs to Supabase. Reads key from .env."""
import json, os, sys, urllib.request

KEY = os.environ.get("SUPABASE_KEY")
if not KEY:
    # Try reading from the dashboard HTML
    import re
    html_path = os.path.expanduser(r"~/Desktop/supplier-dashboard/index.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            for line in f:
                if "SUPABASE_ANON_KEY" in line and "'" in line:
                    m = re.search(r"'([^']+)'", line)
                    if m:
                        KEY = m.group(1)
                        break
if not KEY:
    print("ERROR: SUPABASE_KEY not set and couldn't extract from HTML")
    sys.exit(1)

url = "https://yybpjnxudjptlnuswskt.supabase.co/rest/v1/daily_briefs"
headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}
data = json.dumps({
    "brief_date": sys.argv[1] if len(sys.argv) > 1 else __import__("datetime").date.today().isoformat(),
    "title": sys.argv[2] if len(sys.argv) > 2 else "Daily Brief",
    "notes": sys.argv[3] if len(sys.argv) > 3 else "",
}).encode()

req = urllib.request.Request(url, data=data, headers=headers)
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f"OK 201 id={result[0]['id']}" if result else f"OK {resp.status}")
except urllib.error.HTTPError as e:
    print(f"ERROR {e.code}: {e.read().decode()[:100]}")
    sys.exit(1)