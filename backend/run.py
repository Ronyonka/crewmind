import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get environment settings
    environment = os.getenv("ENVIRONMENT", "development")

    # Configure based on environment
    if environment == "development":
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["./"],
            log_level="info",
        )
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
