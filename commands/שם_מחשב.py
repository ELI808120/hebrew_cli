import socket

def execute(args):
    lines = []
    
    lines.append({"text": "💻 מאחזר את שם המחשב הנוכחי...", "type": "sys-out"})

    try:
        hostname = socket.gethostname()
        lines.append({"text": f"✅ שם המחשב: {hostname}", "type": "success"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאה באחזור שם המחשב: {e}", "type": "error"})
    
    return {"lines": lines}
