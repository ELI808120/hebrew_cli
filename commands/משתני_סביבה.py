import os

def execute(args):
    lines = []
    
    if args:
        var_name = args[0].upper() # Environment variable names are typically uppercase
        lines.append({"text": f"🔍 מחפש את משתנה הסביבה '{var_name}'...", "type": "sys-out"})
        var_value = os.environ.get(var_name)
        if var_value is not None:
            lines.append({"text": f"✅ {var_name}: {var_value}", "type": "success"})
        else:
            lines.append({"text": f"⚠️ משתנה הסביבה '{var_name}' לא נמצא.", "type": "sys-out"})
    else:
        lines.append({"text": "--- משתני סביבה ---", "type": "success"})
        sorted_env = sorted(os.environ.items())
        for key, value in sorted_env:
            lines.append({"text": f"  {key}: {value}", "type": ""})
        lines.append({"text": "✅ הצגת משתני סביבה הושלמה.", "type": "success"})
    
    return {"lines": lines}
