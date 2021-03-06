import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline


def predict_numerical_from_text(train_df: pd.DataFrame, test_df: pd.DataFrame, text_col: str, target_col: str):
    """
    Predict a numerical value between 0 and 1 from text using Logistic Regression on TF-IDF features.
    Specifically, the _predictor will predict the probability of the target being below or above 0.5.
    Can be used for e.g. sentiment analysis.

    :param train_df: a Pandas dataframe containing the training set
    :param test_df: a Pandas dataframe containing the df set
    :param text_col: the column containing the text that will be used as features
    :param target_col: the column containing the numerical target

    :return: a tuple containing the test set predictions as well as the mean cross-validation score
    """
    train_df['class'] = train_df[target_col] >= 0.5

    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', LogisticRegression()),
    ])

    scores = cross_val_score(text_clf, train_df[text_col], train_df['class'], cv=3)
    mean_clf_score = scores.mean()

    text_clf.fit(train_df[text_col], train_df['class'])

    predicted = text_clf.predict_proba(test_df[text_col])

    return predicted, mean_clf_score


def predict_multiclass_from_text(train_df: pd.DataFrame, test_df: pd.DataFrame, text_col: str, target_col: str,
                                 metric='neg_log_loss'):
    """
        Multi-class classification from text using Logistic Regression on TF-IDF features.

        :param train_df: a Pandas dataframe containing the training set
        :param test_df: a Pandas dataframe containing the df set
        :param text_col: the column containing the text that will be used as features
        :param target_col: the column containing the numerical target
        :param metric: scoring metric for cross-validation

        :return: a tuple containing the test set predictions as well as the mean cross-validation score
        """
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', LogisticRegression()),
    ])

    scores = cross_val_score(text_clf, train_df[text_col], train_df[target_col], cv=3, scoring=metric)
    mean_clf_score = scores.mean()

    text_clf.fit(train_df[text_col], train_df[target_col])

    predicted = text_clf.predict_proba(test_df[text_col])

    return predicted, mean_clf_score
