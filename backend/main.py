# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from typing import List, Optional
from dotenv import load_dotenv
import json
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Movie Recommender API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://watchthis-black.vercel.app"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MoodRequest(BaseModel):
    mood: str
    filters: Optional[dict] = None

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    poster_path: Optional[str]
    release_date: str
    vote_average: float
    genre_ids: List[int]

class RecommendationResponse(BaseModel):
    mood: str
    movies: List[Movie]
    total_results: int
    ai_analysis: Optional[dict] = None  # NEW: Add AI analysis info

# Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "your_tmdb_api_key")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # NEW: Add Groq API key

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# NEW: Initialize Groq client
groq_client = None
if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized successfully")
    except Exception as e:
        print(f"❌ Groq client initialization failed: {e}")
        groq_client = None

# Simple mood to genre mapping (keep as fallback)
MOOD_TO_GENRES = {
    "cheerful": [35, 10751, 16],  # Comedy, Family, Animation
    "gloomy": [18, 10749],        # Drama, Romance
    "reflective": [18, 36],       # Drama, History
    "humorous": [35, 12],         # Comedy, Adventure
    "melancholy": [18, 10402],    # Drama, Music
    "idyllic": [10749, 10751],    # Romance, Family
    "chill": [35, 16, 10751],     # Comedy, Animation, Family
    "romantic": [10749, 35],      # Romance, Comedy
    "weird": [878, 14, 27],       # Sci-Fi, Fantasy, Horror
    "horny": [10749, 18],         # Romance, Drama
    "sleepy": [16, 10751, 35],    # Animation, Family, Comedy
    "angry": [28, 53, 80],        # Action, Thriller, Crime
    "fearful": [27, 53],          # Horror, Thriller
    "lonely": [18, 10749],        # Drama, Romance
    "tense": [53, 9648, 28],      # Thriller, Mystery, Action
    "thoughtful": [18, 36, 99],   # Drama, History, Documentary
    "thrill-seeking": [28, 12, 53], # Action, Adventure, Thriller
    "playful": [35, 16, 10751]    # Comedy, Animation, Family
}

# NEW: AI mood analysis function
def analyze_mood_with_ai(mood_input: str) -> dict:
    """Use Groq AI to analyze mood and return movie parameters"""
    if not groq_client:
        print("⚠️  Groq not available, using fallback")
        return get_fallback_analysis(mood_input)
    
    try:
        prompt = f"""
        Analyze this mood/feeling: "{mood_input}"
        
        Based on this mood, recommend movie parameters. Consider:
        - What genres would match this mood?
        - What rating range would be appropriate?
        - What decade/era might fit?
        - Should we avoid certain themes?
        
        Return ONLY a JSON object with this exact structure:
        {{
            "genres": [list of TMDB genre IDs],
            "min_rating": 6.0,
            "decade": "2010s or 2000s or 1990s or any",
            "keywords": ["keyword1", "keyword2"],
            "avoid_genres": [genre IDs to avoid],
            "reasoning": "brief explanation of choices"
        }}
        
        Genre IDs reference:
        - Comedy: 35, Drama: 18, Action: 28, Thriller: 53, Horror: 27
        - Romance: 10749, Sci-Fi: 878, Fantasy: 14, Animation: 16
        - Family: 10751, Adventure: 12, Crime: 80, Mystery: 9648
        - History: 36, Music: 10402, Documentary: 99
        """
        
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a movie recommendation expert. Analyze moods and return JSON parameters for finding perfect movies."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        print(f"🤖 AI Response: {result}")
        
        # Try to parse JSON from response
        try:
            # Find JSON in the response
            start = result.find('{')
            end = result.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = result[start:end]
                parsed = json.loads(json_str)
                print(f"✅ Parsed AI analysis: {parsed}")
                return parsed
            else:
                print("❌ No JSON found in AI response")
                return get_fallback_analysis(mood_input)
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return get_fallback_analysis(mood_input)
            
    except Exception as e:
        print(f"❌ Groq API call failed: {e}")
        return get_fallback_analysis(mood_input)

