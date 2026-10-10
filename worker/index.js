// Studio 54 hra – statické soubory + počítadlo návštěv a odehraných her (D1)
const PLAY_CAP = 30; // max započítaných her z jedné IP za den
const JSON_H = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" };

const day = () => new Date().toISOString().slice(0, 10);

async function ipHash(req, env) {
  const ip = req.headers.get("cf-connecting-ip") || "0.0.0.0";
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`${env.SALT || "s54"}|${day()}|${ip}`));
  return [...new Uint8Array(buf).slice(0, 12)].map(b => b.toString(16).padStart(2, "0")).join("");
}

async function stats(env) {
  const { results } = await env.DB.prepare("SELECT k, n FROM counters").all();
  const o = { visits: 0, plays: 0 };
  for (const r of results || []) { if (r.k === "visit") o.visits = r.n; if (r.k === "play") o.plays = r.n; }
  return o;
}

async function hit(req, env, ctx) {
  let k = "";
  try { k = String((await req.json())?.k || ""); } catch { /* prázdné tělo */ }
  if (k !== "visit" && k !== "play") return new Response(JSON.stringify({ error: "bad kind" }), { status: 400, headers: JSON_H });
  const d = day(), h = await ipHash(req, env);
  const row = await env.DB.prepare(
    "INSERT INTO seen (d, h, k, n) VALUES (?1, ?2, ?3, 1) ON CONFLICT (d, h, k) DO UPDATE SET n = n + 1 RETURNING n"
  ).bind(d, h, k).first();
  const n = row?.n ?? 1;
  const count = k === "visit" ? n === 1 : n <= PLAY_CAP;
  if (count) await env.DB.prepare("UPDATE counters SET n = n + 1 WHERE k = ?1").bind(k).run();
  // úklid starých otisků (jen dnešek a včerejšek mají smysl)
  if (Math.random() < 0.02) ctx.waitUntil(env.DB.prepare("DELETE FROM seen WHERE d < ?1").bind(new Date(Date.now() - 2 * 864e5).toISOString().slice(0, 10)).run());
  return new Response(JSON.stringify(await stats(env)), { headers: JSON_H });
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/")) {
      try {
        if (url.pathname === "/api/stats" && req.method === "GET")
          return new Response(JSON.stringify(await stats(env)), { headers: { ...JSON_H, "cache-control": "public, max-age=30" } });
        if (url.pathname === "/api/hit" && req.method === "POST") return await hit(req, env, ctx);
        return new Response(JSON.stringify({ error: "not found" }), { status: 404, headers: JSON_H });
      } catch (e) {
        return new Response(JSON.stringify({ error: "server" }), { status: 500, headers: JSON_H });
      }
    }
    return env.ASSETS.fetch(req);
  },
};
