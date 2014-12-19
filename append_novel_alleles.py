from Bio import SeqIO
import argparse
import fileinput
import json
import os, sys

def arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--alleles', required = True, help = "Path to allele directory")
	parser.add_argument('-j', '--jsons', required = True, help = "Path to JSON directory")
	parser.add_argument('-t', '--test', required = True, help = "MIST test name")

	return parser.parse_args()

def load_data(jsonpath):
	"""Converts JSON file into Python dict
	"""
	with open(jsonpath, 'r') as f:
		data = json.load(f)
	return data

def basename(filename):
	"""Strips the path and file extension(s) from a filename.

		Python's standard basename() retains the extension.
	"""
	try:
		start = filename.rindex('/') + 1
	except ValueError:
		start = 0

	try:
		end = filename.index('.')
	except ValueError:
		end = None

	return filename[start:end]

def init_sets(fastapath):
	"""Gets the known alleles and stores them in a set.

	"""
	st = set()
	with open (fastapath, 'r') as f:

		for rec in SeqIO.parse(f, 'fasta'):
			sq = str(rec.seq)
			st.add(sq)

	return st

def get_known_alleles(allele_dir):
	"""Stores known alleles as a dict full of sets.
	"""
	known_alleles = {}

	alleles = [f for f in os.listdir(allele_dir) if '.fasta' in f]

	for allele in alleles:
		
		name = basename(allele)
		path = os.path.join(allele_dir, allele)

		known = init_sets(path)
		known_alleles[name] = known

	return known_alleles

def novel_alleles(json, test):
	"""Generator function that iterates over the JSONs and yields potential novel alleles. 
	"""
	data = load_data(json)
	i=0
	while True:
		try:
			genes = data["Results"][i]["TestResults"][test]

			for gene in genes:
				trunc = genes[gene]["IsContigTruncation"]

				if genes[gene]["BlastResults"] != None:
					
					match = genes[gene]["CorrectMarkerMatch"]
					subjaln = genes[gene]["BlastResults"]["SubjAln"]
					if not (trunc or match) and len(subjaln) > 0:
						yield gene, subjaln

				else:
					if genes[gene]["ForwardPrimerBlastResult"] != None:
						if genes[gene]["ReversePrimerBlastResult"] != None:
							if (not trunc) and len(genes[gene]["Amplicon"]) > 0:
								yield gene, genes[gene]["Amplicon"]

			i += 1

		except IndexError:
			break
			
def get_novel_alleles(jsonpath, known_alleles, test):
	"""Loops over JSONs, finds novel alleles, and tracks them in a dictionary.

	"""
	jsons = [os.path.join(jsonpath, json) for json in os.listdir(jsonpath) if '.json' in json]
	novel = {}

	for json in jsons:
		for gene, potential in novel_alleles(json, test):

			if potential not in known_alleles[gene]:
				try:
					novel[gene].append(potential)
				except KeyError:
					novel[gene] = [potential]

				known_alleles[gene].add(potential)

	return novel

def write_novel_alleles(alleles, novel):
	"""Appends new alleles to multifasta file.
	"""
	for gene in novel:

		filename = os.path.join(alleles, gene + '.fasta')

		with open(filename, 'a') as f:
			for allele in novel[gene]:
				f.write('>placeholder\n')
				f.write(allele + "\n")

		fix_headers(filename)
		
def fix_headers(filename):
	"""Fixes the headers to be the basename and a incrementing allele number.
	e.g. >1

	"""

	counter = 1

	for line in fileinput.input(filename, inplace = True):
		if '>' in line:
			line = line.replace(line, '>'+str(counter)+'\n')
			counter += 1
		sys.stdout.write(line)

def process(args):
	
	known_alleles = get_known_alleles(args.alleles)
	
	novel = get_novel_alleles(args.jsons, known_alleles, args.test)

	write_novel_alleles(args.alleles, novel)

def main():

	args = arguments()
	process(args)

if __name__ == '__main__':
	main()