// Dev server: při každém načtení přebuildí src/ → dist/index.html
// /api/hit a /api/stats nechává produkčnímu workeru. Tady je jen místnost klubu.
import http from "node:http";
import { readFileSync, existsSync } from "node:fs";
import { build } from "./build.mjs";

const PORT = Number(process.env.PORT) || 5454;
const ROOM = new Map();
const CHAT = [];
let lastCast = 0;
const CAST = [
  (dj) => `Pepa od dveří: „U pultu je ${dj || "někdo"}. Netlačte se a jméno řekněte nahlas.“`,
  (dj) => `Péťa od baru: „${dj || "DJ"} hraje. Voda je za šedesát, podpis je za náladu.“`,
  (dj) => `Denisa: „Kdo je tu poprvé, ať se podívá na plakát. Dneska to táhne ${dj || "pult"}.“`,
  (dj) => `Martina: „Na parketu je místo. ${dj || "DJ"} vás vidí, i když děláte, že ne.“`,
];

function readBody(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      try { resolve(JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}")); }
      catch { resolve({}); }
    });
  });
}

function clean(s, n) {
  return String(s || "").replace(/[\u0000-\u001f<>]/g, "").replace(/\s+/g, " ").trim().slice(0, n);
}

async function room(req, res) {
  const now = Date.now();
  if (req.method === "POST") {
    const b = await readBody(req);
    const id = clean(b.id, 16);
    const name = clean(b.name, 18);
    if (id && name) {
      const prev = ROOM.get(id);
      ROOM.set(id, { id, name, look: b.look && typeof b.look === "object" ? b.look : {}, loc: clean(b.loc, 12) || "dvere", seen: now, said: prev?.said || 0 });
      const say = clean(b.say, 140);
      const me = ROOM.get(id);
      if (say && now - me.said > 1200) {
        me.said = now;
        CHAT.push({ name, text: say, t: now, cast: false });
      }
      for (const [k, v] of ROOM) if (now - v.seen > 20000) ROOM.delete(k);
      if (ROOM.size && now - lastCast > 50000) {
        lastCast = now;
        const dj = clean(b.dj, 32);
        CHAT.push({ name: "Klub", text: CAST[Math.floor(Math.random() * CAST.length)](dj), t: now, cast: true });
      }
      while (CHAT.length > 40) CHAT.shift();
    }
  }
  const people = [...ROOM.values()].filter((p) => now - p.seen <= 20000).map(({ id, name, look, loc }) => ({ id, name, look, loc }));
  const chat = CHAT.slice(-30).map(({ name, text, t, cast }) => ({ name, text, t, cast }));
  res.writeHead(200, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }).end(JSON.stringify({ people, chat }));
}

http.createServer((req, res) => {
  const path = req.url.split("?")[0];
  if (path === "/api/room") { room(req, res); return; }
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
