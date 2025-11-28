"""
AI Video Effect Detector - FastAPI Backend
MVP using Gemini 1.5 Pro for video effect classification
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile
import os
import shutil
from typing import Dict, Any
import logging
import json
import time

from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Video Effect Detector",
    description="MVP backend for classifying video editing effects using SlowFast",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Gemini model instance
gemini_model = None

@app.on_event("startup")
async def startup_event():
    """Initialize Gemini API on startup"""
    global gemini_model
    try:
        # Get API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        logger.info("Initializing Gemini API...")
        genai.configure(api_key=api_key)
        # Use the most advanced Gemini model for video understanding
        # Try the latest experimental model first, fallback to 1.5-pro
        try:
            gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Latest experimental
            logger.info("Using Gemini 2.0 Flash Experimental")
        except Exception:
            gemini_model = genai.GenerativeModel('gemini-1.5-pro')  # Most advanced stable model
            logger.info("Using Gemini 1.5 Pro (fallback)")
        logger.info("Gemini API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini API: {e}")
        raise

@app.post("/classify")
async def classify_video_effect(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Classify the video editing effect in an uploaded video.

    Args:
        file: Video file upload (mp4, mov, avi supported)

    Returns:
        JSON with effect classification results
    """
    # Validate file type
    allowed_extensions = {'.mp4', '.mov', '.avi'}
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Create temporary file for the video
    with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as temp_file:
        try:
            # Save uploaded file
            shutil.copyfileobj(file.file, temp_file)
            temp_file.flush()
            video_path = temp_file.name

            # Upload video to Gemini
            logger.info("Uploading video to Gemini...")
            video_file = genai.upload_file(video_path)

            # Wait for file to be processed and become ACTIVE
            logger.info("Waiting for video to be processed...")
            max_wait_time = 120  # Maximum wait time in seconds
            wait_interval = 2   # Check every 2 seconds
            elapsed_time = 0
            
            while video_file.state.name == "PROCESSING":
                if elapsed_time >= max_wait_time:
                    raise HTTPException(
                        status_code=408,
                        detail="Video processing timed out. Please try a shorter video."
                    )
                time.sleep(wait_interval)
                elapsed_time += wait_interval
                video_file = genai.get_file(video_file.name)
                logger.info(f"File state: {video_file.state.name} (waited {elapsed_time}s)")

            if video_file.state.name == "FAILED":
                raise HTTPException(
                    status_code=400,
                    detail="Video processing failed. Please try a different video format."
                )
            
            logger.info(f"Video ready! State: {video_file.state.name}")

            # Create classification prompt
            prompt = """
            Analyze this video clip and identify:
            1. The primary video editing effect/transition used
            2. Any text/caption effects present in the video

            TRANSITION EFFECT categories (choose the best match):
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

            TEXT/CAPTION EFFECT categories (can select multiple, or "none" if no text):
            - typewriter: Text appears letter by letter
            - pop_up: Text pops/bounces into view
            - fade_in: Text fades in gradually
            - slide_in: Text slides in from a direction
            - kinetic_typography: Animated text with movement/scaling
            - glitch_text: Text with glitch/distortion effects
            - neon_glow: Text with glowing/neon effect
            - 3d_text: Three-dimensional text effect
            - handwritten: Text appears as if being written
            - bounce: Text bounces or has elastic animation
            - shake: Text shakes or vibrates
            - highlight: Text gets highlighted or underlined
            - word_by_word: Words appear one at a time
            - scale_in: Text scales up from small to normal
            - rotate_in: Text rotates into position
            - split_text: Text splits or separates
            - stroke_reveal: Text outline draws itself
            - color_wipe: Color sweeps across text
            - none: No text effects detected

            Return ONLY a JSON object in this exact format:
            {
              "effect": "effect_name",
              "confidence": 0.85,
              "description": "brief explanation of the transition effect",
              "caption_effects": {
                "detected": true,
                "effects": ["effect1", "effect2"],
                "text_content": "the actual text shown if readable",
                "description": "description of how the text is animated/styled"
              }
            }

            If no text/captions are present, set caption_effects.detected to false and effects to ["none"].
            """

            # Run Gemini classification
            logger.info("Running Gemini analysis...")
            response = gemini_model.generate_content([prompt, video_file])

            # Parse JSON response
            try:
                # Extract JSON from response
                response_text = response.text.strip()
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

                result = json.loads(response_text)

                # Validate required fields
                required_fields = ["effect", "confidence", "description"]
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing required field: {field}")

                # Ensure effect is valid
                valid_effects = [
                    "hard_cut", "crossfade", "whip_pan", "zoom_cut", "speed_ramp",
                    "shake_transition", "flash_frame", "reverse_effect", "match_cut", "unknown"
                ]
                if result["effect"] not in valid_effects:
                    result["effect"] = "unknown"

                # Ensure confidence is a number between 0 and 1
                result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))

                # Validate caption_effects if present
                valid_caption_effects = [
                    "typewriter", "pop_up", "fade_in", "slide_in", "kinetic_typography",
                    "glitch_text", "neon_glow", "3d_text", "handwritten", "bounce",
                    "shake", "highlight", "word_by_word", "scale_in", "rotate_in",
                    "split_text", "stroke_reveal", "color_wipe", "none"
                ]
                
                if "caption_effects" not in result:
                    result["caption_effects"] = {
                        "detected": False,
                        "effects": ["none"],
                        "text_content": "",
                        "description": "No text effects analyzed"
                    }
                else:
                    # Validate caption effects
                    caption = result["caption_effects"]
                    if "effects" in caption:
                        caption["effects"] = [
                            e for e in caption["effects"] 
                            if e in valid_caption_effects
                        ] or ["none"]
                    else:
                        caption["effects"] = ["none"]
                    
                    if "detected" not in caption:
                        caption["detected"] = caption["effects"] != ["none"]
                    
                    if "text_content" not in caption:
                        caption["text_content"] = ""
                    
                    if "description" not in caption:
                        caption["description"] = ""

                result["model_used"] = "gemini-latest"  # Could be 2.0-flash-exp or 1.5-pro

                logger.info(f"Gemini classification result: {result}")
                return result

            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse Gemini response: {e}")
                logger.error(f"Raw response: {response.text}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to parse classification result from AI model"
                )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Video processing failed: {str(e)}"
            )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "gemini_initialized": gemini_model is not None}


# Serve frontend
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html"""
    return FileResponse(FRONTEND_DIR / "index.html")


# Mount static files for any additional frontend assets
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
