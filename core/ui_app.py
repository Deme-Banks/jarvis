"""Simple local JARVIS window: transcript, type, mic, model name."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import scrolledtext

from core.boot import boot_orchestrator
from core.session import JarvisSession
from voice.audio_pi import PiAudioCapture
from voice.stt_pi import PiSTT
from voice.tts_pi import PiTTS

from core.voice_cli import (
    MIN_UTTERANCE_BYTES,
    SILENCE_FRAMES_END,
    _is_loud,
)


class JarvisUI:
    def __init__(self) -> None:
        self.session = JarvisSession(boot_orchestrator(announce=False))
        self.tts = PiTTS()
        self.busy = False
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.configure(bg="#0b0b0d")
        self.root.geometry("720x540")

        model = self.session.current_model()
        self.status = tk.Label(
            self.root,
            text=f"Model: {model}   |   local, personal",
            fg="#d4af37",
            bg="#0b0b0d",
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.status.pack(fill="x", padx=12, pady=(10, 4))

        self.log = scrolledtext.ScrolledText(
            self.root,
            wrap="word",
            bg="#141418",
            fg="#f2f2f2",
            insertbackground="#f2f2f2",
            font=("Consolas", 11),
            height=22,
        )
        self.log.pack(fill="both", expand=True, padx=12, pady=6)
        self.log.configure(state="disabled")

        row = tk.Frame(self.root, bg="#0b0b0d")
        row.pack(fill="x", padx=12, pady=(0, 12))

        self.entry = tk.Entry(
            row,
            bg="#1c1c22",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Segoe UI", 11),
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<Return>", lambda _e: self._send())

        tk.Button(row, text="Send", command=self._send, bg="#d4af37", fg="#111").pack(
            side="left", padx=(8, 0)
        )
        tk.Button(row, text="Mic", command=self._mic, bg="#2a2a33", fg="#d4af37").pack(
            side="left", padx=(8, 0)
        )
        self.apply_btn = tk.Button(
            row, text="Apply edit", command=self._apply, bg="#2a2a33", fg="#9fef9f"
        )
        self.apply_btn.pack(side="left", padx=(8, 0))

        self._append("JARVIS", "Online. Type a command, or Mic to speak. Edits wait for Apply.")
        self.entry.focus_set()

    def _append(self, who: str, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"{who}: {text}\n\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_busy(self, busy: bool, label: str = "") -> None:
        self.busy = busy
        if label:
            self.status.configure(text=label)

    def _send(self, spoken: str | None = None) -> None:
        if self.busy:
            return
        text = (spoken if spoken is not None else self.entry.get()).strip()
        if not text:
            return
        if spoken is None:
            self.entry.delete(0, "end")
        self._append("You", text)
        self._set_busy(True, "Working…")

        def work() -> None:
            reply = self.session.ask(text)
            self.root.after(0, lambda: self._on_reply(reply))

        threading.Thread(target=work, daemon=True).start()

    def _on_reply(self, reply: str) -> None:
        self._append("JARVIS", reply)
        model = self.session.current_model()
        pending = "   |   edit waiting" if self.session.pending_edit else ""
        self._set_busy(False, f"Model: {model}   |   local, personal{pending}")
        try:
            self.tts.speak_aloud(reply[:400])
        except Exception:
            pass

    def _apply(self) -> None:
        if not self.session.pending_edit:
            self._append("JARVIS", "No pending edit.")
            return
        self._send("apply")

    def _mic(self) -> None:
        if self.busy:
            return
        self._set_busy(True, "Listening…")

        def work() -> None:
            try:
                heard = _capture_utterance()
            except Exception as exc:
                heard = ""
                err = str(exc)
                self.root.after(0, lambda: self._append("JARVIS", f"Mic failed: {err}"))
            self.root.after(0, lambda: self._after_mic(heard))

        threading.Thread(target=work, daemon=True).start()

    def _after_mic(self, heard: str) -> None:
        self._set_busy(False, f"Model: {self.session.current_model()}   |   local, personal")
        if heard:
            self._send(heard)
        else:
            self._append("JARVIS", "I didn't catch that.")

    def run(self) -> None:
        self.root.mainloop()


def _capture_utterance() -> str:
    capture = PiAudioCapture()
    stt = PiSTT()
    capture.start_stream()
    try:
        buf = b""
        silence = 0
        heard_speech = False
        # ~12 s cap
        frames = 0
        max_frames = int((12.0 / (320 / 16000)))
        while frames < max_frames:
            chunk = capture.read_chunk()
            frames += 1
            speech = capture.is_speech(chunk) or _is_loud(chunk)
            if speech:
                heard_speech = True
                buf += chunk
                silence = 0
                continue
            if not heard_speech:
                continue
            silence += 1
            if silence >= SILENCE_FRAMES_END and len(buf) >= MIN_UTTERANCE_BYTES:
                break
        return (stt.transcribe(buf) or "").strip()
    finally:
        capture.cleanup()


def run_ui() -> None:
    JarvisUI().run()
