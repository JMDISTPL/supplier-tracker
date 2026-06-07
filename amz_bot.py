#!/usr/bin/env python3
"""
Amazon PL Bot — Ingestion & Q&A Tool

Usage:
  python amz_bot.py ingest youtube <URL> [--title "Title"]
  python amz_bot.py ingest pdf <FILE> [--title "Title"]
  python amz_bot.py ingest text "<content>" --type tiktok --title "Title" [--url URL]
  python amz_bot.py ask "<question>"
  python amz_bot.py serve       # Start web API server

Environment:
  OPENROUTER_API_KEY  — required (already set in Hermes)
  SUPABASE_KEY        — reads from dashboard index.html if not set
"""
import argparse, json, os, re, sys, textwrap, urllib.request

# ─── Config ───────────────────────────────────────────────────
SUPABASE_URL = "https://yybpjnxudjptlnuswskt.supabase.co"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "") or os.environ.get("HERMES_OPENROUTER_KEY", "")
OPENROUTER_MODEL = "openai/gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMS = 1536
HTML_PATH = os.path.expanduser("~/Desktop/supplier-dashboard/index.html")

# ─── Supabase Key ─────────────────────────────────────────────
def get_supabase_key():
    """Read the Supabase anon key from the dashboard HTML file."""
    if os.environ.get("SUPABASE_KEY"):
        return os.environ["SUPABASE_KEY"]
    if not os.path.exists(HTML_PATH):
        # Try alternative path
        alt = os.path.expanduser("~/supplier-tracker/index.html")
        if os.path.exists(alt):
            html_path = alt
        else:
            raise RuntimeError(f"Cannot find dashboard HTML. Set SUPABASE_KEY env var.")
    else:
        html_path = HTML_PATH
    with open(html_path) as f:
        for line in f:
            if "SUPABASE_ANON_KEY" in line and "= " in line:
                idx = line.index("=")
                m = re.search(r"'([^']+)'", line[idx:])
                if m:
                    return m.group(1)
    raise RuntimeError("Could not extract Supabase anon key from HTML.")

# ─── OpenRouter API ───────────────────────────────────────────
def call_openrouter(payload):
    """Call OpenRouter API and return parsed JSON."""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jmdistpl.github.io/supplier-tracker",
        }
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

