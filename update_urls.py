#!/usr/bin/env python
"""Update all product niches with Amazon search URLs."""
import json, os, re, urllib.request

html_path = os.path.expanduser(r"~/Desktop/supplier-dashboard/index.html")
KEY = None
with open(html_path) as f:
    for line in f:
        if "SUPABASE_ANON_KEY" in line and "'" in line:
            m = re.search(r"'([^']+)'", line)
            if m:
                KEY = m.group(1)
                break

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
}

# Niche name -> Amazon search URL mapping
urls = {
    1: "https://www.amazon.com/s?k=kitchen+compost+bin",
    2: "https://www.amazon.com/s?k=bamboo+floating+shelves+3+pack",
    3: "https://www.amazon.com/s?k=silicone+food+storage+lids+set",
    4: "https://www.amazon.com/s?k=herb+scissors+5+blade+kit",
    5: "https://www.amazon.com/s?k=macrame+wall+hanging+kit+premium",
    6: "https://www.amazon.com/s?k=stainless+steel+oil+sprayer+2+pack",
    7: "https://www.amazon.com/s?k=reusable+beeswax+food+wraps+set",
    8: "https://www.amazon.com/s?k=sun+catchers+stained+glass+set",
    9: "https://www.amazon.com/s?k=photo+drying+rack+wall+mounted",
    10: "https://www.amazon.com/s?k=weighted+silicone+cooking+utensils+set"
}

for nid, surl in urls.items():
    data = json.dumps({"source_url": surl, "updated_at": "2026-06-06T12:00:00Z"}).encode()
    req = urllib.request.Request(
        f"https://yybpjnxudjptlnuswskt.supabase.co/rest/v1/product_niches?id=eq.{nid}",
        data=data, headers=headers, method="PATCH"
    )
    resp = urllib.request.urlopen(req)
    print(f"  id={nid} -> {resp.status}")

print("All URLs updated!")