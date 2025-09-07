import React, { useState } from "react";

interface Movie {
  id: number;
  title: string;
  overview: string;
  poster_path: string | null;
  release_date: string;
  vote_average: number;
  genre_ids: number[];
}

interface Mood {
  id: string;
  label: string;
  emoji: string;
  color: string;
}

interface RecommendationResponse {
  mood: string;
  movies: Movie[];
  total_results: number;
}

interface MoodRequest {
  mood: string;
  filters?: Record<string, any>;
}

const MovieRecommender: React.FC = () => {
  const [selectedMood, setSelectedMood] = useState<string>("");
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const moods: Mood[] = [
    {
      id: "cheerful",
      label: "CHEERFUL",
      emoji: "😊",
      color: "from-yellow-400 to-orange-500",
    },
    {
      id: "reflective",
      label: "REFLECTIVE",
      emoji: "🤔",
      color: "from-blue-400 to-purple-500",
    },
    {
      id: "gloomy",
      label: "GLOOMY",
      emoji: "😔",
      color: "from-gray-400 to-gray-600",
    },
    {
      id: "humorous",
      label: "HUMOROUS",
      emoji: "🤣",
      color: "from-green-400 to-blue-500",
    },
    {
      id: "melancholy",
      label: "MELANCHOLY",
      emoji: "😌",
      color: "from-indigo-400 to-purple-600",
    },
    {
      id: "idyllic",
      label: "IDYLLIC",
      emoji: "🤗",
      color: "from-pink-400 to-red-500",
    },
    {
      id: "chill",
      label: "CHILL",
      emoji: "😎",
      color: "from-cyan-400 to-blue-500",
    },
    {
      id: "romantic",
      label: "ROMANTIC",
      emoji: "🥰",
      color: "from-pink-500 to-rose-500",
    },
    {
      id: "weird",
      label: "WEIRD",
      emoji: "🤪",
      color: "from-purple-400 to-pink-500",
    },
    {
      id: "horny",
      label: "HORNY",
      emoji: "😏",
      color: "from-red-500 to-pink-600",
    },
    {
      id: "sleepy",
      label: "SLEEPY",
      emoji: "😴",
      color: "from-blue-300 to-indigo-400",
    },
    {
      id: "angry",
      label: "ANGRY",
      emoji: "😠",
      color: "from-red-500 to-red-700",
    },
    {
      id: "fearful",
      label: "FEARFUL",
      emoji: "😰",
      color: "from-gray-500 to-gray-700",
    },
    {
      id: "lonely",
      label: "LONELY",
      emoji: "😢",
      color: "from-blue-500 to-gray-600",
    },
    {
      id: "tense",
      label: "TENSE",
      emoji: "😬",
      color: "from-orange-500 to-red-600",
    },
    {
      id: "thoughtful",
      label: "THOUGHTFUL",
      emoji: "🤓",
      color: "from-indigo-500 to-purple-600",
    },
    {
      id: "thrill-seeking",
      label: "THRILL-SEEKING",
      emoji: "🤩",
      color: "from-yellow-500 to-red-600",
    },
    {
      id: "playful",
      label: "PLAYFUL",
      emoji: "😄",
      color: "from-green-400 to-yellow-500",
    },
  ];

  const getMovieRecommendations = async (mood: string): Promise<void> => {
    setLoading(true);
    setError("");
    setSelectedMood(mood);

    try {
      const requestBody: MoodRequest = { mood };

      const response = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: RecommendationResponse = await response.json();
      setMovies(data.movies);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Unknown error occurred";
      setError("Failed to get movie recommendations. Please try again.");
      console.error("Error:", errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const resetSearch = (): void => {
    setSelectedMood("");
    setMovies([]);
    setError("");
  };

  const handleImageError = (
    e: React.SyntheticEvent<HTMLImageElement, Event>
  ): void => {
    const target = e.target as HTMLImageElement;
    const movie = movies.find((m) => target.alt === m.title);
    if (movie) {
      target.src = `https://via.placeholder.com/300x450/4B5563/FFFFFF?text=${encodeURIComponent(
        movie.title
      )}`;
    }
  };

  const formatYear = (dateString: string): string => {
    return dateString ? new Date(dateString).getFullYear().toString() : "N/A";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 bg-gradient-to-r from-white to-purple-200 bg-clip-text ">
            Discover top-rated movies based on your mood
          </h1>
          <p className="text-xl text-purple-200 mb-8">
            How are you feeling now?
          </p>
        </div>

        {/* Mood Selection Grid */}
        {!selectedMood && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-w-6xl mx-auto mb-8">
            {moods.map((mood: Mood) => (
              <button
                key={mood.id}
                onClick={() => getMovieRecommendations(mood.id)}
                className={`bg-gradient-to-r ${mood.color} hover:scale-105 transform transition-all duration-300 rounded-xl p-6 text-white font-bold text-lg shadow-lg hover:shadow-2xl border-2 border-transparent hover:border-white/20`}
                type="button"
                aria-label={`Get ${mood.label.toLowerCase()} movies`}
              >
                <div className="text-3xl mb-2">{mood.emoji}</div>
                <div>{mood.label}</div>
              </button>
            ))}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
            <p className="text-white text-xl">
              Finding perfect movies for your mood...
            </p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-8">
            <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-6 max-w-md mx-auto">
              <p className="text-red-200 text-lg">{error}</p>
              <button
                onClick={() => getMovieRecommendations(selectedMood)}
                className="mt-4 bg-red-500 hover:bg-red-600 px-6 py-2 rounded-lg text-white font-semibold transition-colors"
                type="button"
              >
                Try Again
              </button>
            </div>
          </div>
        )}

        {/* Movie Results */}
        {movies.length > 0 && (
          <div className="max-w-7xl mx-auto">
            {/* Results Header */}
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-3xl font-bold text-white">
                Movies for your{" "}
                <span className="text-purple-300 capitalize">
                  {selectedMood}
                </span>{" "}
                mood
              </h2>
              <div className="flex gap-4">
                <button
                  onClick={resetSearch}
                  className="bg-white/10 hover:bg-white/20 border border-white/30 px-6 py-2 rounded-lg text-white font-semibold transition-all duration-200 backdrop-blur-sm"
                  type="button"
                >
                  Another mood?
                </button>
                <button
                  className="bg-white/10 hover:bg-white/20 border border-white/30 px-6 py-2 rounded-lg text-white font-semibold transition-all duration-200 backdrop-blur-sm"
                  type="button"
                  onClick={() => getMovieRecommendations(selectedMood)}
                >
                  Refresh
                </button>
              </div>
            </div>

            {/* Movies Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {movies.map((movie: Movie) => (
                <div
                  key={movie.id}
                  className="bg-white/10 backdrop-blur-md rounded-xl overflow-hidden shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 border border-white/20"
                >
                  {/* Movie Poster */}
                  <div className="aspect-[2/3] bg-gray-700 relative overflow-hidden">
                    {movie.poster_path ? (
                      <img
                        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                        alt={movie.title}
                        className="w-full h-full object-cover"
                        onError={handleImageError}
                        loading="lazy"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        <div className="text-center p-4">
                          <div className="text-4xl mb-2">🎬</div>
                          <div className="text-sm font-medium">
                            {movie.title}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Rating Badge */}
                    <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                      ⭐ {movie.vote_average.toFixed(1)}
                    </div>

                    {/* AI Recommended Badge */}

                    <div className="absolute top-2 left-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-2 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                      🤖 AI Pick
                    </div>
                  </div>

                  {/* Movie Info */}
                  <div className="p-4">
                    <h3 className="font-bold text-white text-lg mb-2 line-clamp-2">
                      {movie.title}
                    </h3>
                    <p className="text-gray-300 text-sm mb-3 line-clamp-3">
                      {movie.overview}
                    </p>
                    <div className="flex justify-between items-center text-sm text-gray-400">
                      <span>{formatYear(movie.release_date)}</span>
                      <span className="text-purple-300 cursor-pointer hover:text-purple-200 transition-colors">
                        View Details
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-16 text-purple-300">
          <p>Made with 💜 by You</p>
        </div>
      </div>
    </div>
  );
};

export default MovieRecommender;
