"""
Allowlisted PC skills — the closest we get to movie JARVIS on a Windows box.

No arbitrary shell. No surveillance. No attack tools.
"""
from __future__ import annotations

import re
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

try:
    import psutil
except ImportError:
    psutil = None  # type: ignore

try:
    import requests
except ImportError:
    requests = None  # type: ignore

NOTES_DIR = Path.home() / "Documents" / "Jarvis"
SHOTS_DIR = Path.home() / "Pictures" / "Jarvis"

APPS: dict[str, list[str]] = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "explorer": ["explorer.exe"],
    "files": ["explorer.exe"],
    "chrome": ["chrome.exe"],
    "edge": ["msedge.exe"],
    "spotify": ["spotify.exe"],
    "discord": ["discord.exe"],
    "vscode": ["code"],
    "code": ["code"],
    "cursor": ["cursor"],
}

STAND_DOWN = (
    "stand down",
    "stand by",
    "that's all",
    "thats all",
    "go to sleep",
    "never mind",
    "nevermind",
    "dismissed",
)


def try_skill(text: str) -> Optional[str]:
    """Run a real action if the line matches. Otherwise None (LLM handles it)."""
    raw = (text or "").strip()
    if not raw:
        return None
    lowered = raw.lower()

    if any(p in lowered for p in STAND_DOWN):
        return "Standing by, sir."

    if lowered in {"help", "help me", "what can you do", "what do you do", "your capabilities"}:
        return (
            "I can talk, write and edit code in this project, check system status, "
            "tell the time, check the weather, search the web, open apps, take a screenshot, "
            "and jot a note. Say Jarvis, then the command."
        )

    if lowered in {"who are you", "what are you"}:
        return (
            "J.A.R.V.I.S. — Just A Rather Very Intelligent System. "
            "Online, local, and at your service."
        )

    if _looks_like(lowered, ("what time", "current time", "what's the time", "whats the time")):
        return _time()
    if re.fullmatch(r"(the )?date( today)?", lowered):
        return _time()

    if _looks_like(lowered, ("system status", "status report", "how are we looking", "diagnostics")):
        return _status()

    if _looks_like(lowered, ("screenshot", "take a screenshot", "capture the screen")):
        return _screenshot()

    if _looks_like(lowered, ("weather", "what's the weather", "whats the weather", "temperature outside")):
        return _weather()

    note = _extract_after(lowered, raw, ("note that", "take a note", "remember this", "jot down"))
    if note:
        return _note(note)

    if lowered.startswith("search ") or lowered.startswith("google ") or lowered.startswith("look up "):
        query = re.sub(r"^(search|google|look up)\s+", "", raw, flags=re.I).strip()
        return _web_search(query)

    if lowered.startswith("open "):
        target = raw[5:].strip()
        return _open(target)

    return None


def _looks_like(lowered: str, phrases: tuple[str, ...]) -> bool:
    return any(p in lowered for p in phrases)


def _extract_after(lowered: str, raw: str, prefixes: tuple[str, ...]) -> str:
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return raw[len(prefix) :].strip(" :,-")
    return ""


def _time() -> str:
    now = datetime.now()
    return f"It's {now.strftime('%I:%M %p').lstrip('0')} on {now.strftime('%A, %B %d')}."


def _status() -> str:
    bits = [f"All systems operational. {platform_name()}."]
    if psutil:
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory()
        bits.append(f"CPU {cpu:.0f} percent. Memory {ram.percent:.0f} percent used.")
        battery = getattr(psutil, "sensors_battery", lambda: None)()
        if battery:
            plug = "on power" if battery.power_plugged else "on battery"
            bits.append(f"Battery {battery.percent:.0f} percent, {plug}.")
    return " ".join(bits)


def platform_name() -> str:
    import platform

    return f"{platform.system()} {platform.release()}"


def _weather() -> str:
    if not requests:
        return "Weather client isn't installed."
    try:
        resp = requests.get("https://wttr.in/?format=3", timeout=6)
        resp.raise_for_status()
        line = resp.text.strip()
        return line or "Weather service returned nothing."
    except Exception:
        return "I couldn't reach the weather service."


def _web_search(query: str) -> str:
    if not query:
        return "What should I search for?"
    webbrowser.open(f"https://duckduckgo.com/?q={quote_plus(query)}")
    return f"Searching the web for {query}."


def _open(target: str) -> str:
    lowered = target.lower().strip()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        webbrowser.open(target)
        return "Opening that in your browser."
    if "youtube" in lowered:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    for name, cmd in APPS.items():
        if name in lowered:
            try:
                subprocess.Popen(cmd, shell=False)
                return f"Opening {name}."
            except Exception as exc:
                return f"I couldn't launch {name}: {exc}"
    if lowered in {"browser", "the browser", "web"}:
        webbrowser.open("https://duckduckgo.com")
        return "Browser up."
    return f"I don't have {target} on the allow-list. I can open notepad, calculator, explorer, chrome, edge, spotify, vscode, or cursor."


def _screenshot() -> str:
    SHOTS_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOTS_DIR / f"shot-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
    script = f"""
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bmp.Save('{str(path).replace("'", "''")}')
"""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=True,
            capture_output=True,
            timeout=20,
        )
        if path.exists():
            return f"Screenshot saved to {path}."
        return "Screenshot command ran, but I don't see the file yet."
    except Exception as exc:
        return f"Screenshot failed: {exc}"


def _note(text: str) -> str:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    note_path = NOTES_DIR / "notes.txt"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with note_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{stamp}] {text}\n")
    return "Noted, sir."
