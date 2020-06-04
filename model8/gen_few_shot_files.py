# Generate input files for the chartsopt1 domain, from the training data, i.e. chart descriptions given by humans

from typing import List, Dict, Tuple, NamedTuple
import matplotlib.pyplot as plt
import os
import glob
import csv
import re
from pprint import pprint

def parse_info_files_per_chart(chart_file) -> str:
    chart_line: str = ""
    with open("charts_info/" + chart_file, 'r') as f:
        data = f.read()
    lines = data.split("\n")
    # Kick out the title
    lines = lines[1:]
    for line in lines:
        # Each line looks like this: key : values
        # aux[0] is key and aux[1] is values
        if ":" in line:
            aux = line.split(" : ")
            # Category
            values: str = aux[1]
            if "," in values:
                processed_values: List[str] = aux[1].split(", ")
            else:
                processed_values: List[str] = aux[1].split("\t")
            for val_idx, val in enumerate(processed_values):
                chart_line += aux[0].replace(" ", "_") + f"_{val_idx+1}:{val}\t" 
    print(chart_line)
    return chart_line

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


def generate_files(x_categories: Dict[str, List[Tuple[int, str]]], y_values: Dict[str, List[Tuple[int, str]]], diff_add: Dict[str, List[Tuple[int, List[str]]]], diff_mul: Dict[str, List[Tuple[int, List[str]]]]) -> str:
    chart_line: str = ""
    global_counter: int = 1
    for all_values_xcat, all_values_yval in zip(x_categories.values(), y_values.values()):
        for (idx1, val1), (idx2, val2) in zip(all_values_xcat, all_values_yval):
            chart_line += f"bar{idx1+1}_x_categories_{global_counter}:{val1}\tbar{idx1+1}_y_values_{global_counter}:{val2}\t" 
            for all_values_diffadd in diff_add.values():
                for (idx3, val3) in all_values_diffadd:
                    if val1 in val3:
                        local_counter:int = 0
                        for el in val3:
                            chart_line += f"bar{idx1+1}_diffadd{idx3}_{global_counter+local_counter}:{el}\t"
                            local_counter += 1
            for all_values_diffmul in diff_mul.values():
                for (idx4, val4) in all_values_diffmul:
                    if val1 in val4:
                        local_counter:int = 0
                        for el in val4:
                            chart_line += f"bar{idx1+1}_diffmul{idx4}_{global_counter+local_counter}:{el}\t"
                            local_counter += 1
    chart_line += "\n"
    print(chart_line)
    return chart_line

if __name__ == "__main__":
    all_charts = ['info_gender_pay_gap.txt', 'info_median_salary_women.txt', 'info_num_top_unis.txt', 'info_student_choice_study.txt', 'info_women_work_sector.txt', 'info_median_salary_se.txt', 'info_money_spent_he.txt', 'info_obesity.txt', 'info_women_study_departments.txt',  'info_young_evenings.txt']
    #all_charts = ['info_gender_pay_gap.txt']

    #chart_line = parse_info_files_per_chart(chart_file)
    with open('chartsopt1.box', 'w') as g:
        for chart in all_charts:
            xcat, yvals, diffadd, diffmul = parse_info_files_all_charts(chart)
            chart_line = generate_files(xcat, yvals, diffadd, diffmul)
            g.write(chart_line)

