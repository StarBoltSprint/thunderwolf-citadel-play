import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const root = path.dirname(fileURLToPath(import.meta.url));
function walk(d) {
  for (const f of fs.readdirSync(d)) {
    const p = path.join(d, f);
    if (fs.statSync(p).isDirectory()) walk(p);
    else if (p.endsWith('.js') && !p.includes('three.module') && !p.includes('three.min') && !p.includes('fix-imports')) {
      const t = fs.readFileSync(p, 'utf8');
      const m = [...t.matchAll(/from ['"]([^'"]+)['"]/g)];
      if (m.length) {
        console.log(path.relative(root, p));
        m.forEach((x) => console.log('  ', x[1]));
      }
    }
  }
}
walk(root);
