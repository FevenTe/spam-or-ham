from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('best_spam_model.pkl')
vectorizer = joblib.load('best_vectorizer.pkl')

class MessageInput(BaseModel):
    message: str

@app.post("/predict-spam")
def predict_spam(data: MessageInput):
    text_vec = vectorizer.transform([data.message])
    prediction = model.predict(text_vec)[0]
    label = "Spam" if prediction == 1 else "Not Spam"
    
    return {
        "message": data.message,
        "prediction": label,
        "model_name": "Neural Network (MLPClassifier)",
        "f1_score": "93.24%",
        "vectorizer": "Count Vectorizer (ngram 1-2)",
        "max_features": 3000
    }
    # uvicorn server2:app --reload