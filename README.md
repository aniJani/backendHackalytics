# FastAPI Dashboard Backend

A powerful dashboard API built with FastAPI that provides data visualization, analysis, and insights capabilities. The application integrates with MongoDB Atlas for data storage and includes features like FRED API integration, OpenAI-powered insights, and dynamic visualization generation.

## Features

- 📊 Data Visualization Generation using OpenAI
- 📈 FRED Economic Data Integration
- 💾 MongoDB Atlas Database Integration
- 🔍 Dataset Analysis and Management
- 🤖 AI-Powered Business Insights
- 🔄 CORS Support for Frontend Integration

## Prerequisites

- Python 3.8+
- MongoDB Atlas Account
- OpenAI API Key
- FRED API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aniJani/backendHackalytics/tree/main
cd backendHackalytics
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your configuration:
```env
MONGODB_URL=your_mongodb_atlas_url
MONGODB_DBNAME=dashboard_db
OPENAI_API_KEY=your_openai_api_key
FRED_API_KEY=your_fred_api_key
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

### Dataset Management
- `POST /api/dataset/upload` - Upload a new dataset
- `GET /api/dataset/list` - List available datasets
- `GET /api/dataset/head` - Preview dataset contents

### Visualization
- `POST /api/visualization/generate` - Generate visualizations
- `POST /api/visualization/rerun` - Rerun existing visualizations

### FRED Integration
- `GET /api/fred/datasets` - Fetch economic datasets from FRED

### Insights
- `POST /api/insights/` - Get AI-powered insights about your data

## Testing

Run the test suite:
```bash
pytest
```

## Project Structure

```
fastapi-dashboard/
├── app/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── main.py
├── tests/
├── uploaded_files/
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
