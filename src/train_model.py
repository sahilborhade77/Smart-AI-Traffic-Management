import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def main():
    os.makedirs('models', exist_ok=True)

    print("Loading dataset...")
    df = pd.read_csv('data/cleaned.csv')

    # Select features relevant to the roadmap (environmental and road conditions)
    features = ['Road_surface_type', 'Types_of_Junction', 'Weather_conditions', 'Light_conditions', 'Cause_of_accident']
    target = 'Accident_severity'

    # Filter out missing values for selected features
    df = df.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    # Encode categorical variables
    encoders = {}
    X_encoded = X.copy()
    for col in features:
        le = LabelEncoder()
        # Convert to string to prevent mixed type errors
        X_encoded[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
    
    X = X_encoded

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training Random Forest Classifier...")
    # Using class_weight='balanced' to handle any slight data imbalances
    rf = RandomForestClassifier(n_estimators=150, max_depth=15, random_state=42)
    rf.fit(X_train, y_train)

    # Evaluation
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*40)
    print(f"🎯 Model Accuracy: {acc * 100:.2f}%")
    print("="*40)
    
    print("\n📊 Feature Importances (Save this for your Report!):")
    importances = rf.feature_importances_
    
    # Sort importances
    sorted_idx = np.argsort(importances)[::-1]
    for idx in sorted_idx:
        print(f" - {features[idx]}: {importances[idx]*100:.2f}%")

    # Save to disk
    with open('models/rf_model.pkl', 'wb') as f:
        pickle.dump(rf, f)
        
    with open('models/encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)

    print("\n✅ Success! Saved 'rf_model.pkl' and 'encoders.pkl' to the models directory.")

if __name__ == "__main__":
    main()
