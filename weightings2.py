import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler

# Load your CSV
df = pd.read_csv("fdata.csv")

# Set the target column
target_col = "Wins"

# Columns to exclude from training
exclude = ["Name", "Jersey Number", "Club", "Nationality", "Position", target_col]
X = df.drop(columns=exclude)
y = df[target_col]

# Fill missing values and scale features
X = X.fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
feature_names = X.columns.tolist()

# Manual weights (you can fine-tune these)
manual_weights = {
    "Age": -0.05,
    "Appearances": 0.2,
    "Goals": 0.3,
    "Shots": 0.1,
    "Shots on target": 0.2,
    "Clean sheets": 0.05,
    "Goals conceded": -0.15,
    "Tackle success %": 0.05,
    "Blocked shots": 0.05,
    "Interceptions": 0.05,
    "Clearances": 0.05,
    "Successful 50/50s": 0.03,
    "Aerial battles won": 0.03,
    "Assists": 0.3,
    "Passes": 0.1,
    "Crosses": 0.05,
    "Through balls": 0.05,
    "Accurate long balls": 0.05,
    "Saves": 0.2,
    "Catches": 0.1,
    "Sweeper clearances": 0.05,
    "Goal Kicks": 0.05,
    "Yellow cards": -0.1,
    "Red cards": -0.3,
    "Fouls": -0.2,
    "Offsides": -0.1
}

# Normalize manual weights
total_manual = sum(abs(v) for v in manual_weights.values())
manual_weights = {k: v / total_manual for k, v in manual_weights.items()}

# Train ElasticNet on Wins
model = ElasticNet(alpha=0.1, l1_ratio=0.5)
model.fit(X_scaled, y)

# Extract and normalize model coefficients
coefs = dict(zip(feature_names, model.coef_))
total_learned = sum(abs(v) for v in coefs.values() if v != 0)
learned_weights = {k: v / total_learned for k, v in coefs.items() if v != 0}

# Blend manual and learned weights
blend_alpha = 0.5  # 0 = only learned, 1 = only manual
final_weights = {
    k: blend_alpha * manual_weights.get(k, 0) + (1 - blend_alpha) * learned_weights.get(k, 0)
    for k in set(manual_weights) | set(learned_weights)
}

# Convert to weight vector and compute hybrid rating
weights_vector = np.array([final_weights.get(f, 0) for f in feature_names])
df["Hybrid Rating"] = X_scaled @ weights_vector

# Save and preview
df[["Name", "Position", "Wins", "Hybrid Rating"]].to_csv("hybrid_player_ratings.csv", index=False)
print(df[["Name", "Position", "Wins", "Hybrid Rating"]].sort_values(by="Hybrid Rating", ascending=False).head(10))
