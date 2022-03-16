import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sys

try:
    data = pd.read_csv(sys.argv[1])
except:
    print("Usage: python 21.py <path-to-spambase.data>")
    sys.exit(1)


# split data to features and labels
x = data.drop([57],axis='columns')
y = data[57]

# split data to train and test
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)


C_values = [0.0005]
kernal_names = ['linear', 'poly', 'rbf']
test_accuracy_table = pd.DataFrame(columns=['C', 'Linear', 'Poly', 'RBF'])
train_accuracy_table = pd.DataFrame(columns=['C', 'Linear', 'Poly', 'RBF'])

for c in C_values:
  test_accuracies = []
  train_accuracies = []
  for ker in kernal_names:

    classifier = SVC(C=c, kernel=ker , max_iter=1e8)
    classifier.fit(x_train, y_train)
    y_pred_train = classifier.predict(x_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    y_pred_test = classifier.predict(x_test)
    accuracy_test = accuracy_score(y_test, y_pred_test)
    test_accuracies.append(accuracy_test)
    train_accuracies.append(accuracy_train)

  curr_df1 = pd.DataFrame({'C': c, 'Linear': train_accuracies[0], 'Poly': train_accuracies[1], 'RBF': train_accuracies[2]}, index=[0])
  curr_df2 = pd.DataFrame({'C': c, 'Linear': test_accuracies[0], 'Poly': test_accuracies[1], 'RBF': test_accuracies[2]}, index=[0])
  train_accuracy_table =  pd.concat([train_accuracy_table, curr_df1], ignore_index=True)
  test_accuracy_table = pd.concat([test_accuracy_table, curr_df2], ignore_index=True)

print("Test Accuracy Table:\n")
print(test_accuracy_table)
print("\nTrain Accuracy Table:\n")
print(train_accuracy_table)

# make .md file
train_accuracy_table.to_markdown('train_accuracy_table.md')
test_accuracy_table.to_markdown('test_accuracy_table.md')
