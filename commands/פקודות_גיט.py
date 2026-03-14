import subprocess
import os

def execute(args):
    lines = []
    
    # Prepend 'git' to the arguments
    git_command = ["git"] + args

    try:
        if not os.path.isdir(".git"):
            lines.append({"text": "❌ שגיאה: זוהי אינה ספריית Git.", "type": "error"})
            return {"lines": lines}

        # Run the git command
        process = subprocess.run(git_command, capture_output=True, text=True, check=False, encoding='utf-8')

        output = process.stdout.strip()
        error_output = process.stderr.strip()

        if process.returncode != 0:
            lines.append({"text": f"❌ שגיאת Git (קוד יציאה {process.returncode}):", "type": "error"})
            if error_output:
                lines.append({"text": error_output, "type": "error"})
            return {"lines": lines}
        
        # Basic parsing for 'git status'
        if args and args[0] == "status":
            lines.append({"text": "📊 סטטוס Git:", "type": "success"})
            if "nothing to commit, working tree clean" in output:
                lines.append({"text": "✅ העץ נקי, אין שינויים לבצע.", "type": ""})
            else:
                for line in output.splitlines():
                    # Translate common status lines
                    if "On branch" in line:
                        lines.append({"text": f" branch: {line.replace('On branch', 'בענף')}", "type": "sys-out"})
                    elif "Your branch is up to date with" in line:
                        lines.append({"text": "⬆️ הענף שלך מעודכן.", "type": "sys-out"})
                    elif "Changes not staged for commit:" in line:
                        lines.append({"text": "⚠️ שינויים שלא נשלחו ל-commit:", "type": ""})
                    elif "Untracked files:" in line:
                        lines.append({"text": "❓ קבצים לא במעקב:", "type": ""})
                    elif "Changes to be committed:" in line:
                        lines.append({"text": "✅ שינויים שיישלחו ל-commit:", "type": ""})
                    elif "no changes added to commit" in line:
                        lines.append({"text": "ℹ️ לא נוספו שינויים ל-commit.", "type": "sys-out"})
                    else:
                        lines.append({"text": line, "type": ""}) # Default to standard output
        elif output:
            for line in output.splitlines():
                lines.append({"text": line, "type": ""})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'git' לא נמצאה. ודא ש-Git מותקן ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
