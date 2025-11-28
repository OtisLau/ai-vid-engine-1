# AI Video Effect Detector - Gemini Backend

This is the FastAPI backend for the AI Video Effect Detector MVP, using Google's Gemini AI for video effect classification.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Test Setup
```bash
python test_gemini.py
```

### 4. Run the API
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Classify Video Effect
```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_video.mp4"
```

**Response:**
```json
{
  "effect": "crossfade",
  "confidence": 0.92,
  "description": "Gradual dissolve transition between two shots over 2 seconds",
  "model_used": "gemini-latest"
}
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Supported Effects

The system can detect these video editing effects:
- `hard_cut` - Abrupt change between shots
- `crossfade` - Gradual dissolve/fade transition
- `whip_pan` - Fast camera pan with motion blur
- `zoom_cut` - Quick zoom transition
- `speed_ramp` - Speed change (slow/fast motion)
- `shake_transition` - Camera shake effect
- `flash_frame` - Brief white/black flash
- `reverse_effect` - Reverse motion
- `match_cut` - Visual continuity cut
- `unknown` - No clear effect detected

## Model

Uses the latest Gemini model available:
- Primary: `gemini-2.0-flash-exp` (experimental, most advanced)
- Fallback: `gemini-1.5-pro` (stable, very capable)

Both models excel at video understanding and can analyze temporal patterns, motion, and editing techniques.

## Cost

- ~$0.002-0.01 per video analysis (depending on video length)
- No setup costs, no GPU requirements
- Pay-per-use pricing from Google AI
