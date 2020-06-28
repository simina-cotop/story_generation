# Generate input files for the chartsopta and chartsoptb domains, from the training data, i.e. chart descriptions given by humans
# including descriptions of the bars as annotated information

from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import os
import glob
import re
from pprint import pprint
from parse_chart_descriptions import turn_chart_info_files_into_sentences
from gensim.models import Phrases

# Each line in the file will look like this:
# global description + local description, where the local one will be 23 different ones

# 1. Parse the info files to get the global information and create a dictionary which has as key each bar basic info 
# 2. Parse the description files to get the sentences corresponding to each bar and add those to the dictionary
# 3. From the dictionary generate the files according to the correct structure


def turn_chart_info_into_sentences(chart_file: str) -> Tuple[Dict[int, Dict[int, List[Tuple[str,str]]]], Dict[int, Dict[int, List[Tuple[str,str]]]]]:
    # chart_descriptions[0] = {0: List[(law firms, <x_axis_label_highest_value>),(highest, <y_axis_highest_value>)], 1:List[()],...}
    chart_descriptions: Dict[int, Dict[int, List[Tuple[str,str]]]] = {}
    reversed_chart_descriptions: Dict[int, Dict[int, List[Tuple[str,str]]]] = {}
    
    # idx: description index
    idx: int = 0

    with open("../no_delexi_data/" + chart_file, 'r') as fin:
        
        inline = fin.readline() # Reads ''
        inline = fin.readline()
        
        # sent_idx: sentence index
        sent_idx: int = 0

        # While we did not reach the end of the file        
        while inline != '':
            
            chart_descriptions.setdefault(idx, {})
            reversed_chart_descriptions.setdefault(idx, {})

            inline = inline.replace("\n", "")
            assert(inline != '')
            # Split on the spaces
            splited_inline = inline.split(' <')

            # If we have annotated lines
            if (len(splited_inline) == 2):
                assert(splited_inline[1] != '')
                chart_descriptions[idx].setdefault(sent_idx, list()).append((splited_inline[0].strip(' '), splited_inline[1].rstrip("> ")))
                reversed_chart_descriptions[idx].setdefault(sent_idx, list()).append((splited_inline[1].rstrip("> "), splited_inline[0].strip(' ')))

            # If we found a dot, we need to start a new sentence
            if inline == '.':
                sent_idx += 1
            
            if inline == '<end_of_description>':
                    idx += 1
                    sent_idx = 0
                    inline = fin.readline()
            else:
                inline = fin.readline()
                
    #pprint(chart_descriptions)
    #pprint(reversed_chart_descriptions)

    return chart_descriptions, reversed_chart_descriptions


def convert_sentences_to_bigrams(reversed_chart_descs: Dict[int, Dict[int, List[Tuple[str,str]]]], bigram) -> Dict[int, Dict[int, List[Tuple[str,List[str]]]]]:
    new_reversed_chart_descriptions: Dict[int, Dict[int, List[Tuple[str,List[str]]]]] = {}
    #all_vals: Dict[int, List[Tuple[str,str]]]
    for idx, all_vals in reversed_chart_descs.items():
        new_reversed_chart_descriptions[idx] = {}
        #all_sents: List[Tuple[str,str]]
        for sent_idx, all_sents in all_vals.items():
            interm_list = []
            # dict_idx: int, elems: Tuple[str,str]
            for dict_idx, elems in enumerate(all_sents):
                interm_sent = elems[1].split(" ")
                interm_list.append((elems[0], bigram[interm_sent]))
            new_reversed_chart_descriptions[idx][sent_idx] = interm_list
    return new_reversed_chart_descriptions



