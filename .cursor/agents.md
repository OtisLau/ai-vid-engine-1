PROJECT TITLE:

AI Video Effect Detector (Engine 1 MVP)

PROJECT SUMMARY (HIGH-LEVEL)

This project creates the MVP version of Engine 1 of a bigger AI video editing system.
For the MVP:

User Flow:

User uploads a short video clip (5–10 seconds).

Backend uses the latest Gemini model (2.0 Flash Exp or 1.5 Pro) to analyze the entire video.

Backend classifies the video editing effect using AI semantic understanding.

Backend outputs a structured JSON response, containing:

the predicted effect

confidence score

description of the effect

This is the only functionality required for MVP.

No timeline, no rendering, no block generation, no UI effects, no additional ML models.
Just video → effect classification using Gemini's video understanding.

---

## 📋 DETAILED IMPLEMENTATION PLAN (8 Days)

### **Day 1: Foundation & Setup**
**Objectives:** Environment setup, API access, basic project structure

**Tasks:**
- [ ] Install Python dependencies (`fastapi`, `uvicorn`, `google-generativeai`)
- [ ] Get Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Set up environment variable: `export GEMINI_API_KEY="your-key"`
- [ ] Create project folder structure
- [ ] Test Gemini API connectivity with `test_gemini.py`

**Deliverables:**
- Working Python environment with Gemini access
- Basic project structure established
- API key validated

### **Day 2-3: Backend API Development**
**Objectives:** Complete FastAPI server with Gemini integration

**Tasks:**
- [ ] Implement FastAPI server (`backend/main.py`)
- [ ] Add `/classify` endpoint with video upload support
- [ ] Integrate Gemini 2.0 Flash Exp (fallback to 1.5 Pro)
- [ ] Implement file validation (format, size limits)
- [ ] Add comprehensive error handling
- [ ] Create structured analysis prompts for video effects
- [ ] Parse and validate Gemini JSON responses
- [ ] Add CORS middleware for frontend integration

**Deliverables:**
- Fully functional `/classify` API endpoint
- Gemini video analysis working
- Error handling for all edge cases
- API documentation

### **Day 4-5: Frontend Development**
**Objectives:** Create user-friendly web interface

**Tasks:**
- [ ] Design HTML interface with drag-and-drop upload
- [ ] Implement JavaScript for file handling and API calls
- [ ] Add loading states and progress indicators
- [ ] Create results visualization (effect name, confidence bar, description)
- [ ] Add debug section showing raw API responses
- [ ] Implement error display and user feedback
- [ ] Style for mobile responsiveness
- [ ] Test cross-browser compatibility

**Deliverables:**
- Complete web interface at `frontend/index.html`
- Drag-and-drop video upload working
- Real-time results display
- Professional UI/UX

### **Day 6-7: Testing & Validation**
**Objectives:** Comprehensive testing of all functionality

**Tasks:**
- [ ] Create test video library (examples of each effect type)
- [ ] Test all 10 effect categories (hard_cut, crossfade, whip_pan, etc.)
- [ ] Validate accuracy and confidence scoring
- [ ] Performance testing (response times, file sizes)
- [ ] Error handling validation (invalid files, network issues)
- [ ] Cross-platform testing (different browsers, video formats)
- [ ] Load testing with multiple concurrent requests
- [ ] API rate limit testing and handling

**Deliverables:**
- Test results report
- Performance benchmarks
- Bug fixes and optimizations
- Confidence in system reliability

### **Day 8: Launch Preparation**
**Objectives:** Final polish and documentation

**Tasks:**
- [ ] Complete README with setup instructions
- [ ] Create deployment guide
- [ ] Add environment configuration examples
- [ ] Document API endpoints and responses
- [ ] Create troubleshooting guide
- [ ] Final user experience testing
- [ ] Performance optimization
- [ ] Code cleanup and comments

**Deliverables:**
- Production-ready system
- Complete documentation
- Deployment instructions
- User guide

---

## 🎯 SUCCESS CRITERIA

### **Functional Requirements ✅**
- [ ] Video upload via drag-and-drop or file picker
- [ ] Analysis completes in < 60 seconds
- [ ] Returns accurate effect classification
- [ ] Provides confidence score (0.0-1.0)
- [ ] Includes descriptive explanation
- [ ] Handles all supported video formats
- [ ] Robust error handling and user feedback

### **Technical Requirements ✅**
- [ ] Gemini API integration working
- [ ] FastAPI server running locally
- [ ] File size limits (50MB max)
- [ ] CORS enabled for frontend
- [ ] JSON API responses
- [ ] Temporary file cleanup
- [ ] No memory leaks

