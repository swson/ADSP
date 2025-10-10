# Classifier Evaluation on Error-Injected Sparse Matrix Data #
This repository contains a Jupyter Notebook-based implementation of multiple classification models (e.g., AB, k-NN, DT, RF, DNN, MLP, SVM, RBM, RBM_Recon, AE_LR_CNN) to detect and analyze anomalies in performance counter data derived from error-injected sparse matrix computations.

- Loading of experimental performance counter results stored in JSON format.
- Construction of labeled datasets using dataset.py.
- Training and evaluation of multiple classifiers for anomaly detection.
- Comparison of metrics (accuracy, precision, recall, F1-score) across models.

## classifiers 
- AB: AdaBoost
- k-NN: k-Nearest Neighbors
- DT: Decision Tree
- RF: Random Forest
- DNN: Deep Neural Network
- MLP: Multi-Layer Perceptron
- SVM: Support Vector Machine
- RBM: Restricted Boltzmann Machine
- RBM_Recon: Reconstruction-based RBM
- AE_LR_CNN: Autoencoder + Logistic Regression + CNN hybrid

## Dataset 
Input data is stored as JSON files in `adsp-data/494_bus/`. These files represent PMC (Performance Monitoring Counter) outputs collected during error-injected CG computations on a fixed sparse matrix (494_bus.mtx).
The dataset.py script reads these JSON files, extracts relevant features, and creates a DataFrame suitable for classification.

## How to run 
1. Install required Python packages
`pip install -r requirements.txt`

2. Run the Jupyter Notebook
`jupyter notebook`

3. Open any notebook (e.g., `DT.ipynb`) to explore training, evaluation, and performance visualization for that model.