def generate_files_sa(new_reversed_chart_descs: Dict[int, Dict[int, List[Tuple[str,List[str]]]]]) -> List[str]:
    all_chart_lines: List[str] = []
    global_counter: int = 1
    
    # idx: int, all_vals: Dict[int, List[Tuple[str,str]]]
    for idx, all_vals in new_reversed_chart_descs.items():
        for sent_idx, all_sents in all_vals.items():
            chart_line: str = ""
            # dict_idx: int, elems: Tuple[str,str]
            for dict_idx, elems in enumerate(all_sents):
                all_words_in_element: List[str] = elems[1]
                # Iterate over the words in a sentence and output them
                for word_idx, word in enumerate(all_words_in_element):
                    chart_line += f"{elems[0]}_{word_idx+1}:{word}\t"
                    
            chart_line = chart_line.rstrip('\t')
            chart_line += "\n"
            all_chart_lines.append(chart_line)
    '''for idx, el in enumerate(all_chart_lines):
        pprint(new_reversed_chart_descs[idx])
        print(idx, el, "\n\n\n")'''
    return all_chart_lines


def write_to_file_chartssa(no_delexi_charts: List[str], all_sents: List[List[str]]) -> None:
    with open(os.path.join('chartssa/original_data/','chartssa.box'), 'w') as g:
        with open(os.path.join('chartssa/original_data/','train.box'), 'w') as train:
            with open(os.path.join('chartssa/original_data/','test.box'), 'w') as test:
                with open(os.path.join('chartssa/original_data/','valid.box'), 'w') as valid:
        
                    for chart in no_delexi_charts:

                        chart_descs, reversed_chart_descs = turn_chart_info_into_sentences(chart)
                        
                        #pprint(chart_descs)
                        #pprint(reversed_chart_descs)
                        #pprint(all_sents)

                        #!!! all_sents must contain a list of sentences, with each sentence being a list of words
                        bigram = Phrases(all_sents, min_count=1, threshold=10)
                        bigram.add_vocab([["Financial", "Groups"], ["Law", "Firms"], ["Computer", "Science"]])
                        #print("aaaaaaaa=",bigram[['Financial', 'Groups', 'are', 'more', 'awsome', 'than', 'law', 'firms', 'and', 'even', 'more', 'awesome', 'than', 'computer', 'science']])
                        #print(bigram.vocab)

                        new_reversed_chart_descs = convert_sentences_to_bigrams(reversed_chart_descs, bigram)
                        #pprint(new_reversed_chart_descs)

                        # chart_lines_senta : all the sentences belonging to chart `chart`
                        chart_lines_sa = generate_files_sa(new_reversed_chart_descs)
                        #pprint(chart_lines_sa)

                        len_all_chart_sentences = len(chart_lines_sa)
                        #print("len=", len_all_chart_sentences)
                        g.write(''.join(chart_lines_sa))

                        for line_idx, chart_line in enumerate(chart_lines_sa):
                            if line_idx in list(range(5)):
                                #print("test=", line_idx)
                                test.write(chart_line)
                            elif line_idx in list(range(5,10)):
                                #print("valid=", line_idx)
                                valid.write(chart_line)
                            elif line_idx in list(range(10,len_all_chart_sentences)):
                                #print("train=", line_idx)
                                train.write(chart_line)


def turn_dict_into_sent_b(chart_descs: Dict[int, Dict[int, List[Tuple[str,str]]]]) -> Dict[int, Dict[int, Dict[str, Set[str]]]]:
    chart_infos: Dict[int, Dict[int, Dict[str, Set[str]]]] = {}
    # all_vals: Dict[int, List[Tuple[str,str]]]
    for idx, all_vals in chart_descs.items():
        chart_infos.setdefault(idx, {})
        # all_sents: List[Tuple[str,str]]]
        for sent_idx, all_sents in all_vals.items():
            chart_infos[idx].setdefault(sent_idx, {})
            for el in all_sents:
                proc_idx = el[1].lstrip(" <").rstrip("> ")
                assert(proc_idx != '')
                chart_infos[idx][sent_idx].setdefault(proc_idx, set())
                if el[0].lower() not in chart_infos[idx][sent_idx][proc_idx]:
                    chart_infos[idx][sent_idx][proc_idx].add(el[0])
    print("HERE\n")
    pprint(chart_infos)
    return chart_infos

