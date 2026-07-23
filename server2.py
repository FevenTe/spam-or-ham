from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI()

# Enable CORS so your React frontend can talk to this backend smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Load your saved champion model and vectorizer on startup
model = joblib.load('best_spam_model.pkl')
vectorizer = joblib.load('best_vectorizer.pkl')

# 2. Define the expected incoming JSON structure from the frontend
class MessageInput(BaseModel):
    message: str

@app.post("/predict-spam")
def predict_spam(data: MessageInput):
    # Transform raw text into the 3,000-feature count matrix
    text_vec = vectorizer.transform([data.message])
    
    # Predict (1 for Spam, 0 for Ham)
    prediction = model.predict(text_vec)[0]
    
    label = "Spam" if prediction == 1 else "Not Spam"
    
    return {
        "message": data.message,
        "prediction": label
    }