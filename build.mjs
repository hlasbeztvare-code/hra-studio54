// Zabalí src/ zpět do jednoho souboru dist/index.html (stejný formát jako produkce)
import fs from "node:fs";
import zlib from "node:zlib";

const replaceBlock = (html, t, content) => {
  const open = `<script type="__bundler/${t}">`;
  const i = html.indexOf(open);
  if (i < 0) throw new Error(`Chybí blok ${t}`);
  const j = html.indexOf("</script>", i);
  return html.slice(0, i + open.length) + content + html.slice(j);
};

// Escapování, aby obsah nemohl ukončit <script> blok
const safeJson = (v) => JSON.stringify(v).replaceAll("</", "<" + String.fromCharCode(92) + "u002F");

export function build() {
  fs.mkdirSync("dist", { recursive: true });
  let html = fs.readFileSync("deploy/original.html", "utf8");
  const index = JSON.parse(fs.readFileSync("src/assets.json", "utf8"));
  const manifest = {};
  const tpl = fs.readFileSync("src/template.html", "utf8");
  const ext = JSON.parse(fs.readFileSync("src/ext_resources.json", "utf8"));
  const idOf = Object.fromEntries(ext.map((r) => [r.uuid, r.id]));
  // jen aktiva, na která šablona odkazuje (uuid nebo id), a skripty runtime
  const used = (uuid, mime) => mime.includes("javascript") || tpl.includes(uuid) || (idOf[uuid] && tpl.includes(idOf[uuid]));
  let skipped = 0;
  for (const [uuid, { file, mime }] of Object.entries(index)) {
    if (!used(uuid, mime)) { skipped++; continue; }
    const buf = fs.readFileSync(`src/assets/${file}`);
    manifest[uuid] = { mime, compressed: true, data: zlib.gzipSync(buf, { level: 9 }).toString("base64") };
  }
  if (skipped) console.log(`vynecháno nepoužitých aktiv: ${skipped}`);
  const BUILD_V = String(Date.now());
  const d = new Date();
  const z = (n) => String(n).padStart(2, "0");
  const BUILD_SHORT = `${d.getFullYear()}${z(d.getMonth() + 1)}${z(d.getDate())}-${z(d.getHours())}${z(d.getMinutes())}`;
  html = replaceBlock(html, "manifest", JSON.stringify(manifest));
  const tpl2 = fs.readFileSync("src/template.html", "utf8")
    .replaceAll("__BUILD_V__", BUILD_V)
    .replaceAll("__BUILD_SHORT__", BUILD_SHORT);
  html = replaceBlock(html, "template", safeJson(tpl2));
  html = replaceBlock(html, "ext_resources", JSON.stringify(JSON.parse(fs.readFileSync("src/ext_resources.json", "utf8"))));
  fs.writeFileSync("dist/index.html", html);
  // DŮLEŽITÉ: wrangler nasazuje ./deploy, takže index.html musí být i tam
  if (fs.existsSync("deploy")) fs.writeFileSync("deploy/index.html", html);
  // náhledový obrázek pro sdílení odkazu (og:image) – musí ležet vedle index.html
  if (fs.existsSync("src/og.jpg")) fs.copyFileSync("src/og.jpg", "dist/og.jpg");
  if (fs.existsSync("src/favicon.ico")) fs.copyFileSync("src/favicon.ico", "dist/favicon.ico");
  // instalace na plochu: manifest + ikony vedle index.html
  if (fs.existsSync("src/pwa")) for (const f of fs.readdirSync("src/pwa")) fs.copyFileSync(`src/pwa/${f}`, `dist/${f}`);
  return html.length;
}

if (process.argv[1]?.endsWith("build.mjs")) {
  console.log(`dist/index.html: ${build()} B`);
}