def convert_chartssb_to_bigrams(chart_infos: Dict[int, Dict[int, Dict[str, Set[str]]]], bigram2) -> Dict[int, Dict[int, Dict[str, List[str]]]]:
    new_chart_infos: Dict[int, Dict[int, Dict[str, List[str]]]] = {}
    # all_vals: Dict[int, Dict[str, Set[str]]]
    for idx, all_vals in chart_infos.items():
        new_chart_infos.setdefault(idx, {})
        # sent_idx:int, all_sents: Dict[str, Set[str]]
        for sent_idx, all_sents in all_vals.items():
            new_chart_infos[idx].setdefault(sent_idx, {})
            # a_idx: str, all_sents: Set[str]
            for a_idx, all_set in all_sents.items():
                new_chart_infos[idx][sent_idx].setdefault(a_idx,list())
                for el in all_set:
                    el = el.replace(",", "")
                    new_chart_infos[idx][sent_idx][a_idx] += bigram2[el.split(" ")]
    print("HERE3\n")
    pprint(new_chart_infos)
    return new_chart_infos

def generate_files_sb(chart_infos: Dict[int, Dict[int, Dict[str, List[str]]]]) -> List[str]:
    #print("HERE2\n")
    all_chart_lines: List[str] = []
    global_counter: int = 1
    # idx: int, all_vals: Dict[int, Dict[str, List[str]]]
    for idx, all_vals in chart_infos.items():
        # sent_idx: int, all_sents: Dict[str, List[str]]]
        for sent_idx, all_sents in all_vals.items():
            chart_line: str = ""
            # dict_idx: str, elems: List[str]
            for dict_idx, elems in all_sents.items():
                    for word_idx, word in enumerate(elems):
                        chart_line += f"{dict_idx}_{word_idx+1}:{word}\t"
            chart_line = chart_line.rstrip('\t')
            chart_line += "\n"
            all_chart_lines.append(chart_line)
    for idx, el in enumerate(all_chart_lines):
        print(idx, el, "\n")
    return all_chart_lines


def write_to_file_chartssb(no_delexi_charts: List[str], all_sents: List[List[str]]) -> None:
    with open(os.path.join('chartssb/original_data/','chartssb.box'), 'w') as g:
        with open(os.path.join('chartssb/original_data/','train.box'), 'w') as train:
            with open(os.path.join('chartssb/original_data/','test.box'), 'w') as test:
                with open(os.path.join('chartssb/original_data/','valid.box'), 'w') as valid:
        
                    for chart in no_delexi_charts:

                        chart_descs, _ = turn_chart_info_into_sentences(chart)
                        #print(chart_descs)

                        bigram2 = Phrases(all_sents, min_count=1, threshold=2)
                        bigram2.add_vocab([["Financial", "Groups"], ["Law", "Firms"], ["Computer", "Science"]])
                        print("vocab=",bigram2.vocab)
                        chart_infos_sentb = turn_dict_into_sent_b(chart_descs)
                        new_infos = convert_chartssb_to_bigrams(chart_infos_sentb, bigram2)
                        chart_lines_sentb = generate_files_sb(new_infos)
                        len_all_chart_sentences = len(chart_lines_sentb)
                        print("len=", len_all_chart_sentences)
                        g.write(''.join(chart_lines_sentb))

                        for line_idx, chart_line in enumerate(chart_lines_sentb):
                            if line_idx in list(range(5)):
                                #print("test=", line_idx)
                                test.write(chart_line)
                            elif line_idx in list(range(5,10)):
                                #print("valid=", line_idx)
                                valid.write(chart_line)
                            elif line_idx in list(range(10,len_all_chart_sentences)):
                                #print("train=", line_idx)
                                train.write(chart_line)



if __name__ == "__main__":

    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    #no_delexi_charts = ['women_representation_in_different_sectors.txt']

    all_descriptions: List[List[str]] = []
    for chart in no_delexi_charts:
        current_desc: List[str] = turn_chart_info_files_into_sentences(chart)
        for desc in current_desc:
            all_words = desc.split(" ")
            all_descriptions.append(all_words)
   
    #Create chartssenta files
    #write_to_file_chartssa(no_delexi_charts, all_descriptions)

    #Create chartssentb files
    write_to_file_chartssb(no_delexi_charts, all_descriptions)
        



    
    