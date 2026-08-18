"""
Jarvis voice: British neural TTS (movie-like), with local SAPI fallback.
"""
from __future__ import annotations

import asyncio
import os
import re
import subprocess
import tempfile
import threading
from typing import Callable, Optional

import config_pi as config

FENCE_RE = re.compile(r"```[\s\S]*?```")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MARKUP_RE = re.compile(r"[*_#>`]+")
SPACE_RE = re.compile(r"\s+")

_play_lock = threading.Lock()
_stop_flag = threading.Event()


def spoken_form(text: str, *, limit: int = 420) -> str:
    """What Jarvis should say: no markdown, no code fences, short enough to speak."""
    raw = (text or "").strip()
    if not raw:
        return ""
    had_code = bool(FENCE_RE.search(raw))
    out = FENCE_RE.sub(" ", raw)
    out = LINK_RE.sub(r"\1", out)
    out = re.sub(r"`([^`]+)`", r"\1", out)
    out = MARKUP_RE.sub(" ", out)
    out = re.sub(r"\s+([,.;:!?])", r"\1", out)
    out = SPACE_RE.sub(" ", out).strip()
    if had_code:
        if out:
            out = out.rstrip(".") + ". The code is on screen, sir."
        else:
            out = "The code is on screen, sir."
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "."
    return out


def _play_mp3(path: str) -> None:
    """Play an mp3 on Windows without extra audio libraries."""
    path = os.path.abspath(path)
    try:
        import pygame

        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if _stop_flag.is_set():
                pygame.mixer.music.stop()
                break
            pygame.time.wait(40)
        return
    except Exception:
        pass

    if os.name != "nt":
        subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path], check=False)
        return

    import ctypes

    alias = "jarvistts"
    winmm = ctypes.windll.winmm

    def send(cmd: str) -> int:
        return int(winmm.mciSendStringW(cmd, None, 0, None))

    send(f"close {alias}")
    err = send(f'open "{path}" type mpegvideo alias {alias}')
    if err:
        err = send(f'open "{path}" alias {alias}')
    if err:
        raise RuntimeError(f"Windows could not play speech audio ({err})")
    send(f"play {alias} wait")
    send(f"close {alias}")


async def _edge_save(text: str, path: str, voice: str, rate: str, pitch: str) -> None:
    import ssl

    import edge_tts
    import edge_tts.communicate as edge_comm

    async def _save() -> None:
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(path)

    try:
        await _save()
        return
    except Exception as exc:
        if "CERTIFICATE" not in str(exc).upper() and "SSL" not in str(exc).upper():
            raise
    # Some Windows setups (corporate TLS inspection) fail Edge's cert check.
    edge_comm._SSL_CTX = ssl._create_unverified_context()
    await _save()


