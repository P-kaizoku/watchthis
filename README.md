# WatchThis - Mood-Based Movie Recommender

A smart movie recommendation system that suggests perfect movies based on your current mood using AI-powered analysis.

## 🎬 Features

- **Mood-Based Recommendations**: Describe your mood in natural language and get personalized movie suggestions
- **AI-Powered Analysis**: Uses Groq API with Llama 3 for intelligent mood interpretation
- **Rich Movie Data**: Powered by The Movie Database (TMDB) API with comprehensive movie information
- **Smart Filtering**: Filter by genre, year, rating, and more
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Movie Details**: View detailed information including cast, director, trailers, and more

## 🚀 Tech Stack

### Backend

- **Python FastAPI** - REST API framework
- **Groq API** - AI mood analysis using Llama 3
- **TMDB API** - Movie database and metadata
- **Flask-CORS** - Cross-origin resource sharing

### Frontend

- **React.js** - User interface framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API requests
- **Lucide React** - Beautiful icons
- **CSS3** - Custom styling with gradients and animations

## 📋 Prerequisites

Before running this project, make sure you have:

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Groq API key (free at [console.groq.com](https://console.groq.com))
- TMDB API key (free at [themoviedb.org](https://www.themoviedb.org/settings/api))

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/watchthis.git
cd watchthis
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Edit .env file with your API keys
# GROQ_API_KEY=your_groq_api_key_here
# TMDB_API_KEY=your_tmdb_api_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:3000`

Visit `http://localhost:3000` in your browser to use the application!

## 🔧 Configuration

### Environment Variables

#### Backend (.env)

```env
GROQ_API_KEY=your_groq_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

#### Frontend (optional .env)

```env
REACT_APP_API_URL=http://localhost:5000
```

## 📚 API Documentation

### POST /api/recommendations

Get movie recommendations based on mood.

**Request Body:**

```json
{
  "mood": "feeling nostalgic and want something heartwarming",
  "filters": {
    "genre": "Drama",
    "year": "2020",
    "min_rating": "7"
  }
}
```

**Response:**

```json
{
  "mood": "feeling nostalgic and want something heartwarming",
  "parameters": {
    "genres": ["drama", "romance"],
    "min_rating": 7.0,
    "tone": "neutral"
  },
  "recommendations": [
    {
      "id": 12345,
      "title": "Movie Title",
      "overview": "Movie description...",
      "poster_path": "https://image.tmdb.org/...",
      "vote_average": 8.2,
      "release_date": "2020-01-01"
    }
  ]
}
```

### GET /api/movie/{id}

Get detailed information about a specific movie.

### GET /health

Health check endpoint.

## 🎨 Usage Examples

### Mood Input Examples

- "I'm feeling sad and need something uplifting"
- "Excited and want an action-packed adventure"
- "Stressed from work, need something relaxing"
- "Nostalgic for the 90s"
- "Want something scary but not too intense"

## 🚀 Deployment

### Backend Deployment (Railway)

1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables in Railway dashboard
4. Deploy automatically from main branch

### Frontend Deployment (Vercel)

1. Create account at [vercel.com](https://vercel.com)
2. Connect your GitHub repository
3. Set build command: `npm run build`
4. Set output directory: `build`
5. Add environment variable: `REACT_APP_API_URL=your_railway_backend_url`

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Roadmap

- [ ] User accounts and mood history
- [ ] Social sharing features
- [ ] Streaming platform integration
- [ ] Advanced mood analysis with image/voice input
- [ ] Group recommendation features
- [ ] Mobile app development

## 🐛 Known Issues

- Large movie posters may load slowly on slow connections
- Some older movies may have limited metadata

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for providing fast AI inference
- [The Movie Database (TMDB)](https://www.themoviedb.org) for comprehensive movie data
- [Lucide](https://lucide.dev) for beautiful icons
- [React](https://reactjs.org) team for the amazing framework

## 📞 Support

For support, email your-email@example.com or create an issue on GitHub.

---

**Happy Movie Watching! 🎬🍿**
