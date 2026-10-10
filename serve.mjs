// Dev server: při každém načtení přebuildí src/ → dist/index.html
import http from "node:http";
import { readFileSync, existsSync } from "node:fs";
import { build } from "./build.mjs";

const PORT = Number(process.env.PORT) || 5454;

http.createServer((req, res) => {
  const path = req.url.split("?")[0];
  const MIME = { png: "image/png", jpg: "image/jpeg", ico: "image/x-icon", webmanifest: "application/manifest+json" };
  const ext = path.split(".").pop();
  if (path !== "/" && path !== "/index.html" && MIME[ext] && /^\/[\w.-]+$/.test(path) && existsSync("dist" + path)) {
    res.writeHead(200, { "Content-Type": MIME[ext] }).end(readFileSync("dist" + path));
    return;
  }
  if (path !== "/" && path !== "/index.html") {
    res.writeHead(404, { "Content-Type": "text/plain" }).end("404");
    return;
  }
  try {
    build();
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" });
    res.end(readFileSync("dist/index.html"));
  } catch (err) {
    console.error(err);
    res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" }).end(`Build selhal:\n${err.stack}`);
  }
}).listen(PORT, () => console.log(`Hra běží na http://localhost:${PORT}`));
