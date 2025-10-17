import os
import uvicorn
from main import app  # note: 'app.main', not 'backend.app.main'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