### **Quality Requirements ✅**
- [ ] > 80% accuracy on test videos
- [ ] Intuitive user interface
- [ ] Clear error messages
- [ ] Debug information available
- [ ] Mobile-responsive design
- [ ] Professional appearance

---

## 💰 COST ANALYSIS

### **Development Costs (One-time)**
- **Time:** 8 days developer effort
- **Tools:** Free (VS Code, Python, Git)
- **Testing:** Sample videos (free to create)

### **Runtime Costs (Per Video)**
- **Gemini API:** $0.002-0.01 per analysis
- **Example:** 1,000 videos/month = $2-10
- **Infrastructure:** Local development = $0
- **Internet:** Required for API calls

### **Scaling Considerations**
- API costs scale linearly with usage
- No server infrastructure costs
- Easy to implement caching for repeated analyses
- Rate limiting can control costs

---

## 🚨 RISKS & MITIGATIONS

### **High Risk**
1. **Gemini API Access Issues**
   - Risk: API key problems, rate limits, service outages
   - Mitigation: Clear setup instructions, error handling, fallback messaging

2. **Video Format Compatibility**
   - Risk: Unsupported codecs or corrupted files
   - Mitigation: Client-side validation, clear error messages, format documentation

### **Medium Risk**
1. **Accuracy Expectations**
   - Risk: Gemini may not perfectly classify subtle effects
   - Mitigation: Clear documentation of capabilities, "unknown" fallback, user education

2. **Performance Variability**
   - Risk: API response times vary by video complexity
   - Mitigation: Progress indicators, timeout handling, user expectations setting

### **Low Risk**
1. **Browser Compatibility**
   - Risk: Drag-and-drop not working in older browsers
   - Mitigation: Fallback file input, progressive enhancement

2. **File Size Issues**
   - Risk: Large videos causing timeouts
   - Mitigation: Size limits, compression hints, progress feedback

---

## 🔄 DEPLOYMENT & USAGE

### **Local Development**
```bash
# Setup
cd backend
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
python main.py

# Frontend served via FastAPI or separate server
# Access at http://localhost:8000
```

### **Production Deployment**
- Environment variable configuration
- API key security (never in code)
- Error monitoring (optional)
- CDN for frontend assets (optional)

### **User Workflow**
1. Open web interface
2. Drag & drop video file (5-10 seconds)
3. Wait for AI analysis (~30-60 seconds)
4. View results: effect type, confidence, description
5. Use debug section for technical details

---

## 🎉 FINAL VALIDATION CHECKLIST

**Before launch, verify:**
- [ ] Gemini API key configured and tested
- [ ] All 10 effect types working
- [ ] Response times acceptable (< 60s)
- [ ] Error handling comprehensive
- [ ] Frontend fully functional
- [ ] Documentation complete
- [ ] Test videos prepared
- [ ] Performance benchmarks met
- [ ] Cost expectations clear

**MVP Success = Working video effect classifier with good UX!**

🚀 MVP SCOPE (WHAT WE BUILD NOW)
IN SCOPE:

FFmpeg-based frame extraction

Preprocessing frames

Running X3D-S model (ONNX Runtime)

Running SlowFast model (ONNX Runtime)

Fusion logic to combine predictions

FastAPI backend with /classify endpoint

Simple HTML/React frontend to upload video

JSON result display

OUT OF SCOPE (DO NOT BUILD IN MVP):

Video editor UI

Timeline

Effect block generator

LLM explanations

Rendering/exporting

Masking/segmentation

Motion tracking

Overlays/textures

Fine-tuning models

Cloud inference

GPU acceleration beyond ONNX Runtime

Multi-user functionality

Authentication

🎬 EFFECT CLASSES FOR MVP

We classify only 10 base effects that cover 80% of UGC transitions:

CLASSES = [
  "hard_cut",
  "crossfade",
  "whip_pan",
  "zoom_cut",
  "speed_ramp",
  "shake_transition",
  "flash_frame",
  "reverse_effect",
  "match_cut",
  "unknown"
]


If confidence is below threshold → return "unknown".

🧠 MODELS TO USE (VERY IMPORTANT)
Primary Model (Google Gemini AI):

Gemini 2.0 Flash Experimental (latest video understanding model)

Model requirements:

API-based (no local model storage)

run via Google Generative AI SDK

automatic video format support

semantic understanding of editing effects

confidence scoring and natural language descriptions

🎬 VIDEO ANALYSIS (GEMINI AI)

