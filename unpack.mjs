// Rozbalí bundlovaný index.html do src/ (template + assety)
import fs from "node:fs";
import zlib from "node:zlib";

const html = fs.readFileSync(process.argv[2] || "dist/original.html", "utf8");
const block = (t) => {
  const i = html.indexOf(`<script type="__bundler/${t}">`);
  if (i < 0) throw new Error(`Chybí blok ${t}`);
  return html.slice(html.indexOf(">", i) + 1, html.indexOf("</script>", i));
};

const EXT = { "image/svg+xml": "svg", "image/webp": "webp", "image/png": "png", "image/jpeg": "jpg",
  "font/woff2": "woff2", "application/javascript": "js", "text/javascript": "js", "text/css": "css",
  "audio/mpeg": "mp3", "audio/wav": "wav" };

const manifest = JSON.parse(block("manifest"));
const index = {};
for (const [uuid, e] of Object.entries(manifest)) {
  let buf = Buffer.from(e.data, "base64");
  if (e.compressed) buf = zlib.gunzipSync(buf);
  const file = `${uuid}.${EXT[e.mime] || "bin"}`;
  fs.writeFileSync(`src/assets/${file}`, buf);
  index[uuid] = { file, mime: e.mime };
}
fs.writeFileSync("src/assets.json", JSON.stringify(index, null, 2));
fs.writeFileSync("src/template.html", JSON.parse(block("template")));
fs.writeFileSync("src/ext_resources.json", JSON.stringify(JSON.parse(block("ext_resources")), null, 2));
console.log(`Rozbaleno: ${Object.keys(index).length} assetů, template ${fs.statSync("src/template.html").size} B`);
