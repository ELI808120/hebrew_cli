import os
import sys
import subprocess
import importlib.util
import webview

# --- פונקציה לטעינת הגדרות חיצוניות (פותרת את בעיית ה-AttributeError) ---
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def load_settings():
    base_path = get_base_path()
    settings_path = os.path.join(base_path, "settings.py")
    
    # ערכי ברירת מחדל למקרה שהקובץ חסר או פגום
    class DefaultConfig:
        LOGO = "=== המעטפת העברית ===\nנתיב: {path}\nפקודות: {cmd_count}"
        APP_TITLE = "מעטפת עברית - גרסה חסינה"
        PROMPT_SYMBOL = "פקודה < "

    if os.path.exists(settings_path):
        try:
            spec = importlib.util.spec_from_file_location("settings", settings_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        except Exception as e:
            print(f"שגיאה בטעינת settings.py: {e}")
            return DefaultConfig
    return DefaultConfig

# טעינת הקונפיגורציה
ext_config = load_settings()

# --- הממשק הגרפי (HTML) ---
HTML_CONTENT = f"""
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            background-color: #121212;
            color: #00ff00;
            font-family: 'Consolas', 'Courier New', monospace;
            margin: 0; padding: 20px; font-size: 16px; overflow-y: auto;
        }}
        #history {{ margin-bottom: 10px; }}
        .line {{ margin: 5px 0; line-height: 1.5; white-space: pre-wrap; word-break: break-all; }}
        .cmd-echo {{ color: #ffffff; font-weight: bold; margin-top: 15px; }}
        .error {{ color: #ff5555; }}
        .success {{ color: #5ce1e6; }}
        .sys-out {{ color: #aaaaaa; }}
        #input-container {{ display: flex; align-items: center; margin-top: 10px; }}
        #prompt {{ margin-left: 10px; font-weight: bold; white-space: nowrap; color: #5ce1e6; }}
        #cmd-input {{
            background: transparent; border: none; color: #00ff00;
            font-family: inherit; font-size: inherit; flex-grow: 1;
            outline: none; direction: rtl;
        }
        pre {{ font-family: inherit; margin: 0; white-space: pre; }}
    </style>
</head>
<body>
    <div id="history"></div>
    <div id="input-container">
        <span id="prompt">{ext_config.PROMPT_SYMBOL}</span>
        <input type="text" id="cmd-input" autocomplete="off" autofocus>
    </div>

    <script>
        const input = document.getElementById('cmd-input');
        const history = document.getElementById('history');

        function appendLine(text, className="line") {{
            const div = document.createElement('div');
            div.className = className;
            div.textContent = text;
            history.appendChild(div);
            window.scrollTo(0, document.body.scrollHeight);
        }}

        input.addEventListener('keypress', function (e) {{
            if (e.key === 'Enter') {{
                const cmd = input.value.trim();
                if (!cmd) return;
                appendLine("פקודה <  " + cmd, "line cmd-echo");
                input.value = '';
                pywebview.api.execute(cmd).then(function(response) {{
                    if (response.clear) {{ history.innerHTML = ''; }}
                    else if (response.lines) {{
                        response.lines.forEach(item => {{ appendLine(item.text, "line " + item.type); }});
                    }}
                }});
            }}
        }});

        window.addEventListener('pywebviewready', function() {{
            pywebview.api.get_startup_info().then(function(logo) {{
                const pre = document.createElement('pre');
                pre.className = "line success";
                pre.style.fontSize = "12px";
                pre.textContent = logo;
                history.appendChild(pre);
                appendLine("המערכת מוכנה. הקלד פקודה.", "line sys-out");
            }});
        }});
        document.addEventListener('click', () => input.focus());
    </script>
</body>
</html>
"""

class Api:
    def __init__(self):
        base_path = get_base_path()
        self.commands_dir = os.path.join(base_path, "commands")
        self.modules = {}
        self.setup_modular_commands()

    def setup_modular_commands(self):
        if not os.path.exists(self.commands_dir):
            os.makedirs(self.commands_dir)
        for filename in os.listdir(self.commands_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                cmd_name = filename[:-3]
                filepath = os.path.join(self.commands_dir, filename)
                try:
                    spec = importlib.util.spec_from_file_location(cmd_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.modules[cmd_name] = module.execute
                except Exception as e:
                    print(f"Error loading {cmd_name}: {e}")

    def get_startup_info(self):
        cmd_count = len(self.modules)
        # טעינה מחדש של הקונפיגורציה כדי לאפשר שינוי לוגו "חם"
        current_config = load_settings()
        return current_config.LOGO.format(path=os.getcwd(), cmd_count=cmd_count)

    def execute(self, full_cmd):
        parts = full_cmd.split()
        if not parts: return {"lines": []}
        cmd = parts[0]
        args = parts[1:]

        if cmd == "נקה": return {"clear": True}
        if cmd == "צא": os._exit(0)

        if cmd in self.modules:
            try:
                return self.modules[cmd](args)
            except Exception as e:
                return {"lines": [{"text": f"שגיאה בפקודה: {e}", "type": "error"}]}

        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.run(full_cmd, shell=True, capture_output=True, startupinfo=startupinfo)
            output = (result.stdout + result.stderr).decode('cp862', errors='replace')
            lines = [{"text": line, "type": "sys-out"} for line in output.splitlines() if line.strip()]
            return {"lines": lines or [{"text": "הפקודה בוצעה.", "type": "sys-out"}]}
        except Exception as e:
            return {"lines": [{"text": f"שגיאת מערכת: {e}", "type": "error"}]}

if __name__ == '__main__':
    api = Api()
    webview.create_window(ext_config.APP_TITLE, html=HTML_CONTENT, js_api=api, width=950, height=650)
    webview.start()