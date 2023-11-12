#! /usr/bin/env python

from collections import defaultdict
import sys

f1 = open('../ko00001.keg', 'r')
f2 = open('user_ko_staph348.txt', 'r')
f3 = open('staph348_ko_matrix.txt','w')
f4 = open('staph348_kegg_c_matrix.txt','w')
f5 = open('staph348_kegg_b_matrix.txt','w')


# make a dict of KEGG funtional categories with each K number
def nesteddict(): 
  return defaultdict(nesteddict)

kegg_category_dict=nesteddict()
ko_categories = f1.read()
for A_level_category in ko_categories.split('A09')[1:]:
    A_level_category_name = 'A09'+A_level_category.split('\n')[0]
    #print(A_level_category_name)
    for B_level_category in A_level_category.split('B  ')[1:]:
        B_level_category_name = B_level_category.split('\n')[0]
        #print(B_level_category_name)
        for C_level_category in B_level_category.split('C    ')[1:]:
            C_level_category_name = C_level_category.split('\n')[0]
            #print(C_level_category_name)
            D_level_category = '\t'.join(C_level_category.split('\n')[1:])
            #for D_level_category in C_level_category.split('D      ')[1:]:
            #print(D_level_category)
            if D_level_category != '':
                #print(C_level_category_name)
                kegg_category_dict[A_level_category_name][B_level_category_name][C_level_category_name] = D_level_category


lines = f2.readlines()
genome_dict = defaultdict(list)
genome_keggC_dict = defaultdict(list)
genome_keggB_dict = defaultdict(list)
kolist, keggC_list, keggB_list = [], [], []
for line in lines:
	if len(line.strip().split('\t')) > 1:
		#print(line.strip().split('\t'))
		gene, ko = line.split('\t')[:]
		ko = ko.strip()
		#print(ko)
		genome='_'.join(gene.split('_')[0:2])
		if ko not in kolist:
			kolist.append(ko)
		# KEGG D level dictionary
		if genome_dict.get(genome):
			genome_dict[genome].append(ko)
		else:
			genome_dict[genome] = []
			genome_dict[genome].append(ko)
		
		# KEGG C level dictionary
		for A in list(kegg_category_dict.keys()):
			for B in kegg_category_dict[A]:
				for C in kegg_category_dict[A][B]:
					if ko in kegg_category_dict[A][B][C]:
						#c level dict
						if C not in keggC_list:
							keggC_list.append(C)
						if genome_keggC_dict.get(genome):
							genome_keggC_dict[genome].append(C)
						else:
							genome_keggC_dict[genome] = []
							genome_keggC_dict[genome].append(C)
						#b level dict
						if B not in keggB_list:
							keggB_list.append(B)
						if genome_keggB_dict.get(genome):
							genome_keggB_dict[genome].append(B)
						else:
							genome_keggB_dict[genome] = []
							genome_keggB_dict[genome].append(B)
	else:
		genome='_'.join(line.split('_')[0:2])
		#print(genome)
		if "unassigned" not in kolist:
			kolist.append("unassigned")
		if genome_dict.get(genome):
			genome_dict[genome].append("unassigned")
		else:
			genome_dict[genome] = []
			genome_dict[genome].append("unassigned")

		#c level dict
		if "unassigned" not in keggC_list:
			keggC_list.append("unassigned")
		if genome_keggC_dict.get(genome):
			genome_keggC_dict[genome].append("unassigned")
		else:
			genome_keggC_dict[genome] = []
			genome_keggC_dict[genome].append("unassigned")
		
		#b level dict
		if "unassigned" not in keggB_list:
			keggB_list.append("unassigned")
		if genome_keggB_dict.get(genome):
			genome_keggB_dict[genome].append("unassigned")
		else:
			genome_keggB_dict[genome] = []
			genome_keggB_dict[genome].append("unassigned")


for genome in genome_dict:
	#print(genome)
	f3.write('\t'+genome)
	f4.write('\t'+genome)
	f5.write('\t'+genome)
f3.write('\n')
f4.write('\n')
f5.write('\n')

#count and write D level functions
for ko in kolist:
	f3.write(ko.strip())
	for genome in genome_dict:
		#print(genome)
		ko_number = genome_dict[genome].count(ko)
		f3.write('\t'+str(ko_number))
	f3.write('\n')

#count and write C level functions
for C in keggC_list:
	print(C)
	f4.write(C.strip())
	for genome in genome_dict:
		#print(genome)
		keggC_number = genome_keggC_dict[genome].count(C)
		f4.write('\t'+str(keggC_number))
	f4.write('\n')

#count and write B level functions
for B in keggB_list:
	print(B)
	f5.write(B.strip())
	for genome in genome_dict:
		#print(genome)
		keggB_number = genome_keggB_dict[genome].count(B)
		f5.write('\t'+str(keggB_number))
	f5.write('\n')


f1.close()
f2.close()
f3.close()
f4.close()
f5.close()

