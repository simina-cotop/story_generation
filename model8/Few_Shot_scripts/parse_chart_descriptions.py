# Generate input files for the chartsoptb domain, from the training data, i.e. chart descriptions given by humans
# including descriptions of the bars as sentences

from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import os
import glob
import csv
import re
from pprint import pprint


def parse_info_files_per_chart(chart_file: str) -> List[str]:
    all_chart_descriptions: Dict[int, List[str]] = {}
    final_chart_descriptions: List[str] = []

    idx: int = 0
    with open("../no_delexi_data/" + chart_file, 'r') as fin:
        inline = fin.readline() # Reads ''
        inline = fin.readline()
        # While we did not reach the end of the file        
        while inline != '':
            # Remove the \n from the strings
            inline = inline.replace("\n", "")
            assert(inline != '')
            # Split on the spaces
            splited_inline = inline.split(' <')
            
            # If we have annotated lines
            assert(splited_inline[0] != '')
            all_chart_descriptions.setdefault(idx, list()).append(splited_inline[0].strip(' '))
                
            if inline == '<end_of_description>':
                    idx += 1
            inline = fin.readline()
    #print(all_chart_descriptions)

    #pprint(all_chart_descriptions)
    for idx, description in all_chart_descriptions.items():
        desc_str: str = ' '.join(description)
        desc_str = desc_str.replace('<end_of_description>','')
        desc_str = desc_str.replace(" .", ".")
        desc_str = desc_str.replace(" %", "%")
        desc_str = desc_str.replace("( ", "(")
        desc_str = desc_str.replace(" )", ")")
        final_chart_descriptions.append(desc_str)
    #print(final_chart_descriptions)
    return final_chart_descriptions


if __name__ == "__main__":
    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    #no_delexi_charts = ['women_representation_in_different_sectors.txt']
    
    
    with open('chartsoptb.summary', 'w') as g:
        for chart in no_delexi_charts:
            chart_descs = parse_info_files_per_chart(chart)
            for desc in chart_descs:
                g.write(desc + "\n")
    
    with open('train.summary', 'w') as train:
        with open('test.summary', 'w') as test:
            with open('valid.summary', 'w') as valid:
                for chart in no_delexi_charts:
                    chart_descs = parse_info_files_per_chart(chart)
                    for desc_idx, desc in enumerate(chart_descs):
                        if desc_idx in list(range(17)):
                            #print("train=", desc_idx)
                            train.write(desc + "\n")
                        elif desc_idx in list(range(17,20)):
                            test.write(desc + "\n")
                            #print("test=", desc_idx)
                        elif desc_idx in list(range(20,23)):
                            #print("valid=", desc_idx)
                            valid.write(desc + "\n")