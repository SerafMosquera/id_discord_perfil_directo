import os
import qrcode
from flask import Flask, redirect, render_template_string

app = Flask(__name__)

# ✅ Tu ID numérica de Discord
ID_DISCORD = "1529305639329726654"

PERFIL_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mi Perfil de Discord</title>
<style>
  body {
    margin: 0;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1e1f22, #2b2d31);
    font-family: 'Segoe UI', sans-serif;
  }
  .card {
    background: #2b2d31;
    border-radius: 16px;
    padding: 30px;
    width: 320px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    color: #fff;
  }
  .avatar-wrap {
    position: relative;
    width: 110px;
    height: 110px;
    margin: 0 auto 15px;
  }
  .avatar {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 4px solid #5865F2;
    object-fit: cover;
  }
  .status {
    position: absolute;
    bottom: 4px;
    right: 4px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 4px solid #2b2d31;
  }
  .online { background: #23a55a; }
  .idle { background: #f0b232; }
  .dnd { background: #f23f43; }
  .offline { background: #80848e; }
  h1 { margin: 5px 0; font-size: 22px; }
  .tag { color: #949ba4; font-size: 14px; margin-bottom: 15px; }
  .activity {
    background: #1e1f22;
    border-radius: 10px;
    padding: 10px;
    font-size: 13px;
    color: #dbdee1;
    min-height: 18px;
  }
</style>
</head>
<body>
  <div class="card">
    <div class="avatar-wrap">
      <img id="avatar" class="avatar" src="" alt="avatar">
      <div id="status" class="status offline"></div>
    </div>
    <h1 id="username">Cargando...</h1>
    <div class="tag" id="tag"></div>
    <div class="activity" id="activity">Sin actividad</div>
  </div>

<script>
const ID = "{{ id_discord }}";

async function actualizarPerfil() {
  try {
    const res = await fetch(`https://api.lanyard.rest/v1/users/${ID}`);
    const json = await res.json();
    if (!json.success) return;
    const d = json.data;

    const avatarHash = d.discord_user.avatar;
    const avatarUrl = avatarHash
      ? `https://cdn.discordapp.com/avatars/${ID}/${avatarHash}.png?size=256`
      : `https://cdn.discordapp.com/embed/avatars/0.png`;

    document.getElementById("avatar").src = avatarUrl;
    document.getElementById("username").innerText = d.discord_user.global_name || d.discord_user.username;
    document.getElementById("tag").innerText = "@" + d.discord_user.username;

    const statusEl = document.getElementById("status");
    statusEl.className = "status " + d.discord_status;

    const act = d.activities && d.activities.length > 0 ? d.activities[0] : null;
    document.getElementById("activity").innerText = act
      ? (act.name + (act.details ? " — " + act.details : ""))
      : "Sin actividad";
  } catch (e) {
    console.error("Error actualizando perfil:", e);
  }
}

actualizarPerfil();
setInterval(actualizarPerfil, 5000);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    # Redirige directo a tu perfil real de Discord
    return redirect(f"https://discord.com/users/{ID_DISCORD}")


@app.route("/perfil")
def perfil():
    return render_template_string(PERFIL_HTML, id_discord=ID_DISCORD)


def generar_qr():
    # El QR apunta a la página de perfil en vivo, no a la redirección directa
    base_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")
    url_destino = f"{base_url}/perfil"

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url_destino)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("codigo_qr.png")
    print("✨ ¡Código QR permanente generado exitosamente como 'codigo_qr.png'!")


if __name__ == "__main__":
    generar_qr()
    app.run(host="0.0.0.0", port=5000)