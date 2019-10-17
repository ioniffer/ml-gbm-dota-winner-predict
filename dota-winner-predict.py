import pandas
import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

data = pandas.read_csv('features.csv', index_col='match_id')
X = data.loc[:, 'start_time':'dire_first_ward_time']
y = data['radiant_win']

nan_count = X.isnull().sum()
nan_count = nan_count[nan_count != 0]
print('Признаки с пропусками (NaN) |  Количество пропусков')
print(nan_count)
print('Заменим все пропущенные значения на нули')
X.fillna(inplace=True, value=0)

print('Столбец с целевой переменной - radiant_win')

# todo: количество деревьев 10, 20, 30

# n_estimators = 10,20,30 - количество деревьев
gbm = GradientBoostingClassifier(n_estimators=10, verbose=True,
                                 random_state=241)
splits = 5
kf = KFold(n_splits=splits, random_state=1, shuffle=True)


gbm_score = 0
for train, test in kf.split(X):
    X_train, X_test = X.iloc[train], X.iloc[test]
    y_train, y_test = y.iloc[train], y.iloc[test]
    gbm.fit(X_train, y_train)
    pred = gbm.predict_proba(X_test)[:, 1]
    gbm_score += roc_auc_score(y_test, pred)
    print(gbm_score)
print(gbm_score/splits)

'''
data_test = pandas.read_csv('features_test.csv', index_col='match_id')
X_test = data_test.loc[:, 'start_time':'dire_first_ward_time']
X_test.fillna(inplace=True, value=0)
'''


# print(X_test)

# pred = clf.predict_proba(X_test)[:, 1] - оценка принадлежности к 1 классу
# реализоавать AUC-ROC


#corr = np.corrcoef(features, rowvar=False)
#corr = corr.reshape((108, 108))  # 108 108
#print(np.shape(corr))
#np.savetxt('corr.csv', corr, fmt='%1.2f', delimiter=';')
