import numpy as np
from   scipy import stats
from   sklearn import datasets
from   sklearn.naive_bayes import GaussianNB
from   sklearn.cross_validation import train_test_split


def main():
    boston = datasets.load_boston()
    y = boston.target     # House prices
    mean = np.mean(y)
    y = y > mean            # y now means is_above_average_house_price

    fns = boston.feature_names
    predictors = np.array([
        'CHAS',     # Is district close to river
        'NOX',      # Air concentration of nitrous-oxide
        'CRIM',     # Crime rate per capita
        ])
    X_idx = np.in1d(fns, predictors)
    X = boston.data[:, X_idx]

    X_train, X_test, y_train, y_test = train_test_split(
        y, X, test_size=0.25, random_state=33)

    for p, x in zip(predictors, np.rollaxis(X, 1)):
        print('%s vs House price - srcc: %f, p_value: %f' % (
            (p, ) + stats.spearmanr(x, y)))


if __name__ == '__main__':
    main()
