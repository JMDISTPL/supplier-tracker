#!/usr/bin/env python
"""Insert 10 product niches into Supabase. Reads key from index.html."""
import json, os, re, urllib.request

# Read key from dashboard HTML
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
if not KEY:
    print("ERROR: could not find Supabase key")
    exit(1)

url = "https://yybpjnxudjptlnuswskt.supabase.co/rest/v1/product_niches"
headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

niches = [
    {
        "niche_name": "Kitchen Compost Bin",
        "category": "kitchen",
        "price_range": "$49-69",
        "monthly_sales_min": 15000,
        "monthly_sales_max": 20000,
        "est_cpc": 0.95,
        "competition_level": "Low (2 major brands)",
        "weight_kg": 1.5,
        "top_reviews_range": "100-400",
        "est_production_cost": 10.00,
        "pros": ["Eco trend is accelerating", "Naturally hits $49-69 price range", "Very low review barriers on top listings", "Under 2kg for cheap FBA shipping", "Easy differentiation (matte/mint/upgraded filter)", "Only 2-3 major brands dominating"],
        "cons": ["Higher CPC range ($0.95-1.20)", "Stainless steel can dent in shipping if poorly packed", "Seasonal dip in winter months?", "Charcoal filter replacement adds complexity"],
        "market_context": "Zero waste / eco-home trend is gaining momentum. Composting is becoming mainstream in US households."
    },
    {
        "niche_name": "Bamboo Floating Shelves 3-Pack",
        "category": "home-decor",
        "price_range": "$49-59",
        "monthly_sales_min": 18000,
        "monthly_sales_max": 30000,
        "est_cpc": 0.60,
        "competition_level": "Medium (variants under 300 reviews)",
        "weight_kg": 1.2,
        "top_reviews_range": "150-600",
        "est_production_cost": 8.00,
        "pros": ["HIGHEST demand of all options (18-30k SV)", "Cheapest CPC ($0.60-0.95)", "Easy differentiation (bamboo, bracketless, no-drill)", "Lightweight for cheap shipping", "Year-round demand, no seasonality"],
        "cons": ["More competition than compost bin", "Some heavy hitters with 600+ reviews", "Assembly instructions matter for returns", "Bamboo quality varies by supplier"],
        "market_context": "Minimalist home decor trend continues. Boho + Japandi interior design driving floating shelf demand."
    },
    {
        "niche_name": "Premium Silicone Food Storage Lids 12-Pack",
        "category": "kitchen",
        "price_range": "$49-59",
        "monthly_sales_min": 15000,
        "monthly_sales_max": 22000,
        "est_cpc": 0.70,
        "competition_level": "Moderate (many <300 reviews)",
        "weight_kg": 0.6,
        "top_reviews_range": "200-600",
        "est_production_cost": 5.00,
        "pros": ["Cheapest to produce (~$5/unit)", "Very lightweight (0.6kg) = ultra cheap shipping", "Low CPC ($0.70)", "High LTV (subscription repeat buy category)", "Universal fit means fewer SKUs"],
        "cons": ["Needs careful bundling to hit $49 price point", "Moderate competition", "Multiple sizes needed in set = more SKU complexity", "BPA-free certification required"],
        "market_context": "Kitchen organization is a top Amazon growth vertical. Meal prep culture is driving demand."
    },
    {
        "niche_name": "Premium Herb Scissors 5-Blade + Cleaning Kit",
        "category": "kitchen",
        "price_range": "$44-55",
        "monthly_sales_min": 12000,
        "monthly_sales_max": 18000,
        "est_cpc": 0.75,
        "competition_level": "Very low (1-2 brands, 100-400 reviews)",
        "weight_kg": 0.3,
        "top_reviews_range": "100-400",
        "est_production_cost": 4.00,
        "pros": ["LOWEST competition on the list", "Ultra lightweight (0.3kg) = cheapest shipping", "Very low CPC ($0.75)", "Low production cost (~$4)", "Top reviews as low as 100 = easy to rank"],
        "cons": ["SV 12-18k slightly below 15k target", "Hard to hit $45 without bundling (cleaning brush + storage case)", "Sharp edges = liability concern", "Small product = easy to counterfei"],
        "market_context": "Home cooking trend continues. Herb garden / fresh herb popularity is driving demand for prep tools."
    },
    {
        "niche_name": "DIY Macrame Wall Hanging Kit (Premium)",
        "category": "home-decor",
        "price_range": "$45-60",
        "monthly_sales_min": 15000,
        "monthly_sales_max": 25000,
        "est_cpc": 0.85,
        "competition_level": "Low-moderate (few >500 reviews)",
        "weight_kg": 0.4,
        "top_reviews_range": "200-500",
        "est_production_cost": 6.00,
        "pros": ["Strong boho decor trend tailwind", "Very lightweight", "High SV (15-25k)", "Easy differentiation (premium cotton + wood dowel)", "DIY angle = less price sensitivity"],
        "cons": ["Bundling needed to hit $45+", "Finished piece kits need careful packaging", "DIY market has more returns", "Seasonal (stronger in spring/summer)"],
        "market_context": "Boho home decor is one of the fastest-growing aesthetic styles on TikTok/Pinterest."
    },
    {
        "niche_name": "Stainless Steel Oil Sprayer 2-Pack",
        "category": "kitchen",
        "price_range": "$45-55",
        "monthly_sales_min": 15000,
        "monthly_sales_max": 25000,
        "est_cpc": 0.90,
        "competition_level": "Moderate (few strong brands)",
        "weight_kg": 0.4,
        "top_reviews_range": "300-800",
        "est_production_cost": 5.00,
        "pros": ["Health/keto/air fryer trend tailwind", "Lightweight", "2-pack naturally hits $45+ price", "High monthly demand"],
        "cons": ["Higher CPC (~$0.90-1.15)", "Top reviews at 300-800 = harder to rank", "Nozzle clogging complaints are common", "Some heavy hitters (Evo, Misto)"],
        "market_context": "Air fryer + keto diet trend continues driving kitchen gadget demand."
    },
    {
        "niche_name": "Reusable Beeswax Food Wraps Set of 10",
        "category": "kitchen",
        "price_range": "$45-50",
        "monthly_sales_min": 15000,
        "monthly_sales_max": 20000,
        "est_cpc": 0.85,
        "competition_level": "Moderate (300-700 reviews)",
        "weight_kg": 0.2,
        "top_reviews_range": "300-700",
        "est_production_cost": 4.00,
        "pros": ["Eco-friendly trend", "ULTRA lightweight (0.2kg)", "Low production cost", "Good CPC"],
        "cons": ["Hard to hit $45 without bamboo sleeve add-on", "Moderate competition", "300-700 reviews on top = harder to rank", "Beeswax sourcing quality varies"],
        "market_context": "Plastic-free kitchen trend accelerating. Good complement to compost bin niche."
    },
    {
        "niche_name": "Modern Sun Catchers Set of 3",
        "category": "home-decor",
        "price_range": "$49-79",
        "monthly_sales_min": 10000,
        "monthly_sales_max": 15000,
        "est_cpc": 0.70,
        "competition_level": "Very low (mainly handmade shops)",
        "weight_kg": 0.5,
        "top_reviews_range": "50-200",
        "est_production_cost": 5.00,
        "pros": ["VERY low competition", "Tiny top reviews (50-200) = easiest to rank", "Low CPC ($0.70)", "Premium bundled 3-pack hits $49-79", "Different aesthetic = less direct comparison shopping"],
        "cons": ["SV 10-15k below 15k target", "Breakable (glass) = higher return rate", "Niche aesthetic limits market size", "Trend may be shorter-lived"],
        "market_context": "Minimalist / window decor trending on social media. Good complement to macrame."
    },
    {
        "niche_name": "Wooden Photo/Art Drying Rack Wall-Mounted",
        "category": "home-decor",
        "price_range": "$49-59",
        "monthly_sales_min": 12000,
        "monthly_sales_max": 18000,
        "est_cpc": 0.80,
        "competition_level": "Very low (1-2 FBA sellers, mostly Etsy)",
        "weight_kg": 0.8,
        "top_reviews_range": "50-250",
        "est_production_cost": 7.00,
        "pros": ["VERY low competition", "Extremely low reviews (50-250)", "Works for both kitchen (dried herbs) and decor (photos)", "Dual purpose = wider market", "Good CPC"],
        "cons": ["SV 12-18k slightly below 15k target", "Needs bundle (clips + twine) for $49+", "Niche aesthetic", "Wall-mount = more installation friction"],
        "market_context": "Home office / aesthetic wall decor trend growing. Dried herb storage also trending."
    },
    {
        "niche_name": "Weighted Silicone Cooking Utensil Set 5-Piece",
        "category": "kitchen",
        "price_range": "$45-55",
        "monthly_sales_min": 18000,
        "monthly_sales_max": 30000,
        "est_cpc": 0.85,
        "competition_level": "Moderate (some heavy hitters)",
        "weight_kg": 0.7,
        "top_reviews_range": "200-500",
        "est_production_cost": 7.00,
        "pros": ["HIGHEST volume (18-30k++)", "Good CPC ($0.85)", "Weighted handles = premium feel = price justification", "Easy manufacturing in China", "Low returns category"],
        "cons": ["Moderate competition (2-3 major brands)", "Needs SS core + weighted handle = higher unit cost", "Color fading complaints", "Commodity risk = race to bottom on price"],
        "market_context": "Home cooking remains strong. 'Chef-quality' positioning allows premium pricing."
    }
]

# Insert in batches
batch_size = 10
for i in range(0, len(niches), batch_size):
    batch = niches[i:i+batch_size]
    data = json.dumps(batch).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        print(f"Inserted {len(result)} niches (row {i+1}-{i+len(batch)})")
        for n in result:
            print(f"  - {n['niche_name']} (id={n['id']})")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR {e.code}: {body[:200]}")

print("Done!")
