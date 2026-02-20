import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

X = np.array([

    # NORMAL
    [10, 5, 60],
    [20, 10, 70],
    [25, 15, 80],
    [30, 20, 90],

    # CPU
    [150, 10, 80],
    [180, 15, 90],
    [200, 20, 100],

    # MEMORY
    [20, 60, 90],
    [30, 65, 95],
    [40, 70, 100],

    # CPU + MEMORY
    [170, 60, 110],
    [190, 70, 120],

    # ALL
    [180, 70, 300],
    [200, 80, 350]
])

y = np.array([
    0,0,0,0,
    1,1,1,
    2,2,2,
    3,3,
    4,4
])

model = LogisticRegression(max_iter=800)
model.fit(X, y)

joblib.dump(model, "controller/model/model.pkl")

print("Model retrained successfully.")