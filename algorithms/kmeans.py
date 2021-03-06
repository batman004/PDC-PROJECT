import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets._samples_generator import make_blobs

def kmeans():
        np.random.seed(0)
        batch_size = 45
        centers = [[1, 1], [-1, 1], [1, -1]]
        n_clusters = len(centers)
        X, labels_true = make_blobs(n_samples=100000, centers=centers, cluster_std=0.7)


        # Compute clustering with Means
        k_means = KMeans(init='k-means++', n_clusters=3, n_init=10, verbose=1)
        t0 = time.time()
        k_means.fit(X)
        t_batch = time.time() - t0


        # Compute clustering with ParallelKMeans
        mbk = MiniBatchKMeans(init='k-means++', n_clusters=3, batch_size=batch_size,
                        n_init=10, max_no_improvement=10, verbose=1)
        t0 = time.time()
        mbk.fit(X)
        t_mini_batch = time.time() - t0


        # Plot result
        fig = plt.figure(figsize=(8, 3))
        fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
        colors = ['red', 'green', 'blue']

        cdict = {"High" : "red", "Medium" : "blue", "Low":"green"}

        # We want to have the same colors for the same clusters in parallelised and non-parallel k-means
        k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)
        mbk_means_cluster_centers = np.sort(mbk.cluster_centers_, axis=0)
        k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
        mbk_means_labels = pairwise_distances_argmin(X, mbk_means_cluster_centers)
        order = pairwise_distances_argmin(k_means_cluster_centers,
                                        mbk_means_cluster_centers)

        # KMeans
        ax = fig.add_subplot(1, 3, 1)
        for k, col in zip(range(n_clusters), colors):
                my_members = k_means_labels == k
                cluster_center = k_means_cluster_centers[k]
                ax.plot(X[my_members, 0], X[my_members, 1], 'w',
                        markerfacecolor=col, marker='.')
                ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                        markeredgecolor='k', markersize=6)

        ax.set_title('KMeans')
        ax.set_xticks(())
        ax.set_yticks(())
        plt.text(2, 2.9, 'Legend\nHigh -> red\nMedium -> Green\nLow -> Blue')
        plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
        t_batch, k_means.inertia_))

        # ParallelKMeans
        ax = fig.add_subplot(1, 3, 2)
        for k, col in zip(range(n_clusters), colors):
                my_members = mbk_means_labels == order[k]
                cluster_center = mbk_means_cluster_centers[order[k]]
                ax.plot(X[my_members, 0], X[my_members, 1], 'w',
                        markerfacecolor=col, marker='.')
                ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                        markeredgecolor='k', markersize=6)
        ax.set_title('Parallelized KMeans')
        ax.set_xticks(())
        ax.set_yticks(())
        plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f' %
                (t_mini_batch, mbk.inertia_))
                
        # Initialise the different array to all False
        different = (mbk_means_labels == 4)
        ax = fig.add_subplot(1, 3, 3)
        for k in range(n_clusters):
                different += ((k_means_labels == k) != (mbk_means_labels == order[k]))
                identic = np.logical_not(different)
                ax.plot(X[identic, 0], X[identic, 1], 'w',
                        markerfacecolor='#bbbbbb', marker='.')
                ax.plot(X[different, 0], X[different, 1], 'w',
                        markerfacecolor='m', marker='.')
        ax.set_title('Difference')
        ax.set_xticks(())
        ax.set_yticks(())
        plt.suptitle("Showing the Execution time for KMeans and Parallel KMeans")
        plt.show()

