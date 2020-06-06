# Generate input files for the chartsopta and chartsoptb domains, from the training data, i.e. chart descriptions given by humans
# including descriptions of the bars as annotated information

from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import os
import glob
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
            if (len(splited_inline) == 2):
                assert(splited_inline[1] != '')
                chart_descriptions.setdefault(idx, list()).append((splited_inline[0].strip(' '), splited_inline[1].rstrip("> ")))
            
            if inline == '<end_of_description>':
                    idx += 1
                    inline = fin.readline()
            else:
                inline = fin.readline()
                
    pprint(chart_descriptions)
    #print(idx)
    
    return chart_descriptions


def turn_dict_into_opt_a(chart_descs: Dict[int, List[Tuple[str,str]]]) -> Dict[int, Dict[str, Set[str]]]:
    chart_infos: Dict[int, Dict[str, Set[str]]] = {}
    for idx, val in chart_descs.items():
        chart_infos.setdefault(idx, {})
        for el in val:
            proc_idx = el[1].lstrip(" <").rstrip("> ")
            assert(proc_idx != '')
            chart_infos[idx].setdefault(proc_idx, set())
            if el[0].lower() not in chart_infos[idx][proc_idx]:
                chart_infos[idx][proc_idx].add(el[0])
    pprint(chart_infos)
    pprint(chart_descs)
    return chart_infos


def generate_files_opt_a(chart_infos: Dict[int, Dict[str, Set[str]]]) -> List[str]:
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
                # Iterate over the words in a sentence and output them
                for word_idx, word in enumerate(all_words_in_element):
                    chart_line += f"{dict_idx}_{word_idx+1}:{word}\t"
            else: # The set has more than one element
                for set_idx, el in enumerate(elems):
                    all_words_in_element: List[str] = el.split(" ")    
                    # Iterate over the words in a sentence and output them
                    for widx, wel in enumerate(all_words_in_element):
                        chart_line += f"{dict_idx}_{widx+1}:{wel}\t" 
        chart_line += "\n"
        all_chart_lines.append(chart_line)
    #for idx, el in enumerate(all_chart_lines):
    #    print(idx, el, "\n")
    return all_chart_lines



def turn_dict_into_opt_b(chart_descs: Dict[int, List[Tuple[str,str]]]) -> Dict[int, Dict[str, Set[str]]]:
    chart_infos: Dict[int, Dict[str, Set[str]]] = {}
    for idx, val in chart_descs.items():
        chart_infos.setdefault(idx, {})
        for el in val:
            proc_idx = el[1].lstrip(" <").rstrip("> ")
            assert(proc_idx != '')
            chart_infos[idx].setdefault(proc_idx, set())
            if el[0].lower() not in chart_infos[idx][proc_idx]:
                chart_infos[idx][proc_idx].add(el[0])
    #pprint(chart_infos)
    return chart_infos


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
                # Iterate over the words in a sentence and output them
                for word_idx, word in enumerate(all_words_in_element):
                    chart_line += f"{dict_idx}_{word_idx+1}:{word}\t"
            else: # The set has more than one element
                for set_idx, el in enumerate(elems):
                    all_words_in_element: List[str] = el.split(" ")    
                    # Iterate over the words in a sentence and output them
                    for widx, wel in enumerate(all_words_in_element):
                        chart_line += f"{dict_idx}_{widx+1}:{wel}\t" 
        chart_line = chart_line.rstrip('\t')
        chart_line += "\n"
        all_chart_lines.append(chart_line)
    #for idx, el in enumerate(all_chart_lines):
    #    print(idx, el, "\n")
    return all_chart_lines


if __name__ == "__main__":
    all_charts = ['info_gender_pay_gap.txt', 'info_median_salary_women.txt', 'info_num_top_unis.txt', 'info_student_choice_study.txt', 'info_women_work_sector.txt', 'info_median_salary_se.txt', 'info_money_spent_he.txt', 'info_obesity.txt', 'info_women_study_departments.txt',  'info_young_evenings.txt']
    #all_charts = ['info_gender_pay_gap.txt']

    #no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    no_delexi_charts = ['women_representation_in_different_sectors.txt']
    
    with open('chartsopta.box', 'w') as g:
        #for chart in no_delexi_charts:

        chart_descs = parse_info_files_per_chart(no_delexi_charts[0])
        #print(chart_descs)

        chart_infos_a = turn_dict_into_opt_a(chart_descs)
        chart_lines_a = generate_files_opt_a(chart_infos_a)

        g.write(''.join(chart_lines_a)+'\n\n')


#TODO: uncomment this when I am done generating chartsopta
    with open(os.path.join('chartsoptb/original_data/','chartsoptb.box'), 'w') as g:
        for chart in no_delexi_charts:
            chart_descs = parse_info_files_per_chart(chart)
            #print(chart_descs)

            chart_infos_b = turn_dict_into_opt_b(chart_descs)
            chart_lines_b = generate_files_opt_b(chart_infos_b)

            g.write(''.join(chart_lines_b))

            with open(os.path.join('chartsoptb/original_data/','train.box'), 'w') as train:
                with open(os.path.join('chartsoptb/original_data/','test.box'), 'w') as test:
                    with open(os.path.join('chartsoptb/original_data/','valid.box'), 'w') as valid:
                        for line_idx, chart_line in enumerate(chart_lines_b):
                            if line_idx in list(range(17)):
                                #print("train=", desc_idx)
                                train.write(chart_line)
                            elif line_idx in list(range(17,20)):
                                test.write(chart_line)
                                #print("test=", desc_idx)
                            elif line_idx in list(range(20,23)):
                                #print("valid=", desc_idx)
                                valid.write(chart_line)

    