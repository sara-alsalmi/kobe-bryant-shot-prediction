# Kobe Bryant Shot Prediction 

Predict whether Kobe Bryant made or missed a shot using machine learning.

## Dataset

[Kobe Bryant Shot Selection](https://www.kaggle.com/competitions/kobe-bryant-shot-selection/data) from Kaggle: the shots Kobe took during his NBA career, with details like shot location, distance, type and time.

## Models

- K-Nearest Neighbors (KNN)
- Logistic Regression

## Files

| File | What it is |
|---|---|
| `Final.ipynb` | Main notebook: EDA, preprocessing, training and evaluation |
| `Experiments.ipynb` | Extra experiments to try to improve the model |
| `dataset/data.csv` | The dataset |
| `streamlit_app/` | A small basketball game app that uses the model |

## Run the app

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```
