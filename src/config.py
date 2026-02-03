"""Configuration and client initialization for the Trading Research Agent."""

import os
import redis
import anthropic
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- API Keys ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found in environment variables. "
        "Please create a .env file with your API key. "
        "See .env.example for reference."
    )

# --- LLM Clients ---
CLAUDE_CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# --- Storage Clients ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

try:
    REDIS_CLIENT = redis.Redis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        decode_responses=True,
        socket_connect_timeout=5
    )
    # Test connection
    REDIS_CLIENT.ping()
except (redis.ConnectionError, redis.TimeoutError) as e:
    print(f"Warning: Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}")
    print(f"Error: {e}")
    print("Caching will be disabled. Run 'docker-compose up -d' to start Redis.")
    REDIS_CLIENT = None

try:
    QDRANT_CLIENT = QdrantClient(url=QDRANT_URL, timeout=5)
    # Test connection
    QDRANT_CLIENT.get_collections()
except Exception as e:
    print(f"Warning: Could not connect to Qdrant at {QDRANT_URL}")
    print(f"Error: {e}")
    print("Vector storage will be disabled. Run 'docker-compose up -d' to start Qdrant.")
    QDRANT_CLIENT = None

# --- Model Configuration ---
MODEL_MAP = {
    "haiku": "claude-3-haiku-20240307",  # Claude 3 Haiku
    "sonnet": "claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet (latest)
    "opus": "claude-3-opus-20240229",
}

# --- Cache TTL Settings (in seconds) ---
CACHE_TTL_COMPANY_INFO = 3600  # 1 hour
CACHE_TTL_PRICE_DATA = 900     # 15 minutes