Gemini directly analyzes uploaded video files without preprocessing.

Analysis capabilities:
- Native video format support (MP4, MOV, AVI, etc.)
- Full temporal understanding (no frame extraction needed)
- Semantic comprehension of editing techniques
- Confidence scoring and detailed descriptions

Requirements:

Videos uploaded directly to Gemini API

Automatic format detection and processing

No local video processing required

Temporary file cleanup after analysis

🔧 GEMINI ANALYSIS (REQUIRED)

Gemini analyzes the complete video and returns structured classification.

Example response:

Gemini → {"effect": "crossfade", "confidence": 0.92, "description": "Gradual dissolve transition between scenes"}


The backend must:

Upload video file to Gemini API

Send structured analysis prompt

Parse JSON response from Gemini

Validate response format and content

⚖️ PREDICTION LOGIC (REQUIRED)

Gemini AI provides direct classification with confidence:

RULE 1 — Gemini determines effect based on video content analysis

RULE 2 — Validate effect is in allowed categories (fallback to "unknown")

RULE 3 — Ensure confidence is between 0.0-1.0

RULE 4 — Include descriptive explanation from Gemini

Output example:

{
  "effect": "whip_pan",
  "confidence": 0.94,
  "description": "Fast camera pan with motion blur transitioning between two scenes",
  "model_used": "gemini-latest"
}

📡 BACKEND API REQUIREMENTS
FastAPI Endpoint: /classify

Method:

POST /classify
Content-Type: multipart/form-data
file: video.mp4

Response Format:
{
  "effect": "whip_pan",
  "confidence": 0.94,
  "description": "Fast camera pan with motion blur transitioning between two scenes",
  "model_used": "gemini-latest"
}

Error responses:

invalid file type/format

file too large (>50MB)

API key not configured

Gemini API error

video analysis timeout

📁 REQUIRED FOLDER STRUCTURE
project/
  backend/
    main.py                 # FastAPI app with Gemini integration
    requirements.txt        # Python dependencies
    test_gemini.py         # Setup validation script
    README.md              # Complete setup guide
  frontend/
    index.html             # Drag-drop video upload interface

🛠️ BACKEND PROCESSING PIPELINE

Receive video upload

Validate file (format, size)

Upload video to Gemini API

Send analysis prompt with effect categories

Receive JSON classification response

Validate and format response

Return structured JSON result

Clean up temporary files

⚙️ IMPORTANT DEVELOPMENT RULES FOR CURSOR AGENTS
GENERAL

Code must run locally on macOS (M2).

Gemini API requires internet connection.

Use typed Python code (PEP 484).

Add comprehensive error handling.

API REQUIREMENTS

Gemini API key must be configured via environment variable.

Handle API rate limits and timeouts gracefully.

Validate all API responses before processing.

FASTAPI BEHAVIOR

Must support CORS for frontend integration

Must handle video file uploads (50MB limit)

Must return consistent JSON responses

Must provide detailed error messages

FRONTEND

Must support drag/drop + file upload

Must POST multipart/form-data to /classify

Must display:

predicted effect with description

confidence visualization (bar chart)

raw API response in debug section

loading states and error handling

🔥 FUTURE PHASES (DO NOT BUILD, ONLY DOCUMENT)

For Cursor context, list but do NOT implement:

effect block generator (Engine 2)

timeline editor

rendering pipeline

LLM explanations

segmentation-based effects

multi-model combinations

product ad effect matching

timestamp targeted effect queries (“what is happening at 0:12?”)

These are later phases.

✅ WHAT SUCCESS LOOKS LIKE FOR MVP

User uploads a video → Gemini AI analyzes → returns effect classification with description.

Two examples:

Example 1:

User uploads a whip pan:

{
  "effect": "whip_pan",
  "confidence": 0.94,
  "description": "Fast camera pan with motion blur transitioning between two scenes",
  "model_used": "gemini-latest"
}

Example 2:

User uploads a crossfade:

{
  "effect": "crossfade",
  "confidence": 0.89,
  "description": "Gradual dissolve transition between two shots over 2 seconds",
  "model_used": "gemini-latest"
}

🎯 MVP VALIDATION CHECKLIST

- [ ] Gemini API key configured and working
- [ ] Video upload and analysis working (< 60 seconds)
- [ ] All 10 effect types detectable
- [ ] Confidence scores meaningful (0.0-1.0)
- [ ] Descriptive explanations provided
- [ ] Error handling robust
- [ ] Frontend drag-drop functional
- [ ] Debug mode shows raw API responses

This is the complete Gemini-powered MVP.