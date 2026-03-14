import random

def execute(args):
    lines = []
    
    lines.append({"text": "🪙 מטיל מטבע...", "type": "sys-out"})

    result = random.choice(["עץ", "פלי"])
    
    lines.append({"text": f"✅ התוצאה: {result}", "type": "success"})
    
    return {"lines": lines}
