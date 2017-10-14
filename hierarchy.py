from jellyfish import jaro_distance
import numpy as np
import scipy.cluster.hierarchy
import matplotlib.pyplot as plt


def d(coord, words):
	i, j = coord
	return 1 - jaro_distance(words[i], words[j])


def calculate_relations(data, show_plot=False):
	ids = data['ids']
	addresses = data['addresses']
	addresses =  [i.decode('UTF-8') for i in addresses]

	coords = np.triu_indices(len(addresses), 1)
	array = np.apply_along_axis(d, 0, coords, addresses)
	linkage = scipy.cluster.hierarchy.linkage(array)
	# print linkage

	flat = scipy.cluster.hierarchy.fcluster(linkage, 0.15, criterion='distance')
	#print flat

	dendro = scipy.cluster.hierarchy.dendrogram(linkage)
	# print dendro
	if(show_plot):
		plt.title('Hierarchical Clustering Dendrogram (truncated)')
		plt.xlabel('sample index or (cluster size)')
		plt.ylabel('distance')
		scipy.cluster.hierarchy.dendrogram(
		    linkage,
		    truncate_mode='lastp',  # show only the last p merged clusters
		    p=12,  # show only the last p merged clusters
		    leaf_rotation=90.,
		    leaf_font_size=12.,
		    show_contracted=True,  # to get a distribution impression in truncated branches
		)
		plt.show()

	return linkage, flat