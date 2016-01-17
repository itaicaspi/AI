from get_features import get_ads_features
from noise import get_noisy_folds
import numpy as np
from sklearn import tree
import random
from math import ceil, floor
from time import clock
import pickle


def get_ad_dataset():
     # Load ad dataset
    ad_dataset_file = 'ad-dataset/ad.data'
    ad_dataset = np.genfromtxt(ad_dataset_file, delimiter=',', dtype=str)
    ad_dataset[ad_dataset == 'ad.'] = 1
    ad_dataset[ad_dataset == 'nonad.'] = 0
    ads_features = get_ads_features(201239480, 302629605)
    ads_features += [np.shape(ad_dataset)[1]-1]
    ad_dataset = ad_dataset[:, ads_features].astype(int)
    ad_dataset = ad_dataset.tolist()

    return get_noisy_folds(ad_dataset)


def get_har_dataset():
    # Load HAR dataset
    har_dataset_file = 'UCI HAR Dataset/train/X_train.txt'
    har_labels_file = 'UCI HAR Dataset/train/y_train.txt'
    har_dataset = np.genfromtxt(har_dataset_file, dtype=float)
    har_labels = np.genfromtxt(har_labels_file, dtype=int)
    har_labels[har_labels <= 3] = 1     # replace moving labels
    har_labels[har_labels >= 4] = 0     # replace resting labels
    har_labels.shape = (-1, 1)
    har_dataset = np.concatenate((har_dataset, har_labels), axis=1)
    har_dataset = har_dataset.tolist()

    return get_noisy_folds(har_dataset)


def dump_data_sets_to_file():
    ad_noisy_folds, ad_folds = get_ad_dataset()
    har_noisy_folds, har_folds = get_har_dataset()
    pickle.dump(ad_folds, open("ad_folds.p", "wb"))
    pickle.dump(ad_noisy_folds, open("ad_noisy_folds.p", "wb"))
    pickle.dump(har_folds, open("har_folds.p", "wb"))
    pickle.dump(har_noisy_folds, open("har_noisy_folds.p", "wb"))


def load_data_sets():
    ad_folds = pickle.load(open("ad_folds.p", "rb"))
    ad_noisy_folds = pickle.load(open("ad_noisy_folds.p", "rb"))
    har_folds = pickle.load(open("har_folds.p", "rb"))
    har_noisy_folds = pickle.load(open("har_noisy_folds.p", "rb"))
    return ad_folds, ad_noisy_folds, har_folds, har_noisy_folds


def fit(examples, classifications, features_idx_list, features_classifier, min_samples_leaf = 4):
    ''' recursive function. builds a tree in the format [left_son, feature_idx, right_son],
        with the classification 0 or 1 in the leaves
    '''
    if len(examples) <= min_samples_leaf or len(features_idx_list) == 0:
        count = 0
        for c in classifications:
            count += c
        return round(float(count)/len(classifications))

    feature_idx = features_classifier(features_idx_list)
    features_idx_list.remove(feature_idx)
    left_examples = []
    right_examples = []
    left_classifications = []
    right_classifications = []
    i = 0 # index in the classifications list

    # split the example for the left and right sons
    for example in examples:
        if example[feature_idx]:
            left_examples.append(example)
            left_classifications.append(classifications[i])
        else:
            right_examples.append(example)
            right_classifications.append(classifications[i])
        i += 1

    count = 0
    for c in classifications:
        count += c
    if len(left_classifications) == 0:
        left_son = round(float(count)/len(classifications))
    else:
        left_son = fit(left_examples, left_classifications, features_idx_list, features_classifier)
    if len(right_classifications) == 0:
        right_son = round(float(count)/len(classifications))
    else:
        right_son = fit(right_examples, right_classifications, features_idx_list, features_classifier)

    return [left_son, feature_idx, right_son]


def classify_example(tree, example):
    if (tree == 1 or tree == 0):
        return tree
    if example[tree[1]]:
       return classify_example(tree[2], example)
    return classify_example(tree[0], example)


def predict(tree, examples):
    for example in examples:
       classify_example(tree, example)


def k_fold_cross_validation(folds, noisy_folds,criteria="entropy"):
    mean_accuracy = 0.0
    trees = []
    for test_fold_idx in range(len(folds)):
        # train for all folds except for test_fold_idx
        X = []
        Y = []
        for train_fold_idx in range(len(folds)):
            if train_fold_idx == test_fold_idx:
                continue
            X += [row[:-1] for row in noisy_folds[train_fold_idx]]
            Y += [row[-1] for row in noisy_folds[train_fold_idx]]
        clf = tree.DecisionTreeClassifier(criterion="entropy", min_samples_leaf=8)
        clf = clf.fit(X, Y)
        # test for test_fold_idx
        X = [row[:-1] for row in folds[test_fold_idx]]
        Y = [row[-1] for row in folds[test_fold_idx]]
        results = clf.predict(X).tolist()
        count = [1 for i in range(len(results)) if results[i] == Y[i]]
        mean_accuracy += len(count)/float(len(results))
        trees += [clf]
    mean_accuracy /= float(len(folds))
    return trees, mean_accuracy

