import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Function to load data, train, evaluate models, and output feature importances
def process_data(file_path, model_name_suffix=""):
    # Load the data
    df = pd.read_csv(file_path)

    # Split the data into 60% training, 20% validation, and 20% testing
    train_size = int(0.60 * len(df))
    val_size = int(0.20 * len(df))

    # Adjusted Splits for Time-Series Data
    train_df = df.iloc[:train_size]
    val_df = df.iloc[train_size:train_size + val_size]
    test_df = df.iloc[train_size + val_size:]

    # Separate features and labels
    X_train = train_df.drop(columns=['File', 'Label'])  # Features
    y_train = train_df['Label'].astype(int)  # Labels

    X_val = val_df.drop(columns=['File', 'Label'])
    y_val = val_df['Label'].astype(int)

    X_test = test_df.drop(columns=['File', 'Label'])
    y_test = test_df['Label'].astype(int)

    # Feature names for later use
    feature_names = X_train.columns

    # Scale the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    # Train Random Forest
    rf_model = RandomForestClassifier(class_weight='balanced', random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict_proba(X_test)[:, 1]

    # logistic regression model
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict_proba(X_test)[:, 1]

    # Evaluate model
    def evaluate_model(y_true, y_pred, model_name, threshold):
        pred = (y_pred >= threshold).astype(int)
        accuracy = accuracy_score(y_true, pred)
        precision = precision_score(y_true, pred)
        recall = recall_score(y_true, pred)
        auc = roc_auc_score(y_true, y_pred)

        print(f"Performance of {model_name}:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"AUC: {auc:.4f}")
        print('-' * 30)

    evaluate_model(y_test, rf_pred, f"Random Forest {model_name_suffix}", threshold=0.5)
    evaluate_model(y_test, lr_pred, f"Logistic Regression {model_name_suffix}", threshold=0.5)

    # Feature importance
    feature_importances = rf_model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)

    # Save feature importances to CSV
    importance_csv_path = f'feature_importances_{model_name_suffix.replace(" ", "_")}.csv'
    importance_df.to_csv(importance_csv_path, index=False)
    print(f"Feature importances saved to {importance_csv_path}")

    # Plot feature importances
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title(f'Feature Importances ({model_name_suffix})')
    plt.gca().invert_yaxis()  # Most important at the top
    plt.tight_layout()
    plt.show()

# Process the data and output feature importances
process_data('event_matrix.csv', model_name_suffix="Error Detection")
