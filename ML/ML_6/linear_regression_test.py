import joblib
import pandas as pd

model_filename = "artefacts/final_sgd_reg_model.joblib"
preprocessor_filename = "artefacts/data_preprocessor.joblib"

loaded_model = joblib.load(model_filename)
loaded_preprocessor = joblib.load(preprocessor_filename)

FEATURE_COLUMNS = [
    'crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 
    'dis', 'rad', 'tax', 'ptratio', 'black', 'lstat'
]

def make_prediction_from_list(input_list, feature_names, loaded_model, loaded_preprocessor):
    X_input = pd.DataFrame([input_list], columns=feature_names)
    # print(f"\nInput DataFrame:\n{X_input}")

    X_input_processed = loaded_preprocessor.transform(X_input)
    predictions = loaded_model.predict(X_input_processed)
    # print(predictions[0])
    return predictions[0]

test_features_list = [
    input("Enter a value of crim : "),    # crim
    0,     # zn
    18.1,  # indus
    0,     # chas
    0.7,   # nox
    4.0,   # rm 
    100,   # age
    1.0,   # dis 
    24,    # rad
    666,   # tax
    20.2,  # ptratio
    300,   # black
    30     # lstat 
]

predicted_value = make_prediction_from_list(test_features_list, FEATURE_COLUMNS, loaded_model, loaded_preprocessor)

print(f"Predicted medv: {predicted_value:.2f}")