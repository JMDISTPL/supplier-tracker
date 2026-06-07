#!/usr/bin/env python
"""Post 10 niches as a sourcing brief to Supabase."""
import json, os, re, urllib.request

html_path = os.path.expanduser(r"~/Desktop/supplier-dashboard/index.html")
KEY = None
if os.path.exists(html_path):
    with open(html_path) as f:
        for line in f:
            if "SUPABASE_ANON_KEY" in line and "'" in line:
                m = re.search(r"'([^']+)'", line)
                if m:
                    KEY = m.group(1)
                    break

url = "https://yybpjnxudjptlnuswskt.supabase.co/rest/v1/daily_briefs"
headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

notes = """Good morning Jack! ☀️

🔍 PRODUCT SOURCING REPORT — Top 10 Niches

💪 WORKOUT OF THE DAY
None (research day)

📖 MARKET RESEARCH THEME
First product opportunities in Kitchen & Home Decor fitting your criteria: $45-80 sell price, 15k+ SV, <$1.25 CPC, <2kg

💡 TOP PICKS

🥇 Kitchen Compost Bin — $49-69
SV 15-20k | CPC $0.95 | Low comp | 1.5kg | ~$10 cost
Pros: Eco trend, naturally fits price, low reviews (100-400), easy differentiation
Cons: Higher CPC, dent risk in shipping

🥈 Bamboo Floating Shelves 3pk — $49-59
SV 18-30k | CPC $0.60 | Medium comp | 1.2kg | ~$8 cost
Pros: HIGHEST demand, cheapest CPC, year-round, easy differentiation
Cons: Some heavy hitters with 600+ reviews

🥉 Weighted Silicone Utensil Set 5pc — $45-55
SV 18-30k | CPC $0.85 | Moderate comp | 0.7kg | ~$7 cost
Pros: Highest volume, good CPC, premium feel, low returns
Cons: 2-3 major brands, commodity risk

📊 ALL 10 NICHES

4. Premium Herb Scissors + Kit — $44-55
   SV 12-18k | CPC $0.75 | VERY low comp | 0.3kg
   Easiest to rank (lowest reviews)

5. DIY Macrame Wall Hanging Kit — $45-60
   SV 15-25k | CPC $0.85 | Low comp | 0.4kg
   Boho trend, DIY premium angle

6. SS Oil Sprayer 2-Pack — $45-55
   SV 15-25k | CPC $0.90 | Moderate | 0.4kg
   Health/air fryer trend

7. Reusable Beeswax Wraps (10pk) — $45-50
   SV 15-20k | CPC $0.85 | Moderate | 0.2kg
   Eco-friendly, ultra light

8. Modern Sun Catchers (3pk) — $49-79
   SV 10-15k | CPC $0.70 | VERY low comp | 0.5kg
   Unique aesthetic, easiest differentiation

9. Wooden Photo/Art Drying Rack — $49-59
   SV 12-18k | CPC $0.80 | VERY low comp | 0.8kg
   Dual purpose (kitchen + decor)

10. Silicone Food Storage Lids (12pk) — $49-59
    SV 15-22k | CPC $0.70 | Moderate | 0.6kg
    Cheapest production (~$5), meal prep trend

🌍 SOURCING STRATEGY
• All 10 posted to the new Sourcing page on your dashboard
• Approve/Deny each one directly on the site
• Denied items go to the learning archive so I improve next time
• Start with supplier scouting on Alibaba for your top picks""".strip()

data = json.dumps({
    "brief_date": "2026-06-06-sourcing",
    "title": "Sourcing Research — 10 Kitchen & Home Decor Niches",
    "notes": notes
}).encode()

req = urllib.request.Request(url, data=data, headers=headers)
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f"Posted OK id={result[0]['id']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"ERROR {e.code}: {body[:200]}")