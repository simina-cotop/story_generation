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


def turn_chart_info_files_into_sentences(chart_file: str) -> List[str]:
    all_chart_descriptions: Dict[int, Dict[int, List[str]]] = {}
    final_chart_descriptions: List[str] = []

    # idx: description index
    idx: int = 0

    with open("../no_delexi_data/" + chart_file, 'r') as fin:
        inline = fin.readline() # Reads ''
        inline = fin.readline()

        # sent_idx: sentence index
        sent_idx: int = 0

        # While we did not reach the end of the file        
        while inline != '':
            all_chart_descriptions.setdefault(idx, {})

            # Remove the \n from the strings
            inline = inline.replace("\n", "")
            assert(inline != '')
            # Split on the spaces
            splited_inline = inline.split(' <')
            
            # If we have annotated lines
            assert(splited_inline[0] != '')
            if splited_inline[0] != '<end_of_description>':
                all_chart_descriptions[idx].setdefault(sent_idx, list()).append(splited_inline[0].strip(' '))

            # If we found a dot, we need to start a new sentence
            if inline == '.':
                sent_idx += 1
                
            if inline == '<end_of_description>':
                    idx += 1
            inline = fin.readline()
    #print(all_chart_descriptions)

    #pprint(all_chart_descriptions)
    # all_sentences: Dict[int, List[str]]
    for idx, all_sentences in all_chart_descriptions.items():
        for sent_idx, sent in all_sentences.items():
            desc_str: str = ' '.join(sent)
            desc_str = desc_str.replace('<end_of_description>','')
            desc_str = desc_str.replace(" .", ".")
            desc_str = desc_str.replace(" %", "%")
            desc_str = desc_str.replace("( ", "(")
            desc_str = desc_str.replace(" )", ")")
            final_chart_descriptions.append(desc_str)
    '''for idx, el in enumerate(final_chart_descriptions):
        print(idx, el, '\n')
    print(len(final_chart_descriptions))'''
    return final_chart_descriptions

def create_chartsoptb_summary(no_delexi_charts: List[str]) -> None:
    with open(os.path.join('chartsoptb/original_data/','chartsoptb.summary'), 'w') as g:
        for chart in no_delexi_charts:
            chart_descs = parse_info_files_per_chart(chart)
            for desc in chart_descs:
                g.write(desc + "\n")

def create_separate_gold_files_opt_dom(no_delexi_charts: List[str]) -> None:
        for cidx, chart in enumerate(no_delexi_charts):
            chart_descs = parse_info_files_per_chart(chart)
            for idx, desc in enumerate(chart_descs):
                if idx in list(range(20,23)):
                    with open(f'chartsopta/all_gold/opta_gold_{cidx}_{idx-20}', 'w') as g:
                        g.write(desc + "\n")



def create_chartsoptb_files(no_delexi_charts: List[str]) -> None:
    with open(os.path.join('chartsoptb/original_data/','train.summary'), 'w') as train:
        with open(os.path.join('chartsoptb/original_data/','test.summary'), 'w') as test:
            with open(os.path.join('chartsoptb/original_data/','valid.summary'), 'w') as valid:
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



def create_chartssenta_summary(no_delexi_charts: List[str]) -> None:
    with open(os.path.join('chartssenta/original_data/','chartssenta.summary'), 'w') as g:
        for chart in no_delexi_charts:
            chart_descs = turn_chart_info_files_into_sentences(chart)
            for desc in chart_descs:
                g.write(desc + "\n")

def create_separate_gold_files_sent_dom(no_delexi_charts: List[str]) -> None:
        for cidx, chart in enumerate(no_delexi_charts):
            chart_descs = turn_chart_info_files_into_sentences(chart)
            for idx, desc in enumerate(chart_descs):
                if idx in list(range(5,10)):
                    with open(f'chartssenta/all_gold/senta_gold_{cidx}_{idx-5}', 'w') as g:
                        g.write(desc + "\n")
                    
    
            

def create_chartssenta_files(no_delexi_charts: List[str]) -> None:
    with open(os.path.join('chartssenta/original_data/','train.summary'), 'w') as train:
        with open(os.path.join('chartssenta/original_data/','test.summary'), 'w') as test:
            with open(os.path.join('chartssenta/original_data/','valid.summary'), 'w') as valid:
                for chart in no_delexi_charts:
                    # charts_descs: list containing all the sentences belonging to only ONE chart
                    chart_descs = turn_chart_info_files_into_sentences(chart)
                    print("len=", len(chart_descs))
                    for desc_idx, desc in enumerate(chart_descs):
                        if desc_idx in list(range(5)):
                            #print("test=", desc_idx)
                            test.write(desc + "\n")
                        elif desc_idx in list(range(5,10)):
                            #print("valid=", desc_idx)
                            valid.write(desc + "\n")
                        elif desc_idx in list(range(10,len(chart_descs))):
                            #print("train=", desc_idx)
                            train.write(desc + "\n")


def gen_gold_files(no_delexi_charts: List[str]) -> None:
    for idx, chart in enumerate(no_delexi_charts):
        with open(f'desc_sent_{idx}', 'w') as desc_sent:
                # chart_descs: List[str] corressponding to ONE chart
                chart_descs = turn_chart_info_files_into_sentences(chart)
                for desc in chart_descs:
                    desc_sent.write(desc + "\n")




if __name__ == "__main__":
    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    #no_delexi_charts = ['women_representation_in_different_sectors.txt']
    
    
    # Create .summary file for chartsoptb
    #create_chartsoptb_summary(no_delexi_charts)

    # Create the rest of the .summary files for chartsoptb
    #create_chartsoptb_files(no_delexi_charts)

    # Parse the .txt files with the chart descriptions and return a list of strings containins the sentences
    #all_descriptions = turn_chart_info_files_into_sentences(no_delexi_charts[0])

    # Create .summary file for chartssenta
    ##create_chartssenta_summary(no_delexi_charts)

    # Create the rest of the .summary files for chartsoptb
    ##create_chartssenta_files(no_delexi_charts)  

    #Generate gold text files for BLEU
    #gen_gold_files(no_delexi_charts)

    #Generate SEPARATE gold text files for BLEU for sent domain
    create_separate_gold_files_sent_dom(no_delexi_charts)

    #Generate SEPARATE gold text files for BLEU for opt domain
    create_separate_gold_files_opt_dom(no_delexi_charts)


