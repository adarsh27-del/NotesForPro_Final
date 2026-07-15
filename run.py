# run.py — Final, clean, modern launcher for NotesForPro (2026 ngrok compatible)

import os
import time
import subprocess
import webbrowser
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ────────────────────────────────────────────────────────────────
PORT = 8000
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")  # Must be set in .env

# ─── LAUNCH ────────────────────────────────────────────────────────────────

def main():
    print("\n" + "═" * 70)
    print("🚀 NotesForPro Backend + ngrok tunnel launcher")
    print("═" * 70)

    # 1. Set authtoken (required in 2026 free tier)
    if NGROK_AUTH_TOKEN:
        try:
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
            print("✓ ngrok authtoken applied successfully")
        except Exception as e:
            print(f"⚠ ngrok authtoken failed: {e}")
            print("   → Get/fix token at: https://dashboard.ngrok.com/get-started/your-authtoken")
            return
    else:
        print("⚠ No NGROK_AUTH_TOKEN found in .env")
        print("   → App will likely fail. Add it now.")
        return

    # 2. Clean up old tunnels
    ngrok.kill()

    # 3. Start Django server (bind to all interfaces for ngrok)
    print(f"Starting Django on port {PORT}...")
    server = subprocess.Popen(
        ["python", "manage.py", "runserver", f"0.0.0.0:{PORT}"],
        stdout=subprocess.DEVNULL,  # hide spam
        stderr=subprocess.DEVNULL
    )

    # Give Django time to start (adjust if needed)
    time.sleep(5)

    # 4. Create tunnel (NO region parameter anymore!)
    try:
        tunnel = ngrok.connect(PORT, "http")  # ← correct 2026 syntax
        public_url = tunnel.public_url
        os.environ["API_BASE_URL"] = public_url.rstrip('/')
        print("\n" + "═" * 80)
        print("🎉 NOTESFORPRO IS LIVE!")
        print(f"   🌐 Web / Mobile / PWA → {public_url}")
        print(f"   📱 API base             → {public_url}/api/")
        print(f"   🖥️  Desktop connects to   → {public_url}")
        print("═" * 80)
        print("Press Ctrl+C to stop\n")

        # Auto-open in default browser (optional but nice)
        webbrowser.open(public_url)

    except Exception as e:
        print("\nngrok tunnel failed:")
        print(str(e))
        print("\nCommon fixes:")
        print("1. Check NGROK_AUTH_TOKEN is correct (copy from dashboard)")
        print("2. Run 'python manage.py runserver 0.0.0.0:8000' alone first to see Django errors")
        print("3. Firewall/antivirus blocking port 8000? Temporarily disable")
        print("4. Try different port: change PORT=8001 in this file")

    # Keep alive until Ctrl+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.terminate()
        ngrok.kill()
        print("Done. Have a great day!")

if __name__ == "__main__":
    main()