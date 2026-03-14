import os

def execute(args):
    lines = []
    
    lines.append({"text": "--- משתני סביבה מלאים ---", "type": "success"})
    lines.append({"text": "{:<30} {:<60}".format("שם משתנה", "ערך"), "type": "sys-out"})
    lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})

    sorted_env = sorted(os.environ.items())
    for key, value in sorted_env:
        # Truncate long values for readability
        display_value = value if len(value) < 60 else value[:57] + "..."
        lines.append({"text": "{:<30} {:<60}".format(key, display_value), "type": ""})
    
    lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
    lines.append({"text": f"✅ הוצגו {len(sorted_env)} משתני סביבה.", "type": "success"})
    
    return {"lines": lines}
