import re, urllib.request, json

with open(r'C:\Users\Jack\Desktop\supplier-dashboard\index.html') as f:
    for line in f:
        if 'SUPABASE_ANON_KEY' in line and "= '" in line:
            m = re.search(r"'([^']+)'", line[line.index('='):])
            if m:
                key = m.group(1)
                break

try:
    req = urllib.request.Request(
        'https://yybpjnxudjptlnuswskt.supabase.co/rest/v1/daily_tasks?limit=1',
        headers={'apikey': key, 'Authorization': f'Bearer {key}'}
    )
    urllib.request.urlopen(req)
    print('EXISTS')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'MISSING: {body[:80]}')