with open(r"C:\Users\Jack\Desktop\supplier-dashboard\index.html", "r") as f:
    content = f.read()

# 1. Replace side-nav HTML + old top-bar
old_header = """<body>

<!-- ===== LEFT NAV ===== -->
<nav class="side-nav">
  <div class="logo">📦</div>
  <a href="#suppliers" onclick="switchPage('suppliers')">
    <span class="nav-icon">📋</span><span>Suppliers</span>
  </a>
  <a href="#briefs" onclick="switchPage('briefs')">
    <span class="nav-icon">📝</span><span>Briefs</span>
  </a>
  <a href="#calendar" onclick="switchPage('calendar')">
    <span class="nav-icon">📅</span><span>Calendar</span>
  </a>
  <a href="#flow" onclick="switchPage('flow')">
      <span class="nav-icon">🗺️</span><span>Flow</span>
    </a>
    <a href="#sourcing" onclick="switchPage('sourcing')">
          <span class="nav-icon">🔍</span><span>Sourcing</span>
        </a>
        <a href="#spec" onclick="switchPage('spec')">
          <span class="nav-icon">📐</span><span>Spec</span>
        </a>
      </nav>

<!-- ===== MAIN ===== -->
<div class="main-area">

<div class="top-bar">
  <div>
    <h1>📦 JMPL Logistics</h1>
    <div class="subtitle">Amazon PL operations dashboard</div>
  </div>
  <button class="btn btn-primary" onclick="openAddModal()" id="addBtn" style="display:none">+ Add Supplier</button>
</div>"""

new_header = """<body>

<header class="top-bar">
  <div class="brand">
    <span style="font-size:22px">📦</span>
    <h1>JMPL Logistics</h1>
  </div>
  <nav class="top-nav">
    <a href="#suppliers" class="active" onclick="switchPage('suppliers')">📋 Suppliers</a>
    <a href="#calendar" onclick="switchPage('calendar')">📅 Calendar</a>
    <a href="#flow" onclick="switchPage('flow')">🗺️ Flow</a>
  </nav>
</header>

<div class="main-area">"""

assert old_header in content, "old_header not found!"
content = content.replace(old_header, new_header)
print("1. Header replaced")

# 2. Remove briefs page HTML
old_briefs = """<!-- BRIEFS PAGE -->
<div id="page-briefs" class="page">
  <div class="briefs-layout">
    <div class="briefs-sidebar">
      <h3>📅 Daily Briefs</h3>
      <div id="briefList"></div>
    </div>
    <div class="briefs-chat" id="briefChat">
      <div class="loading"><div class="spinner"></div><div>Loading briefs...</div></div>
    </div>
  </div>
</div>"""

assert old_briefs in content, "old_briefs not found!"
content = content.replace(old_briefs, "")
print("2. Briefs page removed")

# 3. Remove briefs CSS
old_briefs_css = """  /* ===== BRIEFS PAGE ===== */
  .briefs-layout { display: flex; flex: 1; overflow: hidden; }
  .briefs-sidebar {
    width: 200px; flex-shrink: 0; background: var(--surface);
    border-right: 1px solid var(--border); overflow-y: auto; padding: 12px;
  }
  .briefs-sidebar h3 { font-size: 11px; text-transform: uppercase; letter-spacing: .5px; color: var(--text2); margin-bottom: 8px; padding: 0 4px; }
  .briefs-sidebar .brief-list-item {
    padding: 7px 8px; border-radius: 6px; cursor: pointer; font-size: 12px;
    color: var(--text2); transition: all .1s; margin-bottom: 2px;
  }
  .briefs-sidebar .brief-list-item:hover { background: var(--surface2); color: var(--text); }
  .briefs-sidebar .brief-list-item.active { background: var(--accent); color: white; }
  .briefs-sidebar .brief-list-item .date-label { font-weight: 600; }
  .briefs-sidebar .brief-list-item .title-preview { font-size: 10px; opacity: .7; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .briefs-chat { flex: 1; overflow-y: auto; padding: 24px 32px; display: flex; flex-direction: column; gap: 16px; }
  .brief-entry {
    background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
    padding: 20px 24px; max-width: 720px; align-self: flex-start; width: 100%;
  }
  .brief-entry .brief-date-header { font-size: 13px; font-weight: 600; color: var(--accent); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
  .brief-entry .brief-date-header .title { color: var(--text); font-size: 15px; }
  .brief-empty { text-align: center; padding: 60px 20px; color: var(--text2); }
  .brief-empty .icon { font-size: 40px; margin-bottom: 10px; }
  .brief-empty h3 { font-size: 16px; color: var(--text); margin-bottom: 4px; }
  .brief-empty p { font-size: 13px; }
"""