def embed_texts(texts):
    """Get embeddings for a list of texts via OpenRouter."""
    data = json.dumps({
        "model": EMBEDDING_MODEL,
        "input": texts
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/embeddings",
        data=data,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    return [item["embedding"] for item in resp["data"]]

def ask_llm(system_prompt, user_prompt):
    """Ask the LLM a question with context."""
    result = call_openrouter({
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    })
    return result["choices"][0]["message"]["content"]

# ─── Supabase API ─────────────────────────────────────────────
def supabase_api(method, path, body=None):
    """Call Supabase REST API."""
    key = get_supabase_key()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if body is not None:
        headers["Prefer"] = "return=representation"
        data = json.dumps(body).encode()
    else:
        data = None
    req = urllib.request.Request(
        f"{SUPABASE_URL}{path}",
        data=data, headers=headers, method=method
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

def search_knowledge(query_embedding, threshold=0.7, count=5):
    """Search knowledge chunks by vector similarity."""
    return supabase_api("POST", "/rest/v1/rpc/match_knowledge", {
        "query_embedding": query_embedding,
        "match_threshold": threshold,
        "match_count": count,
    })

def store_chunks(chunks, source_type, source_url, source_title):
    """Store multiple chunks in Supabase."""
    if not chunks:
        return
    embeddings = embed_texts([c["content"] for c in chunks])
    records = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        records.append({
            "content": chunk["content"],
            "embedding": emb,
            "source_type": source_type,
            "source_url": source_url,
            "source_title": source_title,
            "chunk_index": i,
            "metadata": chunk.get("metadata", {}),
        })
    batched = supabase_api("POST", "/rest/v1/knowledge_chunks", records)
    print(f"  Stored {len(batched)} chunks ✓")

# ─── Chunking ─────────────────────────────────────────────────
def chunk_text(text, max_chars=1200, overlap=150):
    """Split text into overlapping chunks of ~max_chars."""
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = []
    curr_len = 0
    for sent in sentences:
        sent_len = len(sent)
        if curr_len + sent_len > max_chars and current:
            chunk_text = " ".join(current)
            chunks.append({"content": chunk_text, "metadata": {}})
            # Keep overlap sentences
            overlap_text = ""
            overlap_len = 0
            kept = []
            for s in reversed(current):
                if overlap_len + len(s) > overlap:
                    break
                kept.insert(0, s)
                overlap_len += len(s)
            current = kept
            curr_len = overlap_len
        current.append(sent)
        curr_len += sent_len
    if current:
        chunks.append({"content": " ".join(current), "metadata": {}})
    return chunks

# ─── Ingest: YouTube ──────────────────────────────────────────
def ingest_youtube(url, title=None):
    """Fetch YouTube transcript and store as knowledge."""
    import subprocess
    script = os.path.expanduser(
        "~/AppData/Local/hermes/skills/media/youtube-content/scripts/fetch_transcript.py"
    )
    result = subprocess.run(
        ["python", script, url, "--text-only", "--timestamps"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0 or not result.stdout.strip():
        try:
            err = json.loads(result.stdout)
            print(f"  ✗ YouTube error: {err.get('error', 'unknown')}")
            return
        except:
            print(f"  ✗ YouTube fetch failed")
            return
    text = result.stdout.strip()
    if not title:
        # Get title from oEmbed
        try:
            req = urllib.request.Request(
                f"https://noembed.com/embed?url={url}", headers={"User-Agent": "Mozilla/5.0"}
            )
            info = json.loads(urllib.request.urlopen(req).read())
            title = info.get("title", url)
        except:
            title = url
    print(f"  Title: {title}")
    print(f"  Text length: {len(text)} chars")
    chunks = chunk_text(text)
    store_chunks(chunks, "youtube", url, title)

# ─── Ingest: PDF ──────────────────────────────────────────────
def ingest_pdf(filepath, title=None):
    """Extract PDF text and store as knowledge."""
    try:
        import pymupdf
    except ImportError:
        print("  Installing pymupdf...")
        import subprocess
        subprocess.run(["uv", "pip", "install", "pymupdf"], check=True)
        import pymupdf
    doc = pymupdf.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()
    if not full_text.strip():
        print(f"  ✗ No text extracted from PDF")
        return
    name = title or os.path.basename(filepath)
    print(f"  Title: {name}")
    print(f"  Text length: {len(full_text)} chars")
    chunks = chunk_text(full_text)
    store_chunks(chunks, "pdf", filepath, name)

# ─── Ingest: Text (TikTok/Reel/manual) ────────────────────────
def ingest_text(content, source_type, title, url=None):
    """Store text content (TikTok, Reel, manual notes) as knowledge."""
    if not content.strip():
        print("  ✗ Empty content")
        return
    print(f"  Title: {title}")
    print(f"  Text length: {len(content)} chars")
    chunks = chunk_text(content)
    store_chunks(chunks, source_type, url or "", title)

# ─── Ask ───────────────────────────────────────────────────────
def ask_question(question, show_sources=True):
    """Ask a question and get an answer grounded in the knowledge base."""
    print(f"\n🔍 Searching knowledge base for: {question}")
    
    # Embed the question
    [embedding] = embed_texts([question])
    
    # Search
    results = search_knowledge(embedding, threshold=0.65, count=5)
    if not results:
        print("  No relevant knowledge found. Answering from general knowledge...\n")
        answer = ask_llm(
            "You are an Amazon Private Label expert assistant. Answer the user's question based on your knowledge of Amazon FBA.",
            question
        )
        print(f"🤖 {answer}\n")
        return
    
    # Build context from results
    context_parts = []
    sources = []
    for r in results:
        context_parts.append(f"[{r['source_type'].upper()}] {r['source_title']}:\n{r['content']}")
        sources.append({
            "type": r["source_type"],
            "title": r["source_title"],
            "url": r.get("source_url", ""),
            "similarity": round(r["similarity"], 3),
        })
    context = "\n\n---\n\n".join(context_parts)
    
    # Generate answer
    system_prompt = textwrap.dedent(f"""\
    You are an Amazon Private Label expert. Your knowledge comes from a curated library of 
    training content including YouTube videos, PDFs, and expert notes.
    
    Answer the user's question using ONLY the provided context. If the context doesn't contain 
    enough information, say so — don't make things up. Be specific with numbers, percentages, 
    and actionable advice. Format your answer with clear sections when appropriate.
    """)
    user_prompt = f"CONTEXT:\n{context}\n\n---\n\nQUESTION: {question}"
    
    print(f"  Found {len(results)} relevant passages. Generating answer...\n")
    answer = ask_llm(system_prompt, user_prompt)
    print(f"🤖 {answer}\n")
    
    if show_sources and sources:
        print("📚 Sources:")
        for s in sources:
            url_str = f" - {s['url']}" if s['url'] else ""
            print(f"  [{s['type']}] {s['title']}{url_str} (relevance: {s['similarity']*100:.0f}%)")
    
    # Save to chat history
    try:
        supabase_api("POST", "/rest/v1/chat_history", {
            "question": question,
            "answer": answer,
            "sources": sources,
        })
    except:
        pass  # non-critical
    
    return answer, sources

# ─── Serve (web API) ──────────────────────────────────────────
def serve():
    """Start a simple HTTP API server for the web UI."""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
    except ImportError:
        print("Starting API server...")
    
    class BotHandler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            if self.path == "/ask":
                q = body.get("question", "")
                try:
                    answer, sources = ask_question(q, show_sources=False)
                    self.wfile.write(json.dumps({"answer": answer, "sources": sources}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            elif self.path == "/health":
                self.wfile.write(json.dumps({"status": "ok"}).encode())
            else:
                self.wfile.write(json.dumps({"error": "not found"}).encode())
    
    port = 8899
    server = HTTPServer(("0.0.0.0", port), BotHandler)
    print(f"🌐 Amazon PL Bot API running on http://localhost:{port}")
    print(f"   POST /ask  {{'question': '...'}}")
    print(f"   GET  /health")
    server.serve_forever()

# ─── CLI ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Amazon PL Bot — Ingestion & Q&A")
    sub = parser.add_subparsers(dest="command")
    
    # ingest
    ingest = sub.add_parser("ingest")
    ingest.add_argument("source", choices=["youtube", "pdf", "text"])
    ingest.add_argument("input", help="URL (youtube), file path (pdf), or content (text)")
    ingest.add_argument("--title", "-t", help="Source title")
    ingest.add_argument("--type", dest="stype", help="Source type for text (tiktok, reel, manual)")
    ingest.add_argument("--url", help="Source URL for text input")
    
    # ask
    ask = sub.add_parser("ask")
    ask.add_argument("question", help="Question to ask the bot")
    
    # serve
    sub.add_parser("serve", help="Start web API server")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        print(f"\n📥 Ingesting {args.source}...")
        if args.source == "youtube":
            ingest_youtube(args.input, args.title)
        elif args.source == "pdf":
            ingest_pdf(args.input, args.title)
        elif args.source == "text":
            stype = args.stype or "manual"
            ingest_text(args.input, stype, args.title or "Untitled", args.url)
        print("✅ Done!\n")
    
    elif args.command == "ask":
        ask_question(args.question)
    
    elif args.command == "serve":
        serve()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()