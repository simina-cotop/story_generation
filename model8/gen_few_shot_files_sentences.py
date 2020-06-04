# Generate input files for the chartsopt2 domain, from the training data, i.e. chart descriptions given by humans
# including descriptions of the bars as sentences

from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import os
import glob
import csv
import re
from pprint import pprint

# Each line in the file will look like this:
# global description + local description, where the local one will be 23 different ones

# TODO:
# 1. Parse the info files to get the global information and create a dictionary which has as key each bar basic info 
# 2. Parse the description files to get the sentences corresponding to each bar and add those to the dictionary
# 3. From the dictionary generate the files according to the correct structure

def parse_info_files_per_chart(chart_file: str) -> Dict[int, List[Tuple[str,str]]]:
    # chart_descriptions[0] = [(law firms, <x_axis_label_highest_value>),(highest, <y_axis_highest_value>),...]
    chart_descriptions: Dict[int, List[Tuple[str,str]]] = {}

    idx: int = 0
    with open("no_delexi_data/" + chart_file, 'r') as fin:
        inline = fin.readline() # Reads ''
        inline = fin.readline()
        # While we did not reach the end of the file        
        while inline != '':
            # Remove the \n from the strings
            inline = inline.replace("\n", "")
            # Split on the spaces
            splited_inline = inline.split('    ')
            # If we have annotated lines
            if (len(splited_inline) == 2):
                chart_descriptions.setdefault(idx, list()).append((splited_inline[0], splited_inline[1]))
            
            if inline == '<end_of_description>':
                    idx += 1
                    inline = fin.readline()
            else:
                inline = fin.readline()
                
    pprint(chart_descriptions)
    #print(idx)
    
    return chart_descriptions

def turn_dict_into_opt_b(chart_descs: Dict[int, List[Tuple[str,str]]]) -> Dict[int, Dict[str, Set[str]]]:
    chart_infos: Dict[int, Dict[str, Set[str]]] = {}
    for idx, val in chart_descs.items():
        chart_infos.setdefault(idx, {})
        for el in val:
            proc_idx = el[1].lstrip(" <").rstrip("> ")
            chart_infos[idx].setdefault(proc_idx, set()).add(el[0])
    pprint(chart_infos)
    return chart_infos


def parse_info_files_all_charts(chart) -> Tuple[Dict[str, List[Tuple[int, str]]], Dict[str, List[Tuple[int, str]]], Dict[str, List[Tuple[int, List[str]]]],Dict[str, List[Tuple[int, List[str]]]]]:
    x_categories: Dict[str, List[Tuple[int, str]]] = {}
    y_values: Dict[str, List[Tuple[int, str]]] = {}
    differences_add: Dict[str, List[Tuple[int, List[str]]]] = {}
    differences_mul: Dict[str, List[Tuple[int, List[str]]]] = {}
    
    with open("charts_info/" + chart, 'r') as f:
        data = f.read()
    lines = data.split("\n")
    # Kick out the title
    lines = lines[1:]
    for line in lines:
        # Each line looks like this: key : values
        # aux[0] is key and aux[1] is values
        if ":" in line:
            aux = line.split(" : ")
            if "x categories" in aux:
                # Category
                new_list: List[Tuple[int, str]] = []
                processed_values: List[str] = aux[1].split(", ")
                for idx, val in enumerate(processed_values):
                    new_list.append((idx, val))
                x_categories[chart] = new_list
            elif "y values" in aux:
                new_list: List[Tuple[int, str]] = []
                processed_values: List[str] = aux[1].split(", ")
                for idx, val in enumerate(processed_values):
                    new_list.append((idx, val))
                y_values[chart] = new_list
            # differences ADD
            elif "pairs" in aux:
                new_list: List[Tuple[int, List[str]]] = []
                processed_values: List[str] = aux[1].split("\t ")
                processed_values = [val.strip("\t") for val in processed_values]
                #re.split(r'\t ?', aux[1])
                for idx, val in enumerate(processed_values):
                    interm_list: List[str] = val.split("-")
                    new_list.append((idx, interm_list))
                differences_add[chart] = new_list
            # differences MUL
            elif "pairs_float" in aux:
                new_list: List[Tuple[int, List[str]]] = []
                processed_values: List[str] = aux[1].split("\t ")
                processed_values = [val.strip("\t") for val in processed_values]
                for idx, val in enumerate(processed_values):
                    interm_list: List[str] = val.split("-")
                    new_list.append((idx, interm_list))
                differences_mul[chart] = new_list

    print(x_categories, y_values, differences_add, differences_mul)
    return x_categories, y_values, differences_add, differences_mul


def generate_files_opt_b(chart_infos: Dict[int, Dict[str, Set[str]]]) -> List[str]:
    all_chart_lines: List[str] = []
    global_counter: int = 1
    # idx: int, all_vals: Dict[str, Set[str]]
    for idx, all_vals in chart_infos.items():
        chart_line: str = ""
        # dict_idx: str, elems: Set[str]
        for dict_idx, elems in all_vals.items():
            # If the set has only one element
            if len(elems) == 1:
                # Store that one element
                element: str = list(elems)[0]
                all_words_in_element: List[str] = element.split(" ")
                # If element contains one word
                '''if len(all_words_in_element) == 1:
                    chart_line += f"{dict_idx}_1:{element}\t"
                else:'''
                for word_idx, word in enumerate(all_words_in_element):
                    chart_line += f"{dict_idx}_{word_idx+1}:{word}\t"
            else: # The set has more than one element
                for set_idx, el in enumerate(elems):
                    all_words_in_element: List[str] = el.split(" ")    
                    # If each element consists of only ONE word
                    '''if len(all_words_in_element) == 1:
                        chart_line += f"{dict_idx}_{set_idx+1}:{el}\t" 
                    else: # if the line contains more than one word
                    '''
                    for widx, wel in enumerate(all_words_in_element):
                        chart_line += f"{dict_idx}_{widx+1}:{wel}\t" 

        chart_line += "\n"
        all_chart_lines.append(chart_line)
    for idx, el in enumerate(all_chart_lines):
        print(idx, el, "\n")
    return all_chart_lines


#TODO: add list of no_delexi data files
if __name__ == "__main__":
    all_charts = ['info_gender_pay_gap.txt', 'info_median_salary_women.txt', 'info_num_top_unis.txt', 'info_student_choice_study.txt', 'info_women_work_sector.txt', 'info_median_salary_se.txt', 'info_money_spent_he.txt', 'info_obesity.txt', 'info_women_study_departments.txt',  'info_young_evenings.txt']
    #all_charts = ['info_gender_pay_gap.txt']
    no_delexi_charts=['women_representation_in_different_sectors.txt']
    chart_descs = parse_info_files_per_chart(no_delexi_charts[0])
    #print(chart_descs)
    #chart_infos_a = turn_dict_into_opt_a(chart_descs)
    chart_infos_b = turn_dict_into_opt_b(chart_descs)
    generate_files_opt_b(chart_infos_b)
    '''with open('chartsopt1.box', 'w') as g:
        for chart in all_charts:
            xcat, yvals, diffadd, diffmul = parse_info_files_all_charts(chart)
            chart_line = generate_files(xcat, yvals, diffadd, diffmul)
            g.write(chart_line)'''

