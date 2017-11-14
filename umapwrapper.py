#!/usr/bin/env python
import sys
import numpy
import umap
import argparse

# Parse command line
parser = argparse.ArgumentParser(description = 'Command line wrapper for umap')
parser.add_argument('-v', '--verbose', help='set verbosity', action='store_true')
parser.add_argument('--inputcsv', help='input file in csv format, rows are data points')
parser.add_argument('--output', help='output file that will contain the embedding')
parser.add_argument('--statsfile', default = None,  help='file to save run time statistics')

parser.add_argument('--n_neighbors', type=int, default=15, help='The size of the local neighborhood for manifold approximation')
parser.add_argument('--n_components', type=int, default=2, help='The dimension of the sapce to embed into.')
parser.add_argument('--metric', default='euclidean', help='The metric to use to compute distances in high dimensional space')
parser.add_argument('--gamma', default=1.0, type=float,help='Weighting applied to negative samples in low dimensional embedding optimization.')
parser.add_argument('--n_edge_samples', type=int, default=None, help='The number of edge/1-simplex samples to be used in optimizing the low dimensional embedding')
parser.add_argument('--alpha', default=1.0, type=float,help='Initial learning rate')
parser.add_argument('--min_dist', default=0.1, type=float,help='The effective minimum distance between embedded points')
parser.add_argument('--spread', default=1.0, type=float,help='The effective scale of embedded points')

# Currently not implemented in this script
#parser.add_argument('--init', default='spectral')
#parser.add_argument('--a', default=None)
#parser.add_argument('--b', default=None)
#parser.add_argument('--metric_kwds')

args = parser.parse_args()

# Debug
print(args)
#sys.exit();

inputfile = args.inputcsv
outputfile = args.output

# Load the input data, ignoreing header line
inputdata = numpy.loadtxt(inputfile, skiprows=1)

#Run umap
import time

t0 = time.time()


emb = umap.UMAP(alpha = args.alpha, gamma = args.gamma, metric = args.metric, min_dist = args.min_dist, n_components = args.n_components, n_neighbors = args.n_neighbors, spread = args.spread).fit_transform(inputdata)

t1 = time.time()

umap_runtime = t1 - t0

if args.statsfile is not None:
    with open(args.statsfile, 'w') as f:
        f.write('%d' % umap_runtime)

# Save the outputfile
numpy.savetxt(outputfile, emb, delimiter = ",")
