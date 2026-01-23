from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.core.mqtt_bridge import WS_CLIENTS

router = APIRouter()

_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>NutryGym Notifications Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    body { font-family: Arial, sans-serif; margin: 16px; }
    .top { display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
    .pill { padding:6px 10px; border:1px solid #ccc; border-radius:999px; }
    .cards { margin-top: 16px; display:flex; flex-direction:column; gap:10px; }
    .card { border:1px solid #ddd; border-radius:10px; padding:12px; }
    .title { font-weight:700; margin-bottom:6px; }
    .meta { font-size: 12px; color:#555; margin-top:6px; }
    .sev-info { border-left:6px solid #2f7; }
    .sev-warning { border-left:6px solid #fb2; }
    .sev-error { border-left:6px solid #f55; }
    .sev-debug { border-left:6px solid #99f; }
    .row { display:flex; gap:8px; flex-wrap:wrap; }
    input { padding:6px 8px; }
    button { padding:6px 10px; cursor:pointer; }
    pre { white-space: pre-wrap; word-break: break-word; margin: 8px 0 0; }
  </style>
</head>
<body>
  <h2>NutryGym Notifications Dashboard</h2>

  <div class="top">
    <span class="pill" id="status">WS: disconnected</span>
    <span class="pill" id="count">Events: 0</span>
    <div class="row">
      <input id="filter" placeholder="filter (text)"/>
      <button onclick="clearEvents()">Clear</button>
    </div>
  </div>

  <div class="cards" id="cards"></div>

<script>
  let ws;
  let events = [];
  let connected = false;

  function sevClass(sev){
    sev = (sev || "").toLowerCase();
    if(sev === "error") return "sev-error";
    if(sev === "warning") return "sev-warning";
    if(sev === "info") return "sev-info";
    return "sev-debug";
  }

  function render(){
    const filter = (document.getElementById("filter").value || "").toLowerCase();
    const cards = document.getElementById("cards");
    cards.innerHTML = "";

    const filtered = events.filter(e => {
      const s = JSON.stringify(e).toLowerCase();
      return !filter || s.includes(filter);
    });

    filtered.slice().reverse().forEach(e => {
      const div = document.createElement("div");
      div.className = "card " + sevClass(e.severity);

      const title = document.createElement("div");
      title.className = "title";
      title.textContent = `${e.title || "Notification"} (${e.severity || "n/a"})`;
      div.appendChild(title);

      const msg = document.createElement("div");
      msg.textContent = e.message || "";
      div.appendChild(msg);

      const meta = document.createElement("div");
      meta.className = "meta";
      meta.textContent = `source=${e.source_service || "unknown"} | type=${e.type || "n/a"}`;
      div.appendChild(meta);

      const pre = document.createElement("pre");
      pre.textContent = JSON.stringify(e, null, 2);
      div.appendChild(pre);

      cards.appendChild(div);
    });

    document.getElementById("count").textContent = `Events: ${events.length}`;
  }

  function clearEvents(){
    events = [];
    render();
  }

  function connect(){
    const proto = location.protocol === "https:" ? "wss" : "ws";
    ws = new WebSocket(`${proto}://${location.host}/ws`);

    ws.onopen = () => {
      connected = true;
      document.getElementById("status").textContent = "WS: connected";
    };

    ws.onclose = () => {
      connected = false;
      document.getElementById("status").textContent = "WS: disconnected (retrying...)";
      setTimeout(connect, 1500);
    };

    ws.onmessage = (ev) => {
      try {
        const obj = JSON.parse(ev.data);
        events.push(obj);
      } catch (e) {
        events.push({ title: "raw", message: ev.data, severity: "debug" });
      }
      render();
    };
  }

  document.getElementById("filter").addEventListener("input", render);
  connect();
</script>

</body>
</html>
"""

@router.get("/", response_class=HTMLResponse, tags=["Web"])
def index():
    return HTMLResponse(_HTML)

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    WS_CLIENTS.add(ws)
    try:
        while True:
            # mantener viva la conexión
            await ws.receive_text()
    except WebSocketDisconnect:
        WS_CLIENTS.discard(ws)
    except Exception:
        WS_CLIENTS.discard(ws)
