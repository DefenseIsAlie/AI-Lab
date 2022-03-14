import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sys

path = sys.argv[1]

data = pd.read_csv(path,header=None)

# split data to features and labels
x = data.drop([57],axis='columns')
y = data[57]

# split data to train and test
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)


C_values = [0.0005]
kernal_names = ['linear', 'poly', 'rbf']
accuracy_table = pd.DataFrame(columns=['C', 'Linear', 'Poly', 'RBF'])

for c in C_values:
  accuracies = []
  for ker in kernal_names:

    classifier = SVC(C=c, kernel=ker , max_iter=1e8)
    classifier.fit(x_train, y_train)
    y_pred_test = classifier.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred_test)
    accuracies.append(accuracy)

  curr_df = pd.DataFrame({'C': c, 'Linear': accuracies[0], 'Poly': accuracies[1], 'RBF': accuracies[2]}, index=[0])
  accuracy_table = pd.concat([accuracy_table, curr_df], ignore_index=True)
print(accuracy_table)

# make .md file
accuracy_table.to_markdown('accuracy_table.md')
