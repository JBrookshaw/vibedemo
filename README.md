# NFL Team Sentiment Visualizer

A web application that generates visual representations of fan sentiment for NFL teams by analyzing social media posts. Select a team, and the system analyzes recent public posts to create an image that reflects the current emotional state and trending topics among fans.

## Features

- 🏈 Select NFL teams through a simple UI
- 📊 Analyze recent social posts about teams and players
- 🎨 Generate images reflecting fan sentiment and topics
- 🔍 View emotion breakdowns and top discussion topics
- 📱 Responsive web interface
- 🕒 View sentiment history over time

## Quick Start

### Prerequisites

- Python 3.11 or newer
- Node.js 18+ (for future frontend builds)
- pip (Python package manager)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vibedemo.git
cd vibedemo

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the backend server
uvicorn backend.app:app --reload
```

The backend will run at http://localhost:8000

### Frontend Setup (Current PoC)

For the current prototype, simply open `frontend/index.html` in your browser. It will connect to the backend at localhost:8000.

Alternative: Serve the frontend using a basic HTTP server:
```bash
# From the frontend directory
python -m http.server 3000
```
Then visit http://localhost:3000

## Architecture

### Backend (Python/FastAPI)

- FastAPI web framework
- Modular services:
  - Ingestion service (social media posts)
  - Analysis service (emotion/topic extraction)
  - Image generation service

### Frontend (HTML/JavaScript)

- Current: Static HTML + vanilla JavaScript
- Planned: React + TypeScript SPA

### Data Flow

1. User selects NFL team
2. Backend fetches recent social posts
3. Analysis pipeline:
   - Emotion detection
   - Topic extraction
   - Verification weighting
4. Image generation based on analysis
5. Results displayed with emotion breakdown

## Development

### API Documentation

When the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests (Coming Soon)

```bash
# From the backend directory
pytest
```

### Project Structure

```
├── backend/
│   ├── app.py              # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html         # Demo UI
└── specs/                 # Feature specifications
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

[Add chosen license]

## Acknowledgments

- FastAPI for the efficient Python web framework
- NFL teams for inspiration (this is a demo project, not affiliated with NFL)