# NEW: Fallback analysis function
def get_fallback_analysis(mood_input: str) -> dict:
    """Fallback mood analysis when AI is not available"""
    mood = mood_input.lower()
    
    # Simple keyword matching
    if any(word in mood for word in ['happy', 'cheerful', 'upbeat', 'excited']):
        return {
            "genres": [35, 12, 16],  # Comedy, Adventure, Animation
            "min_rating": 6.5,
            "reasoning": "Fallback: Detected positive mood"
        }
    elif any(word in mood for word in ['sad', 'gloomy', 'melancholy', 'down']):
        return {
            "genres": [18, 10749],  # Drama, Romance
            "min_rating": 7.0,
            "reasoning": "Fallback: Detected reflective mood"
        }
    elif any(word in mood for word in ['angry', 'mad', 'frustrated']):
        return {
            "genres": [28, 53, 80],  # Action, Thriller, Crime
            "min_rating": 6.0,
            "reasoning": "Fallback: Detected intense mood"
        }
    elif any(word in mood for word in ['scared', 'fearful', 'nervous']):
        return {
            "genres": [35, 10751],  # Comedy, Family (comfort movies)
            "min_rating": 6.5,
            "avoid_genres": [27],  # Avoid horror
            "reasoning": "Fallback: Detected anxious mood, suggesting comfort movies"
        }
    else:
        return {
            "genres": MOOD_TO_GENRES.get(mood, [35, 18]),
            "min_rating": 6.0,
            "reasoning": "Fallback: Using basic mood mapping"
        }

@app.get("/")
async def root():
    return {"message": "Movie Recommender API is running with AI! 🤖"}

@app.get("/health")
async def health_check():
    ai_status = "available" if groq_client else "unavailable"
    return {
        "status": "healthy",
        "ai_status": ai_status,
        "features": ["mood_analysis", "tmdb_integration"]
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def get_movie_recommendations(request: MoodRequest):
    """Get AI-powered movie recommendations based on mood"""
    try:
        mood = request.mood.lower()
        
        # NEW: Use AI to analyze mood
        print(f"🎭 Analyzing mood: {request.mood}")
        ai_analysis = analyze_mood_with_ai(request.mood)
        
        # Get genres from AI analysis or fallback
        genres = ai_analysis.get("genres", MOOD_TO_GENRES.get(mood, [35, 18]))
        genre_string = ",".join(map(str, genres))
        
        # Build TMDB API request with AI insights
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre_string,
            "sort_by": "vote_average.desc",
            "vote_count.gte": 100,
            "page": 1
        }
        
        # Add AI-suggested filters
        if "min_rating" in ai_analysis:
            params["vote_average.gte"] = ai_analysis["min_rating"]
        
        # Add manual filters (override AI if provided)
        if request.filters:
            if "min_rating" in request.filters:
                params["vote_average.gte"] = request.filters["min_rating"]
            if "year" in request.filters:
                params["primary_release_year"] = request.filters["year"]
        
        print(f"🎬 TMDB query params: {params}")
        
        # Make API call to TMDB
        response = requests.get(f"{TMDB_BASE_URL}/discover/movie", params=params)
        response.raise_for_status()
        
        data = response.json()
        movies = []
        
        # Parse response and create Movie objects
        for movie_data in data["results"][:10]:  # Limit to top 10
            movie = Movie(
                id=movie_data["id"],
                title=movie_data["title"],
                overview=movie_data["overview"],
                poster_path=movie_data.get("poster_path"),
                release_date=movie_data.get("release_date", ""),
                vote_average=movie_data["vote_average"],
                genre_ids=movie_data["genre_ids"]
            )
            movies.append(movie)
        
        return RecommendationResponse(
            mood=request.mood,
            movies=movies,
            total_results=len(movies),
            ai_analysis=ai_analysis  # NEW: Include AI reasoning
        )
        
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/genres")
async def get_genres():
    """Get all available movie genres from TMDB"""
    try:
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(f"{TMDB_BASE_URL}/genre/movie/list", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")

@app.get("/movie/{movie_id}")
async def get_movie_details(movie_id: int):
    """Get detailed information about a specific movie"""
    try:
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")

# NEW: Enhanced AI endpoint
@app.post("/recommend-ai")
async def get_ai_recommendations(request: MoodRequest):
    """Advanced AI-powered recommendations with custom mood analysis"""
    return await get_movie_recommendations(request)

# NEW: Test AI analysis endpoint
@app.post("/analyze-mood")
async def analyze_mood_only(request: MoodRequest):
    """Test endpoint to see AI mood analysis without movie recommendations"""
    analysis = analyze_mood_with_ai(request.mood)
    return {
        "mood": request.mood,
        "analysis": analysis,
        "ai_available": groq_client is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)