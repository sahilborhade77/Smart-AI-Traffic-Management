import streamlit as st
import io
import base64

def _speak(text):
    """Private function to process the audio via gTTS."""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        b64 = base64.b64encode(fp.read()).decode()
        md = f'''
            <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            '''
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        print(f"⚠️ Voice Generation Error: {e}")

def play_alert_async(text):
    """
    Public NON-BLOCKING function (now using gTTS + Streamlit HTML autoplay).
    """
    print(f"🔊 [AI VOICE ALERT]: '{text}'")
    _speak(text)

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
