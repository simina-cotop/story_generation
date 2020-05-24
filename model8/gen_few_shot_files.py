from typing import List, Dict, Tuple, NamedTuple
import matplotlib.pyplot as plt
import os
import glob
import csv
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

def parse_info_files_all_charts(all_charts) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    x_categories: Dict[str, List[str]] = {}
    y_values: Dict[str, List[str]] = {}
    #TODO: differences_add = {}

    for chart in all_charts:
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
                    processed_values: List[str] = aux[1].split(", ")
                    x_categories[chart] = processed_values
                elif "y values" in aux:
                    processed_values: List[str] = aux[1].split(", ")
                    y_values[chart] = processed_values
        print(x_categories, y_values)
    return x_categories, y_values


def generate_files(x_categories: Dict[str, List[str]], y_values: Dict[str, List[str]]) -> str:
    chart_line: str = ""
    for all_values_xcat, all_values_yval in zip(x_categories.values(), y_values.values()):
        for (idx1, val1), (idx2, val2) in zip(enumerate(all_values_xcat), enumerate(all_values_yval)):
            chart_line += f"bar{idx1+1}_x_categories_{idx1+1}:{val1}\tbar{idx1+1}_y_values_{idx2+1}:{val2}\t" 
    print(chart_line)

if __name__ == "__main__":
    #all_charts = ['info_gender_pay_gap.txt', 'info_median_salary_women.txt', 'info_num_top_unis.txt', 'info_student_choice_study.txt', 'info_women_work_sector.txt', 'info_median_salary_se.txt', 'info_money_spent_he.txt', 'info_obesity.txt', 'info_women_study_departments.txt',  'info_young_evenings.txt']
    all_charts = ['info_gender_pay_gap.txt']
    #chart_line = parse_info_files_per_chart(chart_file)

    xcat, yvals = parse_info_files_all_charts(all_charts)
    generate_files(xcat, yvals)

