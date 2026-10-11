"""Regenerate dashboard.js from data.js, charts.js and app.js (all in this folder).

Usage: python build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = "/* FrPD Dashboard browser bundle. Source modules: data.js, charts.js, app.js. */\n'use strict';\n"
for name in ('data.js', 'charts.js', 'app.js'):
    source = (ROOT / name).read_text(encoding='utf8')
    source = '\n'.join(line for line in source.splitlines() if not line.startswith('import '))
    for token, replacement in (
        ('export const ', 'const '),
        ('export function ', 'function '),
        ('export async function ', 'async function '),
    ):
        source = source.replace(token, replacement)
    out += f'\n/* {name} */\n{source}\n'
(ROOT / 'dashboard.js').write_text(out, encoding='utf8')
print('Built dashboard.js')
