from get_features import get_ads_features
from noise import get_noisy_folds
import numpy as np
from sklearn import tree
import random
from math import ceil, floor
from time import clock

def get_ad_dataset():
     # Load ad dataset
    ad_dataset_file = 'ad-dataset/ad.data'
    ad_dataset = np.genfromtxt(ad_dataset_file, delimiter=',', dtype=str)
    ad_dataset[ad_dataset == 'ad.'] = 1
    ad_dataset[ad_dataset == 'nonad.'] = 0
    ads_features = get_ads_features(201239480, 302629605)
    ad_dataset = ad_dataset[:, ads_features].astype(int)

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

    return get_noisy_folds(har_dataset)


def k_fold_cross_validation(folds, noisy_folds, train_on_noisy_data):
    mean_accuracy = 0
    trees = []
    for test_fold_idx in range(len(folds)):
        # train for all folds except for test_fold_idx
        X = []
        Y = []
        for train_fold_idx in range(len(folds)):
            if train_fold_idx == test_fold_idx:
                continue
            if train_on_noisy_data:
                X += [row[:-1] for row in noisy_folds[train_fold_idx]]
            else:
                X += [row[:-2] for row in folds[train_fold_idx]]
            Y += [row[-1] for row in folds[train_fold_idx]]
        clf = tree.DecisionTreeClassifier(criterion="entropy", min_samples_leaf=4)
        clf = clf.fit(X, Y)
        # test for test_fold_idx
        X = [row[:-2] for row in folds[test_fold_idx]]
        Y = [row[-1] for row in folds[test_fold_idx]]
        results = clf.predict(X)
        count = [1 for i in range(len(results)) if results[i] == Y[i]]
        mean_accuracy += (len(count)/len(results))
        trees += [clf]
    mean_accuracy /= len(folds)

    return trees, mean_accuracy


def select_random_features_subset(folds, noisy_folds, q):
    # folds are assumed to have the label as the last feature, noisy folds assumed NOT to have them
    # select random features
    feature_set_size = len(noisy_folds[0][0])
    features_range = list(range(feature_set_size))
    selected_features = random.sample(features_range, ceil(q*feature_set_size))
    reduced_features_noisy_folds = [[row[selected_features] for row in fold] for fold in noisy_folds]
    selected_features += [feature_set_size]
    reduced_features_folds = [[row[selected_features] for row in fold] for fold in folds]

    return reduced_features_noisy_folds, reduced_features_folds


def learn_ensemble(folds, noisy_folds, ensemble_size, ensemble_type=""):
    p = 0.67            # train set size factor
    q = 0.67            # feature set size factor

    # learn 10 ensemble trees
    trees = []
    reduced_features_noisy_folds = []
    reduced_features_folds = []
    num_features = ceil(q*len(noisy_folds[0][0]))
    num_folds = len(folds)
    for s in range(ensemble_size):
        reduced_features_noisy_fold, reduced_features_fold = select_random_features_subset(folds, noisy_folds, q)
        reduced_features_folds.append(reduced_features_fold)
        reduced_features_noisy_folds.append(reduced_features_noisy_fold)
        fold_trees, mean_accuracy = k_fold_cross_validation(reduced_features_fold, reduced_features_noisy_fold, True)
        trees.append(fold_trees)

    # evaluate the accuracy of each ensemble for each fold and average the results
    mean_accuracy = 0
    for test_fold_idx in range(num_folds):
        # test for test_fold_idx
        results = []
        # labels should be the same for all trees (since we are taking the same examples)
        Y = [row[-1] for row in reduced_features_folds[0][test_fold_idx]]
        for s in range(ensemble_size):
            X = [row[:-2] for row in reduced_features_folds[s][test_fold_idx]]
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
        mean_accuracy += (len(count)/len(results))
    # take the mean accuracy
    mean_accuracy /= num_folds

    return mean_accuracy

if __name__ == '__main__':

    ad_noisy_folds, ad_folds = get_ad_dataset()
    start = clock()
    ensemble_size = 11
    mean_accuracy = learn_ensemble(ad_folds, ad_noisy_folds, ensemble_size)
    print("The mean accuracy for ad dataset ensemble of size 1 = " + str(mean_accuracy))
    total_time = clock() - start
    print("Time for training and evaluating = " + str(floor(total_time / 60)) + ":" + str(floor(total_time % 60)))

    har_noisy_folds, har_folds = get_har_dataset()
    start = clock()
    ensemble_size = 11
    mean_accuracy = learn_ensemble(har_folds, har_noisy_folds, ensemble_size)
    print("The mean accuracy for har dataset ensemble of size 1 = " + str(mean_accuracy))
    total_time = clock() - start
    print("Time for training and evaluating = " + str(floor(total_time / 60)) + ":" + str(floor(total_time % 60)))