import os
from src.api.main import app

# This file serves as the entry point for Hugging Face Spaces deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)