import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")
data = shuffle(data, random_state=42)

X = data.drop("label", axis=1)
Y = data["label"]

# Normalize data (VERY IMPORTANT)
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# Train SVM with probability
classifier = SVC(kernel="rbf", probability=True)
classifier.fit(X_train, Y_train)

# Evaluate model
Y_pred = classifier.predict(X_test)
acc = accuracy_score(Y_test, Y_pred)

print(f"Model Accuracy: {acc*100:.2f}%")
print(classification_report(Y_test, Y_pred))

# Save model and scaler
joblib.dump(classifier, "model/letter_prob_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