assert old_briefs_css in content, "old_briefs_css not found!"
content = content.replace(old_briefs_css, "")
print("3. Briefs CSS removed")

# 4. Remove side-nav CSS
old_side_css = """  /* ===== LEFT NAV ===== */
  .side-nav {
    width: 72px; flex-shrink: 0; background: var(--surface);
    border-right: 1px solid var(--border); display: flex;
    flex-direction: column; align-items: center; padding: 16px 0;
    position: sticky; top: 0; height: 100vh;
  }
  .side-nav .logo { font-size: 24px; margin-bottom: 24px; cursor: default; }
  .side-nav a {
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    padding: 12px 8px; margin: 2px 0; border-radius: 10px;
    color: var(--text2); text-decoration: none; cursor: pointer;
    transition: all .15s; font-size: 11px; width: 56px;
  }
  .side-nav a:hover { color: var(--text); background: var(--surface2); }
  .side-nav a.active { color: var(--accent); background: var(--surface2); }
  .side-nav a .nav-icon { font-size: 20px; }"""

if old_side_css in content:
    content = content.replace(old_side_css, "")
    print("4. Side-nav CSS removed")
else:
    print("4. Side-nav CSS NOT found (might already be removed)")

# 5. Update body
content = content.replace("min-height: 100vh; display: flex; }",
                         "min-height: 100vh; display: flex; flex-direction: column; }")
print("5. Body updated")

# 6. Replace top-bar CSS with new version
old_top_css = """  .main-area { flex: 1; display: flex; flex-direction: column; min-width: 0; }
  .top-bar {
    background: var(--surface); border-bottom: 1px solid var(--border);
    padding: 12px 24px; display: flex; align-items: center;
    justify-content: space-between; flex-shrink: 0;
  }
  .top-bar h1 { font-size: 18px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
  .top-bar .subtitle { font-size: 12px; color: var(--text2); }"""

new_top_css = """  .main-area { flex: 1; display: flex; flex-direction: column; min-width: 0; }
  .top-bar {
    background: var(--surface); border-bottom: 1px solid var(--border);
    padding: 10px 24px; display: flex; align-items: center; gap: 20px; flex-shrink: 0;
  }
  .top-bar .brand { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
  .top-bar .brand h1 { font-size: 18px; font-weight: 600; display: flex; align-items: center; gap: 6px; margin:0; }
  .top-nav { display: flex; align-items: center; gap: 4px; flex:1; }
  .top-nav a {
    padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 500;
    color: var(--text2); text-decoration: none; cursor: pointer; transition: all .15s;
    display: flex; align-items: center; gap: 5px;
  }
  .top-nav a:hover { color: var(--text); background: var(--surface2); }
  .top-nav a.active { color: white; background: var(--accent); }"""

assert old_top_css in content, "old_top_css not found!"
content = content.replace(old_top_css, new_top_css)
print("6. Top CSS updated")

# 7. Remove briefs from media queries
old_mq = """    .briefs-layout { flex-direction: column; }
    .briefs-sidebar { width: 100%; max-height: 120px; border-right: none; border-bottom: 1px solid var(--border); }
    .briefs-chat { padding: 12px 16px; }
    .brief-entry { padding: 14px 16px; }"""
if old_mq in content:
    content = content.replace(old_mq, "")
    print("7. Media queries cleaned")

# 8. Remove briefs switchPage call
content = content.replace("if (name === 'briefs') loadBriefs();", "")
print("8. Briefs switch removed")

# 9. Update JS nav selectors
content = content.replace("document.querySelectorAll('.side-nav a').forEach(function(a) { a.classList.remove('active'); });",
                         "document.querySelectorAll('.top-nav a').forEach(function(a) { a.classList.remove('active'); });")
content = content.replace("var link = document.querySelector('.side-nav a[href=\"#' + name + '\"]');",
                         "var link = document.querySelector('.top-nav a[href=\"#' + name + '\"]');")
print("9. Nav selectors updated")

# 10. Remove addBtn line
content = content.replace("document.getElementById('addBtn').style.display = name === 'suppliers' ? '' : 'none';", "")
print("10. addBtn removed")

# 11. Remove side-nav from media queries
old_side_mq = """    .side-nav { width: 56px; }
    .side-nav a { width: 44px; padding: 8px 4px; font-size: 10px; }
    .side-nav a .nav-icon { font-size: 16px; }"""
if old_side_mq in content:
    content = content.replace(old_side_mq, "")
    print("11. Side-nav media queries removed")

with open(r"C:\Users\Jack\Desktop\supplier-dashboard\index.html", "w") as f:
    f.write(content)
print("\n✅ DONE - all changes written!")
