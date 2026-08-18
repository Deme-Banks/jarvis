"""Mic loop: wake word, Vosk, Ollama, Windows TTS."""
from __future__ import annotations

import numpy as np

import config_pi as config
from core.boot import boot_orchestrator
from core.session import JarvisSession
from voice.audio_pi import PiAudioCapture, PiAudioOutput
from voice.stt_pi import PiSTT
from voice.tts_pi import PiTTS

WAKE = config.PiConfig.WAKE_WORD.lower()
MIN_UTTERANCE_BYTES = int(config.PiConfig.SAMPLE_RATE * 2 * 0.4)
SILENCE_FRAMES_END = 25
ENERGY_SPEECH = 400.0


def _is_loud(chunk: bytes) -> bool:
    if len(chunk) < 2:
        return False
    samples = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)
    rms = float(np.sqrt(np.mean(np.square(samples))))
    return rms >= ENERGY_SPEECH


class VoiceJarvis:
    def __init__(self):
        self.audio_capture = PiAudioCapture()
        self.audio_output = PiAudioOutput()
        self.stt = PiSTT()
        self.tts = PiTTS()
        self.session: JarvisSession | None = None
        self.awake = False
        self.is_speaking = False

    def start(self) -> None:
        print("JARVIS starting (voice, Ollama)...")
        if not self.stt.recognizer:
            print("Vosk did not load. Check models/vosk-model-small-en-us-0.15")
            return
        self.session = JarvisSession(boot_orchestrator())
        self.audio_capture.start_stream()
        print(f"Ready. Say '{config.PiConfig.WAKE_WORD}' then your command.")
        print("Press Ctrl+C to exit")
        try:
            self._listen_loop()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()

    def _listen_loop(self) -> None:
        audio_buffer = b""
        silence_frames = 0
        while True:
            try:
                chunk = self.audio_capture.read_chunk()
            except Exception as exc:
                print(f"Mic read failed: {exc}")
                continue
            speech = self.audio_capture.is_speech(chunk) or _is_loud(chunk)
            if speech:
                audio_buffer += chunk
                silence_frames = 0
                continue
            silence_frames += 1
            if audio_buffer and silence_frames >= SILENCE_FRAMES_END:
                if len(audio_buffer) >= MIN_UTTERANCE_BYTES:
                    try:
                        self._handle_utterance(audio_buffer)
                    except Exception as exc:
                        print(f"Utterance error: {exc}")
                audio_buffer = b""
                silence_frames = 0

    def _handle_utterance(self, audio_data: bytes) -> None:
        assert self.session is not None
        text = (self.stt.transcribe(audio_data) or "").strip()
        if len(text) < 2:
            return

        lowered = text.lower()
        print(f"You: {text}")

        if not self.awake:
            if WAKE not in lowered:
                return
            self.awake = True
            after = lowered.split(WAKE, 1)[-1].strip(" ,.-")
            if len(after) < 2:
                self._speak("Yes?")
                return
            text = after

        reply = self.session.ask(text)
        print(f"JARVIS: {reply}")
        self._speak(reply)
        self.awake = False

    def _speak(self, text: str) -> None:
        self.is_speaking = True
        try:
            self.tts.speak_aloud(text)
        except Exception as exc:
            print(f"TTS failed: {exc}")
        finally:
            self.is_speaking = False

    def cleanup(self) -> None:
        try:
            self.audio_capture.cleanup()
        except Exception:
            pass
        try:
            self.audio_output.cleanup()
        except Exception:
            pass


def run_voice() -> None:
    VoiceJarvis().start()
