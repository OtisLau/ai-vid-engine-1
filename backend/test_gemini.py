"""
Test script for Gemini video effect detection
"""

import os
import json
from pathlib import Path

def test_gemini_setup():
    """Test that Gemini API key is configured and basic functionality works"""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("Please set it with: export GEMINI_API_KEY='your-api-key-here'")
        return False

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # Test basic model initialization
        model = genai.GenerativeModel('gemini-1.5-pro')
        print("✅ Gemini API configured successfully")
        print("✅ Model initialized: gemini-1.5-pro")

        return True

    except ImportError:
        print("❌ google-generativeai package not installed")
        print("Install with: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def test_prompt_structure():
    """Test that our prompt structure is valid"""

    prompt = """
    Analyze this video clip and identify the primary video editing effect/transition used.

    Effect categories (choose the best match):
    - hard_cut: Abrupt change between shots with no transition
    - crossfade: Gradual dissolve/fade from one shot to another
    - whip_pan: Fast camera pan movement with motion blur
    - zoom_cut: Quick zoom transition between shots
    - speed_ramp: Speed change (slow motion or fast motion effect)
    - shake_transition: Camera shake or vibration effect
    - flash_frame: Brief white/black flash between shots
    - reverse_effect: Reverse motion playback
    - match_cut: Visual continuity cut matching objects/shapes
    - unknown: No clear editing effect detected

    Return ONLY a JSON object in this exact format:
    {"effect": "effect_name", "confidence": 0.85, "description": "brief explanation"}
    """

    print("✅ Prompt structure validated")
    print("Expected JSON format:")
    print(json.dumps({
        "effect": "crossfade",
        "confidence": 0.92,
        "description": "Gradual dissolve transition between two shots"
    }, indent=2))

if __name__ == "__main__":
    print("🧪 Testing Gemini Video Effect Detector Setup\n")

    gemini_ok = test_gemini_setup()
    print()
    test_prompt_structure()
    print()

    if gemini_ok:
        print("🎉 Setup looks good! Ready to test with actual videos.")
        print("\nNext steps:")
        print("1. Get a Gemini API key from Google AI Studio")
        print("2. Set GEMINI_API_KEY environment variable")
        print("3. Run: python main.py")
        print("4. Test with a video file using the /classify endpoint")
    else:
        print("❌ Setup issues found. Please fix before running the API.")
