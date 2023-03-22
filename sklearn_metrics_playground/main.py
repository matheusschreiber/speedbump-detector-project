import numpy as np
from sklearn.metrics import average_precision_score
y_true = np.array([1])
y_scores = np.array([0.01])

print(average_precision_score(y_true, y_scores))