class FeaturesClassifier:
    def __init__(self, criterion):
        self.criterion = criterion

    def classifier(self, features):
        if  self.criterion == 1:
            return random.choice(features)
        elif self.criterion == 2:
            return random.choice(features)

    def fit(self, examples, classifications, features_idx_list):
        if  self.criterion >= 1:
            return fit(examples, classifications, features_idx_list, self.classifier)
        else:
            clf = tree.DecisionTreeClassifier(criterion="entropy", min_samples_leaf=4)
            return clf.fit(examples, classifications)

    def predict(self, tree, examples):
        if  self.criterion >= 1:
            return predict(tree, examples)
        else:
            return tree.predict(examples).tolist()


def k_fold_cross_validation2(folds, noisy_folds,criteria, feature_set_size):
    mean_accuracy = 0.0
    trees = []
    classifier = FeaturesClassifier(criteria)
    for test_fold_idx in range(len(folds)):
        # train for all folds except for test_fold_idx
        X = []
        Y = []
        for train_fold_idx in range(len(folds)):
            if train_fold_idx == test_fold_idx:
                continue
            X += [row[:-1] for row in noisy_folds[train_fold_idx]]
            Y += [row[-1] for row in noisy_folds[train_fold_idx]]
        tree = classifier.fit(X, Y, list(range(feature_set_size)))
        # test for test_fold_idx
        X = [row[:-1] for row in folds[test_fold_idx]]
        Y = [row[-1] for row in folds[test_fold_idx]]
        results = classifier.predict(tree, X)
        count = [1 for i in range(len(results)) if results[i] == Y[i]]
        mean_accuracy += len(count)/float(len(results))
        trees += [tree]
    mean_accuracy /= float(len(folds))
    return trees, mean_accuracy


def select_random_features_subset(folds, noisy_folds, q):
    # folds are assumed to have the label as the last feature, noisy folds assumed NOT to have them
    # select random features
    feature_set_size = len(noisy_folds[0][0])
    reduced_features_set_size = ceil(q*feature_set_size)
    features_range = list(range(feature_set_size-1))
    selected_features = random.sample(features_range, reduced_features_set_size)
    selected_features += [feature_set_size-1]
    reduced_features_noisy_folds = [[[row[f]for f in selected_features] for row in fold] for fold in noisy_folds]
    reduced_features_folds = [[[row[f]for f in selected_features] for row in fold] for fold in folds]
    return reduced_features_noisy_folds, reduced_features_folds, reduced_features_set_size


def learn_ensemble(folds, noisy_folds, ensemble_size, ensemble_type=1):
    p = 0.5            # train set size factor
    q = 0.5            # feature set size factor

    # learn 10 ensemble trees
    trees = []
    reduced_features_noisy_folds = []
    reduced_features_folds = []
    num_folds = len(folds)
    feature_set_size = len(noisy_folds[0][0])
    for s in range(ensemble_size):
        reduced_features_noisy_fold, reduced_features_fold, features_subset_size = select_random_features_subset(folds, noisy_folds, q)
        reduced_features_folds.append(reduced_features_fold)
        reduced_features_noisy_folds.append(reduced_features_noisy_fold)
        fold_trees, _ = k_fold_cross_validation2(reduced_features_fold, reduced_features_noisy_fold, ensemble_type % 3, features_subset_size)
        trees.append(fold_trees)

    # evaluate the accuracy of each ensemble for each fold and average the results
    mean_accuracy = 0
    for test_fold_idx in range(num_folds):
        # test for test_fold_idx
        results = []
        # labels should be the same for all trees (since we are taking the same examples)
        Y = [row[-1] for row in folds[test_fold_idx]]
        for s in range(ensemble_size):
            X = [row[:-1] for row in reduced_features_folds[s][test_fold_idx]]
            labels = (trees[s][test_fold_idx]).predict(X)
            # sum up the labels predicted by all trees to a single vector
            if results == []:
                results = labels
            else:
                results = [x + y for x, y in zip(results, labels)]
        # take the average label (by dividing the sum by the ensemble size) and then round up to 1 or down to 0
        results = [round(label/ensemble_size) for label in results]
        # count number of matches between predicted label and true label
        count = [1 for i in range(len(results)) if results[i] == Y[i]]
        # sum up the prediction accuracy for the ensemble for each fold
        mean_accuracy += (len(count)/float(len(results)))
    # take the mean accuracy
    mean_accuracy /= float(num_folds)

    return mean_accuracy

if __name__ == '__main__':
    dumpToFile = False
    if dumpToFile:
        dump_data_sets_to_file()
    else:
        ad_folds, ad_noisy_folds, har_folds, har_noisy_folds = load_data_sets()

        sizes = [5, 11, 15, 21, 25, 31, 35, 41, 45, 51]

        for ensemble_size in sizes:
            start = clock()
            mean_accuracy = learn_ensemble(ad_folds, ad_noisy_folds, ensemble_size)
            print("The mean accuracy for ad dataset ensemble of size " + str(ensemble_size) + " = " + str(mean_accuracy))
            total_time = clock() - start
            print("Time for training and evaluating = " + str(floor(total_time / 60)) + ":" + str(floor(total_time % 60)))
'''

            start = clock()
            mean_accuracy = learn_ensemble(har_folds, har_noisy_folds, ensemble_size)
            print("The mean accuracy for har dataset ensemble of size " + str(ensemble_size) + " = " + str(mean_accuracy))
            total_time = clock() - start
            print("Time for training and evaluating = " + str(floor(total_time / 60)) + ":" + str(floor(total_time % 60)))
'''
