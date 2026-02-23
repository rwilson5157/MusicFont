# MusicFont

MusicFont is a small local utility to view and explore SMuFL glyph metadata (`glyphnames.json`) using the Bravura music font.

Features
- Serves an interactive searchable HTML table built from `glyphnames.json`.
- Renders musical glyphs using the installed `Bravura` / `Bravura Text` fonts so you can see the actual symbol.
- Shows glyph name, Unicode codepoint, HTML entity and description.
- Client-side search, copy-visible-names, and single-row selection with "Copy selected" to copy a glyph's Unicode value.

Usage
1. Start the server in this folder:

```bash
python3 render_glyphnames.py
```

2. Open the page (the script will try to open it automatically):

```bash
open http://localhost:8001/
```

Notes
- Requires a local copy of `glyphnames.json` in the same folder. The script will fall back to a bundled `bravura_character_table.html` if present.
- No external Python dependencies; uses the standard library HTTP server.

License
Add your preferred license here.
