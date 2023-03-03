# Copyright contributors to the ai-on-z-triton-is-examples project.

# rfc_train.py
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn2pmml import sklearn2pmml
from sklearn2pmml import PMMLPipeline

# Note: This example borrows from https://github.com/IBM/snapml-examples

# Load training data
X, y = datasets.load_breast_cancer(return_X_y=True)

# Train a PMML pipeline and save it in PMML format
# To be used by Snap ML which imports the Sklearn model into its optimized predict engine

model = RandomForestClassifier(n_estimators = 100, max_depth=4)
pipeline = PMMLPipeline([("model", model)]).fit(X,y)
sklearn2pmml(pipeline, "model.pmml", with_repr=True)