class PiTTS:
    """Speak Jarvis replies aloud. Default: British neural voice (edge-tts)."""

    def __init__(self, engine: Optional[str] = None):
        self.engine = (engine or config.PiConfig.TTS_ENGINE or "edge").lower()
        self.rate = config.PiConfig.TTS_RATE
        self._sapi = None

    def speak(self, text: str, interrupt: bool = False) -> bytes:
        if interrupt:
            self.stop()
        spoken = spoken_form(text)
        if self.engine in {"edge", "neural", "jarvis"}:
            return self._pyttsx3_tts(spoken)
        if self.engine == "piper":
            return self._piper_tts(spoken)
        if self.engine == "pyttsx3":
            return self._pyttsx3_tts(spoken)
        return self._espeak_tts(spoken)

    def speak_aloud(self, text: str) -> None:
        """Speak on the default output device."""
        if not getattr(config.PiConfig, "SPEAK_REPLIES", True):
            return
        spoken = spoken_form(text)
        if not spoken:
            return
        _stop_flag.clear()
        with _play_lock:
            if _stop_flag.is_set():
                return
            try:
                if self.engine in {"edge", "neural", "jarvis", "auto"}:
                    self._edge_speak(spoken)
                    return
            except Exception as exc:
                print(f"Neural TTS failed ({exc}); falling back to Windows voice.")
            try:
                self._sapi_speak(spoken)
            except Exception as e:
                print(f"TTS failed: {e}")

    def _edge_speak(self, text: str) -> None:
        voice = getattr(config.PiConfig, "TTS_VOICE", None) or "en-GB-RyanNeural"
        rate = getattr(config.PiConfig, "TTS_EDGE_RATE", "-12%")
        pitch = getattr(config.PiConfig, "TTS_EDGE_PITCH", "-6Hz")
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        try:
            asyncio.run(_edge_save(text, path, voice, rate, pitch))
            if not _stop_flag.is_set():
                _play_mp3(path)
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _sapi_speak(self, text: str) -> None:
        import pyttsx3

        if self._sapi is None:
            engine = pyttsx3.init()
            engine.setProperty("rate", self.rate)
            self._pick_sapi_voice(engine)
            self._sapi = engine
        self._sapi.say(text)
        self._sapi.runAndWait()

    def _pick_sapi_voice(self, engine) -> None:
        voices = engine.getProperty("voices") or []
        ranked = []
        for voice in voices:
            blob = f"{getattr(voice, 'id', '')} {getattr(voice, 'name', '')}".lower()
            score = 0
            if any(k in blob for k in ("gb", "uk", "british", "george", "hazel", "ryan")):
                score += 3
            if "david" in blob or "mark" in blob or "male" in blob:
                score += 1
            if "zira" in blob or "female" in blob:
                score -= 2
            ranked.append((score, voice))
        ranked.sort(key=lambda item: item[0], reverse=True)
        if ranked and ranked[0][0] > 0:
            engine.setProperty("voice", ranked[0][1].id)

    def _piper_tts(self, text: str) -> bytes:
        try:
            from piper import PiperVoice

            model_path = config.PiConfig.PIPER_MODEL_PATH
            voice = PiperVoice.load(model_path)
            audio_stream = voice.synthesize_stream(text)
            return b"".join(audio_stream)
        except ImportError:
            print("Piper not available, falling back to espeak")
            return self._espeak_tts(text)
        except Exception as e:
            print(f"Piper TTS error: {e}")
            return self._espeak_tts(text)

    def _pyttsx3_tts(self, text: str) -> bytes:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.setProperty("rate", self.rate)
            self._pick_sapi_voice(engine)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
                temp_path = handle.name
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            with open(temp_path, "rb") as handle:
                audio_data = handle.read()
            os.unlink(temp_path)
            return audio_data
        except Exception as e:
            print(f"pyttsx3 error: {e}")
            return self._espeak_tts(text)

    def _espeak_tts(self, text: str) -> bytes:
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
                temp_path = handle.name
            cmd = ["espeak", "-s", str(self.rate), "-w", temp_path, text]
            subprocess.run(cmd, check=True, capture_output=True)
            with open(temp_path, "rb") as handle:
                audio_data = handle.read()
            os.unlink(temp_path)
            return audio_data
        except Exception as e:
            print(f"espeak error: {e}")
            return b""

    def stop(self) -> None:
        _stop_flag.set()
        try:
            import pygame

            pygame.mixer.music.stop()
        except Exception:
            pass
        if os.name == "nt":
            try:
                import ctypes

                ctypes.windll.winmm.mciSendStringW("close jarvistts", None, 0, None)
            except Exception:
                pass
        if self._sapi is not None:
            try:
                self._sapi.stop()
            except Exception:
                pass


class StreamingTTS:
    """Streaming TTS for real-time response"""

    def __init__(self, tts_engine: PiTTS):
        self.tts = tts_engine
        self.is_speaking = False

    def speak_streaming(self, text: str, callback: Optional[Callable] = None):
        audio = self.tts.speak(text)
        if callback:
            callback(audio)
        return audio
