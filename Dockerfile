# Use RunPod's PyTorch image as base
FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04

# ✅ Set working directory
WORKDIR /app

# ✅ Install system dependencies
RUN apt update && apt install -y python3 python3-pip git curl

# ✅ Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn torch transformers accelerate sentence-transformers python-dotenv

# ✅ Copy FastAPI server and `.env`
COPY server.py .  
COPY .env .

# ✅ Create a custom entrypoint script to bypass the NVIDIA script
RUN echo '#!/bin/bash' > /app/entrypoint.sh && \
    echo 'set -e' >> /app/entrypoint.sh && \
    echo '' >> /app/entrypoint.sh && \
    echo '# Execute the command passed to docker run' >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# ✅ Expose API port
EXPOSE 8000

# ✅ Use our custom entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
