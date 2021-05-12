import csv
import math
import operator
from random import sample
import matplotlib.pyplot


def process_csv_file():
    points = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                point = Point(row[1], row[2], row[0])
                points.append(point)
                line_count += 1
    return points


def plot(clusters):
    for cluster in clusters:
        x = [point.val1 for point in cluster.points]
        y = [point.val2 for point in cluster.points]

        symbol = ''
        if cluster.label == 'A':
            symbol = 'ro'
        if cluster.label == 'B':
            symbol = 'bo'
        if cluster.label == 'C':
            symbol = 'go'
        if cluster.label == 'D':
            symbol = 'yo'

        matplotlib.pyplot.plot(x, y, symbol, label=cluster.label)

    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()


def print_statistical_measures(clusters, points):
    for cluster in clusters:
        accuracy_index, precision, rappel, score = cluster.get_statistical_measures(points)
        print("\n")
        print(cluster.label)
        print("Accuracy " + str(accuracy_index))  # the opposite of error
        print("Precision " + str(precision))  # the probability that a positive classified example is relevant
        print("Rappel " + str(rappel))  # the probability that a positive example is correct classified
        print("Score " + str(score))


class Point:
    def __init__(self, val_1, val_2, label):
        self.label = label
        self.val1 = float(val_1)
        self.val2 = float(val_2)
        self.cluster = None

    def __repr__(self):
        return self.label + ',' + str(self.val1) + ',' + str(self.val2)

    def closest_cluster(self, clusters):# computes the euclidean distance between the point and each cluster
        minimum = -1
        for cluster in clusters:
            if minimum == -1:
                minimum = cluster
                continue
            if math.dist((cluster.mean_val1, cluster.mean_val2), (self.val1, self.val2)) <= \
                    math.dist((minimum.mean_val1, minimum.mean_val2), (self.val1, self.val2)):
                minimum = cluster
        return minimum# will choose the closest one


class Cluster:
    def __init__(self, label):
        self.label = label
        self.points = []
        self.mean_val1 = 0
        self.mean_val2 = 0

    def add_point(self, point):
        self.points.append(point)# add point to the cluster to which it was assigned

        if point.cluster:
            point.cluster.points.remove(point)# remove the point from the previous cluster if it was previously assigned

        point.cluster = self# update the point membership to a cluster
        return self.update_means()# update means and compare them

    def update_means(self):
        old_val1 = self.mean_val1
        old_val2 = self.mean_val2

        sum_val1 = 0
        sum_val2 = 0
        for point in self.points:
            sum_val1 += point.val1
            sum_val2 += point.val2
        self.mean_val1 = sum_val1 / len(self.points)
        self.mean_val2 = sum_val2 / len(self.points)

        # if self.mean_val1 == old_val1 and self.mean_val2 == old_val2:
        #     return False

        # compare with the convergence rate
        if abs(self.mean_val1 - old_val1) <= 0.001 and abs(self.mean_val2 - old_val2) <= 0.001:
            return False
        return True

    def update_label(self):
        frequency = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        for point in self.points:
            frequency[point.label] += 1

        self.label = max(frequency.items(), key=operator.itemgetter(1))[0]

    def get_statistical_measures(self, points):
        TP = 0
        FP = 0
        TN = 0
        FN = 0

        for point in self.points:
            if point.label == self.label:
                TP += 1
            else:
                FP += 1

        for point in points:
            if point not in self.points:
                if point.label != self.label:
                    TN += 1
                else:
                    FN += 1

        accuracy_index = (TP + TN) / (TP + TN + FP + FN)  # no. of correct classified / total no. of examples
        precision = TP / (TP + FP)  # no. of correct positive classified/ total no. of examples classified as positive
        rappel = TP / (TP + FN)  # no. of correct positive classified / total no. of positive examples
        score = 2 / ((1 / rappel) + (1 / precision))  # combines the precision with the rappel

        return accuracy_index, precision, rappel, score


def main():
    clusters = []
    points = process_csv_file()

    # create the list of clusters, each cluster will have 0 points and mean_values=0
    clusters.append(Cluster('A'))
    clusters.append(Cluster('B'))
    clusters.append(Cluster('C'))
    clusters.append(Cluster('D'))

    random_points = sample(points, 4)# choose 4 random points
    for i in range(0, 4):# each cluster will have a random mean_val
        clusters[i].mean_val1 = random_points[i].val1
        clusters[i].mean_val2 = random_points[i].val2

    ok = True
    while ok:# will repeat until assigned categories won't change anymore
        ok = False
        for point in points:# for each point assign it to the closest cluster according to the current centroid
            optimal_cluster = point.closest_cluster(clusters)

            if optimal_cluster.add_point(point):# stops depending on the value of the new mean of the cluster
                ok = True

    for i in clusters:
        i.update_label()# update each label depending on the majority of points in the cluster

    print_statistical_measures(clusters, points)
    plot(clusters)


if __name__ == '__main__':
    main()
