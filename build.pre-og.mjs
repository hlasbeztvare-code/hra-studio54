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
  let html = fs.readFileSync("dist/original.html", "utf8");
  const index = JSON.parse(fs.readFileSync("src/assets.json", "utf8"));
  const manifest = {};
  for (const [uuid, { file, mime }] of Object.entries(index)) {
    const buf = fs.readFileSync(`src/assets/${file}`);
    manifest[uuid] = { mime, compressed: true, data: zlib.gzipSync(buf, { level: 9 }).toString("base64") };
  }
  html = replaceBlock(html, "manifest", JSON.stringify(manifest));
  html = replaceBlock(html, "template", safeJson(fs.readFileSync("src/template.html", "utf8")));
  html = replaceBlock(html, "ext_resources", JSON.stringify(JSON.parse(fs.readFileSync("src/ext_resources.json", "utf8"))));
  fs.writeFileSync("dist/index.html", html);
  return html.length;
}

if (process.argv[1]?.endsWith("build.mjs")) {
  console.log(`dist/index.html: ${build()} B`);
}
