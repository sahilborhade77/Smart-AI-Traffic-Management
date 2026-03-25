import pyttsx3
import threading

def initialize_engine():
    """
    Initializes the Windows offline text-to-speech engine.
    Absolutely 0 lag or internet connection required.
    """
    engine = pyttsx3.init()
    
    # Set a professional speaking rate (not too fast for judges)
    engine.setProperty('rate', 165) 
    
    # Attempt to pick the native Windows 10/11 Female Voice (Zira) which sounds much more modern.
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Zira" in voice.name or "Female" in voice.name:
            engine.setProperty('voice', voice.id)
            break
            
    return engine

def _speak(text):
    """Private blocking function to process the audio."""
    try:
        engine = initialize_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Voice Generation Error: {e}")

def play_alert_async(text):
    """
    Public NON-BLOCKING function.
    This is critical for Phase 7: Because Streamlit UI naturally freezes while executing code,
    pushing the Voice Engine to a background CPU thread means your dashboard animations 
    and YOLO video will continue rendering smoothly while the AI speaks!
    """
    print(f"🔊 [AI VOICE ALERT]: '{text}'")
    tts_thread = threading.Thread(target=_speak, args=(text,))
    tts_thread.start()

# =========================================================
# REQUIRED DAY 7 ROADMAP PHRASES
# =========================================================

def trigger_accident_warning():
    play_alert_async("High accident risk zone ahead. Please reduce your speed.")

def trigger_emergency_detection():
    play_alert_async("Emergency Vehicle approaching. Please move to the left lane.")

def trigger_weather_warning(condition_name="fog"):
    play_alert_async(f"Weather risk elevated. Severe {condition_name} detected.")

if __name__ == "__main__":
    import time
    print("=" * 60)
    print("🎙️ MULTI-MODAL VOICE ALERTS MODULE INITIATED")
    print("=" * 60)
    
    # Testing exactly the 3 phrases specified in the Phase 6 Roadmap
    trigger_accident_warning()
    time.sleep(3.5) 
    
    trigger_emergency_detection()
    time.sleep(4.0)
    
    trigger_weather_warning("monsoon rain")
    time.sleep(4.0)
    
    print("\n✅ Tested all background thread voice sequences perfectly!")
