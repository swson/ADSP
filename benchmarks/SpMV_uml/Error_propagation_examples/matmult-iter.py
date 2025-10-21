#! /usr/bin/python
from argparse import ArgumentParser
from datetime import datetime
from os import mkdir, urandom
import random

import numpy as np
from PIL import Image


def dump_matrix(mtx, f):
	make_data = lambda arg: " ".join([f'{x}' for x in arg])

	import scipy
	csr_mtx = scipy.sparse.csr_matrix(mtx)
	print(make_data(csr_mtx.shape), file=f)
	print(make_data(csr_mtx.data), file=f)
	print(make_data(csr_mtx.indices), file=f)
	print(make_data(csr_mtx.indptr), file=f)

def main(args):
	if args.matrix_shape**2 <= args.sparsity:
		# sanity check
		raise ValueError('matrix sparsity is greater than number of elements')

	if args.random_seed is not None:
		seed = int(args.random_seed)
	else:
		seed = int.from_bytes(urandom(4), byteorder='little')

	random.seed(seed)

	dirname = f'{args.base_dir}/{datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}'
	mkdir(dirname)

	mtx = np.zeros((args.matrix_shape, args.matrix_shape, 2))
	pts_corrupt = np.empty(args.iterations)
	if args.save_history:
		diffs = np.empty((args.matrix_shape, args.matrix_shape, args.iterations))

	# create the random matrices
	total_pts = 0
	while total_pts < args.sparsity:
		x = random.randrange(0, args.matrix_shape)
		y = random.randrange(0, args.matrix_shape)
		if mtx[x,y,0] != 1:
			mtx[x,y,0] = 1
			mtx[x,y,1] = 1
			total_pts += 1
	
	# corrupt one of them
	total_pts = 0
	while total_pts < args.bad_elements:
		x = random.randrange(0, args.matrix_shape)
		y = random.randrange(0, args.matrix_shape)
		if (args.corrupt_nonzero_only and mtx[x,y,1] == 1) \
				or (not args.corrupt_nonzero_only and mtx[x,y,1] != 2):
	#	if args.corrupt_nonzero_only:
	#		if mtx[x,y,1] == 1:
	#			mtx[x,y,1] = 2
	#			total_pts += 1
	#	else:
	#		if mtx[x,y,1] != 2:
			mtx[x,y,1] = 2
			total_pts += 1

	with open(f'{dirname}/seed', 'w') as f:
		print(f'{seed}',file=f)

	for cnt, file in enumerate(
				[f'{dirname}/mtx_{matname}' \
					for matname in ['orig', 'modif']] \
			):
		with open(file, 'w') as f:
			dump_matrix(mtx[:,:,cnt], f)

	# now do the operation on the matrices
	orig = mtx.copy()
	for i in range(args.iterations):
		diff = abs(mtx[:,:,0] - mtx[:,:,1])
		mtx[:,:,0] = mtx[:,:,0].dot(orig[:,:,0])
		mtx[:,:,1] = mtx[:,:,1].dot(orig[:,:,1])
		mask = np.where(diff > 1)
		pts_corrupt[i] = len(mask[0])
		if args.save_intermediate \
				and len(mask[0]) > 0:
			savedata = diff.copy()
			savedata[mask] = 1
			img = Image.fromarray(np.uint8(savedata), '1')
			img.save(f'{dirname}/diffs-{i:05d}.png') 
		if args.save_history: diffs[:,:,i] = diff.copy()

	with open(f'{dirname}/pts_corrupt', 'w') as f:
		for count, value in enumerate(pts_corrupt):
			print(f'{count} {value}', file=f)
	

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('--matrix-shape', type=int, default=400)
	parser.add_argument('--base-dir', type=str, default='.')
	parser.add_argument('--iterations', type=int, default=100)
	parser.add_argument('--sparsity', type=int, default=400)
	parser.add_argument('--random-seed', type=int, default=None)
	parser.add_argument('--bad-elements', type=int, default=1)
	parser.add_argument('--save-history', default=False, action='store_true')
	parser.add_argument('--save-intermediate', default=False, action='store_true')
	parser.add_argument('--corrupt-nonzero-only', default=False, action='store_true')

	main(parser.parse_args())
