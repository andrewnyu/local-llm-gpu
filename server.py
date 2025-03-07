import os
import torch
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

app = FastAPI()

# ✅ Get model name from environment variable or use default
DEFAULT_MODEL = "meta-llama/Llama-3.2-3B"  # Default model for production
MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL)
print(f"🔄 Using model: {MODEL_NAME}")

# ✅ Auto-detect the best device
if torch.cuda.is_available():
    device = "cuda"  # ✅ Use GPU if available
    torch_dtype = torch.float16
else:
    device = "cpu"  # ✅ Use CPU if nothing else is available
    torch_dtype = torch.float32

print(f"🔥 Using device: {device}")

# ✅ Load Model with Debugging
try:
    print(f"🔍 Loading tokenizer for {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HUGGINGFACE_TOKEN)
    print(f"✅ Tokenizer loaded!")

    print(f"🔍 Loading model {MODEL_NAME} onto {device}...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch_dtype,
        device_map={"": device},
        token=HUGGINGFACE_TOKEN
    )
    print(f"✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Model failed to load: {e}")

@app.get("/query")
def query(text: str):
    """Generate text using the model."""
    print(f"📝 Received query: {text}")

    try:
        # ✅ Ensure input moves to the correct device
        inputs = tokenizer(text, return_tensors="pt").to(device)
        print(f"🔹 Inputs prepared!")

        # ✅ Generate text with debugging
        output = model.generate(**inputs, max_new_tokens=50)
        print(f"✅ Model inference completed!")

        # ✅ Decode response
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        print(f"📝 Response: {response}")

        return {"response": response}

    except Exception as e:
        print(f"❌ ERROR during inference: {e}")
        return {"error": str(e)}
