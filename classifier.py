import pickle

def predict(X_test):
	with open('model', 'rb') as f:
		rf_classifier = pickle.load(f)
	
	y_pred = rf_classifier.predict([X_test])[0]

	if y_pred == 0:
		print("This app is Benign")
	else:
		print("This app is Piggybacked")