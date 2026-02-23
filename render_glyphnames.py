#!/usr/bin/env python3
"""Serve glyphnames.json as a simple searchable HTML page.

Run: python3 render_glyphnames.py
Then open http://localhost:8000 in your browser (the script opens it automatically).
"""
import json
import html as _html
import os
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(__file__)
JSON_PATH = os.path.join(ROOT, "glyphnames.json")
PORT = 8001


def load_glyphs():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    rows = []
    if isinstance(data, dict):
        for name, info in data.items():
            if isinstance(info, dict):
                codepoint = info.get("codepoint", "") or ""
                description = info.get("description", "") or ""
            else:
                codepoint = ""
                description = ""
            rows.append({"name": name, "codepoint": codepoint, "description": description})
        return rows

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "name" in item:
                rows.append({
                    "name": item.get("name"),
                    "codepoint": item.get("codepoint", "") or "",
                    "description": item.get("description", "") or "",
                })
            else:
                rows.append({"name": str(item), "codepoint": "", "description": ""})
        return rows

    return [{"name": str(data), "codepoint": "", "description": ""}]


def build_html(rows):
        # Build table rows server-side so the page can show samples, names and codepoints.
        row_html_parts = []
        for item in rows:
                name = _html.escape(item.get("name", ""))
                cp = (item.get("codepoint") or "").upper()
                desc = _html.escape(item.get("description", ""))
                sample = ""
                entity = ""
                if cp.startswith("U+"):
                        hexpart = cp[2:]
                        try:
                                code = int(hexpart, 16)
                                sample = chr(code)
                                entity = f"&#x{hexpart};"
                        except Exception:
                                sample = ""
                                entity = ""

                row_html_parts.append(
                        f"<tr>"
                        f"<td class=\"symbol\">{_html.escape(sample)}</td>"
                        f"<td class=\"mono\">{name}</td>"
                        f"<td class=\"mono\">{_html.escape(cp)}</td>"
                        f"<td class=\"mono\">{entity}</td>"
                        f"<td>{desc}</td>"
                        f"</tr>"
                )

        rows_html = "\n".join(row_html_parts)
        total = len(rows)
        html = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Glyph Names (Bravura)</title>
    <style>
        body{{margin:16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#111}}
        .container{{max-width:1200px;margin:0 auto}}
        .controls{{display:flex;gap:8px;margin-bottom:12px}}
        input.search{{flex:1;padding:8px;border:1px solid #ddd;border-radius:6px}}
        table{{width:100%;border-collapse:collapse}}
        thead th{{text-align:left;border-bottom:1px solid #ddd;padding:8px;background:#f8f8f8}}
        tbody td{{padding:8px;border-bottom:1px solid #eee;vertical-align:middle}}
        .symbol{{font-family:'Bravura Text','Bravura',serif;font-size:28px;width:72px}}
        .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','Courier New',monospace}}
        .count{{color:#666;margin-left:8px}}
    </style>
</head>
<body>
    <div class="container">
        <h1>Glyph Names (Bravura)</h1>
        <div class="controls">
            <input id="search" class="search" placeholder="Search by name, U+codepoint, or description">
            <button id="copyBtn" type="button">Copy visible names</button>
            <button id="copySelectedBtn" type="button" disabled>Copy selected</button>
            <div class="count">Total: {total}</div>
        </div>

        <div style="overflow:auto;max-height:72vh;border:1px solid #eee;border-radius:8px;background:#fff;padding:6px">
            <table>
                <thead>
                    <tr><th>Sample</th><th>Glyph name</th><th>Unicode</th><th>HTML entity</th><th>Description</th></tr>
                </thead>
                <tbody id="rows">
{rows_html}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        const search = document.getElementById('search');
        const rows = document.getElementById('rows');
        const copySelectedBtn = document.getElementById('copySelectedBtn');
        function filter() {{
            const q = search.value.trim().toLowerCase();
            const trs = rows.querySelectorAll('tr');
            let shown = 0;
            trs.forEach(tr => {{
                const text = tr.textContent.toLowerCase();
                const ok = !q || text.includes(q);
                tr.style.display = ok ? '' : 'none';
                if (ok) shown++;
            }});
            // If the selected row is hidden by filter, clear selection
            const sel = rows.querySelector('tr.selected');
            if (sel && sel.style.display === 'none') {{
                sel.classList.remove('selected');
                copySelectedBtn.disabled = true;
            }}
            document.querySelector('.count').textContent = 'Showing: ' + shown + ' / ' + {total};
        }}
        search.addEventListener('input', filter);
        // Copy only the selected row: include codepoint, HTML entity, and name (space-separated)
        document.getElementById('copyBtn').addEventListener('click', async () => {
            const sel = rows.querySelector('tr.selected');
            if (!sel) return;
            const code = sel.children[2].textContent.trim();
            const entity = sel.children[3].textContent.trim();
            const name = sel.children[1].textContent.trim();
            const text = [(code || ''), (entity || ''), name].filter(Boolean).join(' ');
            try {
                await navigator.clipboard.writeText(text);
                const b = document.getElementById('copyBtn');
                const old = b.textContent;
                b.textContent = 'Copied';
                setTimeout(() => b.textContent = old, 1200);
            } catch (err) {
                alert('Copy failed: ' + err);
            }
        });

        // Single-row selection logic for copying selected codepoint
        function clearSelection() {{
            const prev = rows.querySelector('tr.selected');
            if (prev) prev.classList.remove('selected');
            copySelectedBtn.disabled = true;
            document.getElementById('copyBtn').disabled = true;
        }}

        function attachRowHandlers() {{
            Array.from(rows.querySelectorAll('tr')).forEach(tr => {{
                tr.style.cursor = 'pointer';
                tr.addEventListener('click', () => {{
                    if (tr.classList.contains('selected')) {{
                        tr.classList.remove('selected');
                        copySelectedBtn.disabled = true;
                        return;
                    }}
                    clearSelection();
                    tr.classList.add('selected');
                    copySelectedBtn.disabled = false;
                    document.getElementById('copyBtn').disabled = false;
                }});
            }});
        }}

        attachRowHandlers();

        copySelectedBtn.addEventListener('click', async () => {
            const sel = rows.querySelector('tr.selected');
            if (!sel) return;
            const code = sel.children[2].textContent.trim();
            const name = sel.children[1].textContent.trim();
            const text = (code ? code + ' ' : '') + name;
            try {
                await navigator.clipboard.writeText(text);
                const old = copySelectedBtn.textContent;
                copySelectedBtn.textContent = 'Copied';
                setTimeout(() => copySelectedBtn.textContent = old, 1200);
            } catch (err) {
                alert('Copy failed: ' + err);
            }
        });
    </script>
</body>
</html>
"""

        # Convert doubled braces (used previously for f-string escaping) to single braces
        html = html.replace('{{', '{').replace('}}', '}')
        # Inject generated rows and totals
        html = html.replace('{rows_html}', rows_html).replace('{total}', str(total))
        return html


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            # Prefer shipping the existing Bravura character table if available
            table_path = os.path.join(ROOT, 'bravura_character_table.html')
            if os.path.exists(table_path):
                with open(table_path, 'rb') as f:
                    encoded = f.read()
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return

            glyphs = load_glyphs()
            html = build_html(glyphs)
            encoded = html.encode('utf-8')
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return

        return super().do_GET()


def main():
    addr = ('', PORT)
    server = ThreadingHTTPServer(addr, Handler)
    url = f'http://localhost:{PORT}/'
    print(f'Serving glyphnames.json at {url} (press Ctrl-C to stop)')
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping server')
        server.server_close()


if __name__ == '__main__':
    main()
