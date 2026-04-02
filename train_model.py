import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load synthetic dataset
df = pd.read_csv("nic_training_dataset.csv")

# Features and labels
X = df['Business_Description']
y = df['NIC_code']

# Vectorize text
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train classifier
model = MultinomialNB()
model.fit(X_vec, y)

# Save model and vectorizer
pickle.dump(model, open("nic_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained and saved!")