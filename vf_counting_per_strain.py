'''
import pandas as pd
from collections import defaultdict

def process_file(filename):
    current_vf_class = None
    current_vf = None
    current_genes = None
    
    result = defaultdict(defaultdict(list))
    gene_list = []
    with open(filename, 'r') as f:
        for line in f:
            # 如果是空行，直接忽略
            if line.strip() == '':
                continue
            
            columns = line.split('\t')

            # 如果第一列不为空，更新VF class，VF和genes
            if columns[0].strip() != '':
                current_vf_class = columns[0].strip()
                current_vf = columns[1].strip()
                current_genes = columns[2].strip()
            else:
                # 如果第二列不为空，更新VF和genes
                if columns[1].strip() != '':
                    current_vf = columns[1].strip()
                    current_genes = columns[2].strip()
                else:
                    # 否则，只更新genes
                    current_genes = columns[2].strip()
            
            # 获取基因列表
            genes = columns[3]
            if "_" in genes:
                for gene in genes.split(';'):
                    strain = '_'.join(gene.split('_')[:2])
                    if strain not in gene_list:
                        gene_list.append(strain)
            
                    # 添加到结果中
                    if result[current_vf_class][current_vf].get(current_genes):
                        result[current_vf_class][current_vf][current_genes].append(strain)
                    else:
                        result[current_vf_class][current_vf][current_genes] = []
                        result[current_vf_class][current_vf][current_genes].append(strain)

            for gene in genes:
                strain = '_'.join(gene.split('_')[:2])
                result.append({
                    'VF class': current_vf_class,
                    'VF': current_vf,
                    'genes': current_genes,
                    'gene': strain
                })

    return result

df = process_file('VFanalyzer.output.txt')

f2 = open('VFanalyzer.output.counts.txt', 'w')  # Header

for strain in gene_list:
    for current_vf_class in result:
        for current_vf in result[current_vf_class]:
            for current_genes in result[current_vf_class][current_vf]:
                strain_num = result[current_vf_class][current_vf][current_genes].count(strain)
                print(current_vf_class+'\t'+current_vf+'\t'+current_genes+'\t'+str(strain_num)+'\n')


#df_counts = df.groupby(['VF class', 'VF', 'genes', 'gene']).size().reset_index(name='counts')
#df_counts.to_csv('VFanalyzer.output_per_strain.txt', index=False, sep='\t')
'''

import pandas as pd
from collections import defaultdict

def process_file(filename):
    current_vf_class = None
    current_vf = None
    current_genes = None

    result = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    gene_list = []

    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            columns = line.split('\t')
            if columns[0].strip() != '':
                current_vf_class = columns[0].strip()
                current_vf = columns[1].strip()
                current_genes = columns[2].strip()
            else:
                if columns[1].strip() != '':
                    current_vf = columns[1].strip()
                    current_genes = columns[2].strip()
                else:
                    current_genes = columns[2].strip()

            genes = columns[3]
            if "_" in genes:
                for gene in genes.split(';'):
                    strain = '_'.join(gene.split('_')[:2]).strip()
                    if strain not in gene_list:
                        gene_list.append(strain)

                    result[current_vf_class][current_vf][current_genes].append(strain)

    return result, gene_list

result, gene_list = process_file('VFanalyzer.output.txt')

with open('VFanalyzer.output.counts.per-strain.txt', 'w') as f:
    f.write('\t'*2)
    for strain in gene_list:
        f.write('\t'+strain)
    f.write('\n')
    for current_vf_class in result:
        f.write(current_vf_class)
        for current_vf in result[current_vf_class]:
            f.write('\t'+current_vf)
            for current_genes in result[current_vf_class][current_vf]:
                f.write('\t'+current_genes)
                for strain in gene_list:
                    strain_num = result[current_vf_class][current_vf][current_genes].count(strain)
                    f.write(f"\t{strain_num}")
                f.write('\n')
