import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
df=pd.read_csv("local_QA.csv")

vectorizer=TfidfVectorizer(max_features=1000,ngram_range=(1,2),lowercase=True,max_df= 1.0, min_df=1)

tfid_matrix=vectorizer.fit_transform(df['Question'].astype(str))
joblib.dump(vectorizer,"vectorizer.pkl")
joblib.dump(tfid_matrix,"tfid_matrix.pkl")
print("model trained successfully")


