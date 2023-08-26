
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: zhongjie wang
# "Determine the threshold for the number of genomes to decide when a gene is considered a core gene."
# input genome completeness must be decimal, seperated by tab(\t).


from random import sample
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor
import argparse

def calculate_presence(a, b):
    """Generate presence list; a is original list; b is absence list."""
    clist = [i for i in a if i not in b]
    return clist

def calculate_product(alist):
    """Generate the product of a list."""
    p = 1
    for a in alist:
        p *= a
    return p

def calculate_absence_probability(absence_list):
    """Calculate the combined absence probability."""
    return calculate_product([1 - val for val in absence_list])

def main(input_file, output_file):
    with open(input_file, 'r') as f1, open(output_file, 'w') as f3:
        completeness_values = [
            round(float(line.split('\t')[5]) / 100, 4) for line in f1.read().split('\n')[1:]
        ]
        
        result = [calculate_product(completeness_values)]
        f3.write(f"0 genome absent:{result[0]}\n")

        def calculate_for_i_absent(i):
            total = sum(
                calculate_product(calculate_presence(completeness_values, list(absent_values)))
                * calculate_absence_probability(absent_values)
                for absent_values in combinations(completeness_values, i)
            )
            return total

        # Using multi-threading to speed up the calculation for each absence level
        with ThreadPoolExecutor() as executor:
            results_for_absence = list(executor.map(calculate_for_i_absent, range(1, len(completeness_values) + 1)))

        for i, res in enumerate(results_for_absence, 1):
            result.append(res)
            f2.write(f"{i} genomes absent:{res}\n")

        f2.write('\n')

        dsum = 0
        for n, d in enumerate(result):
            dsum += d
            f2.write(f"when {n} genomes' absent: containing gene percentage:{dsum:.4f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the threshold for the number of genomes to decide when a gene is considered a core gene.")
    parser.add_argument("--input", "-i", required=True, help="Input completeness file by CheckM. Must be decimals seperated by Tab")
    parser.add_argument("--output", "-o", required=True, help="Output file.")
    
    args = parser.parse_args()
    main(args.input, args.output)
