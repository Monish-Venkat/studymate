from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    APP_NAME: str = 'EduRAG'
    APP_ENV: str = 'development'
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    DATA_DIR: str = 'data'
    DB_DIR: str = 'data/db'
    QUESTION_PAPERS_DIR: str = 'data/question_papers'
    SYLLABUS_DIR: str = 'data/syllabus'
    TEXTBOOKS_DIR: str = 'data/textbooks'
    EMBED_MODEL: str = 'sentence-transformers/all-MiniLM-L6-v2'
    VLLM_BASE_URL: str = 'http://localhost:11434'
    VECTOR_DIR: str = 'data/db/faiss'
    TOP_K: int = 5
    EMBED_THREADS: int = 4
    DOCUMENT_TOKENS: int = 500
    DOCUMENT_OVERLAP: int = 50
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 120
    MIN_SIMILARITY: float = 0.3
    PERSONA_MIN_SIMILARITY: float = 0.3
    STORAGE_KEY: str = ''
    RETENTION_DAYS: int = 30
    TEACHER_API_KEY: str = ''
    TELEGRAM_BOT_TOKEN: str = ''
    TELEGRAM_WEBHOOK_SECRET: str = ''
    PUBLIC_APP_URL: str = 'http://127.0.0.1:3000'
    WHISPER_MODEL: str = 'base'
    ENABLE_GTTS: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    LLM_MAIN_MODEL: str = 'qwen2.5:3b'
    LLM_SOCRATIC_MODEL: str = 'qwen2.5:3b'
    LLM_SMALL_MODEL: str = 'qwen2.5:3b'
    # The 3B model cannot hold a 15-question blueprint in valid JSON; paper
    # generation needs the larger model even though it only partly fits in VRAM.
    LLM_MOCK_MODEL: str = 'qwen2.5:7b'
    # CPU-only hosts generate in minutes, not seconds: an 8192-token mock paper
    # takes roughly half an hour at a few tokens per second.
    LLM_TIMEOUT_SECONDS: float = 3600.0
    # Empty keeps inference on the local Ollama runtime. Set only to reach an
    # OpenAI-compatible endpoint that requires bearer auth.
    LLM_API_KEY: str = ''
    # 'google' mints and refreshes an access token from application default
    # credentials instead of using the static LLM_API_KEY.
    LLM_AUTH: str = ''
    # Default backend for model names with no "ollama:"/"vertex:" prefix.
    # Any LLM_*_MODEL may carry a prefix to override this per task, so local
    # and cloud models can serve different tools at the same time.
    LLM_PROVIDER: str = 'ollama'
    # Full chat-completions URL, for providers whose path is not
    # "<base>/v1/chat/completions" (Vertex AI). Empty keeps the Ollama path.
    LLM_CHAT_URL: str = ''
    SUBJECTS: str = 'physics,chemistry,mathematics,biology'
    LEVELS: str = '1st,2nd'
    QUESTION_PAPER_BOARDS: str = 'cbse,ka'

    def subjects_list(self):
        return [s.strip() for s in self.SUBJECTS.split(',') if s.strip()]

    def levels_list(self):
        return [s.strip() for s in self.LEVELS.split(',') if s.strip()]

    def boards_list(self):
        return [s.strip() for s in self.QUESTION_PAPER_BOARDS.split(',') if s.strip()]

settings = Settings()
