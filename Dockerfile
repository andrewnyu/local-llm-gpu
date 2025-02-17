# ✅ Use a lightweight Ubuntu base image with CUDA support (for GPUs)
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# ✅ Set working directory
WORKDIR /app

# ✅ Install system dependencies
RUN apt update && apt install -y python3 python3-pip git curl

# ✅ Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn torch transformers accelerate sentence-transformers python-dotenv

# ✅ Copy FastAPI server and `.env`
COPY server.py .  
COPY .env .

# ✅ Expose API port
EXPOSE 8000

# ✅ Start FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
