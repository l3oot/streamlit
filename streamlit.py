import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def main():
    st.title('Machine Learning App')
    
    # File upload
    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())
        
        # Select features and target
        target_column = st.selectbox("Select target column", df.columns)
        feature_columns = st.multiselect("Select feature columns", 
                                       [col for col in df.columns if col != target_column])
        
        if len(feature_columns) > 0:
            # Prepare data
            X = df[feature_columns]
            y = df[target_column]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            if st.button('Train Model'):
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train_scaled, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test_scaled)
                accuracy = accuracy_score(y_test, y_pred)
                
                # Show results
                st.write(f"Model Accuracy: {accuracy:.2%}")
                
                # Feature importance
                importance_df = pd.DataFrame({
                    'Feature': feature_columns,
                    'Importance': model.feature_importances_
                })
                st.write("Feature Importance:")
                st.bar_chart(importance_df.set_index('Feature'))
                
                # Make new predictions
                st.subheader("Make Predictions")
                user_input = {}
                for feature in feature_columns:
                    user_input[feature] = st.number_input(f"Enter {feature}:", value=float(df[feature].mean()))
                
                if st.button('Predict'):
                    # Prepare input data
                    input_data = pd.DataFrame([user_input])
                    input_scaled = scaler.transform(input_data)
                    
                    # Make prediction
                    prediction = model.predict(input_scaled)
                    st.write(f"Prediction: {prediction[0]}")

if __name__ == '__main__':
    main()