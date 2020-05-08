from __future__ import annotations
from collections import OrderedDict
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from nltk.corpus import stopwords
import os
import sys
import glob
import re
import subprocess
import spacy
import numpy as np


nlp = spacy.load('en')


@dataclass(init=False)
class Description:
    text: str
    splitted_text: List[str]
    no_stops_text: List[str]
    no_punc_desc: List[str]
    length: int
    number_of_annotations: int
    delexi: List[str]
    ner_text: List[str]
    extra_info: List[str]
    

    def __init__(self: "Description", text: str) -> None:
        super().__init__()
        
        self.text = text.replace('\n', ' ')
        self.splitted_text = self.text.split()
        self.no_stops_text = [t for t in self.splitted_text if t not in stopwords.words('english')]
        self.no_punc_desc = [word for word in self.no_stops_text if word.isalpha()]
        self.length = len(self.splitted_text)
        counter = 0
        for word in self.splitted_text:
            if "<" in word:
                counter += 1
        self.number_of_annotations = counter
        self.delexi = []
        self.ner_text = []
        self.extra_info = []

    def __str__(self: "Description") -> str:
        return f"{self.length} {self.text} {self.number_of_annotations}\n"

    def count_delexicalizations(self: "Description") -> None:
        delexicalization: List[str] = ["NUMBER_HIGHEST", "NUMBER_LEAST", "NUMBER_SCND", "NUMBER_3RD", "NUMBER_4TH", "X_AXIS_HIGHEST", "X_AXIS_LEAST", "X_AXIS_SCND", "X_AXIS_3RD", "X_AXIS_4TH"]
        delexicalization_lower: List[str] = [word.lower() for word in delexicalization]

        # Check if delexicalization words appear
        for word in self.no_stops_text:
            if word in delexicalization or word in delexicalization_lower:
                self.delexi.append(word)

    def count_ners(self: "Description", chrt_vals: List[str]) -> None:
        # For each description get the named entities
        ner = nlp(self.text)
        entities = ner.ents
        # Check which of those do not appear in the chart and save them (the extra ones)
        for entity in entities:
            #self.ner_text.append(entity.text)
            if entity.text not in chrt_vals:
                self.ner_text.append(entity.text)

    # Step 3: check if the script appears (TODO: or anything else that was not caught before)
    def count_extra_info(self: "Description", scr: str) -> None:
        for word in self.no_punc_desc:
            if word not in scr:
                self.extra_info.append(word)
        
        
        
# Get list of the folders which contain the results
def parse_output(script: str) -> List[str]:
    dirs = os.listdir("outputs")
    dirs_script = [d for d in dirs if script in d]
    return dirs_script


# Print the results dictionary
def print_dictionary(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> None:
    for ep in dic:
        print("ep=",ep)
        for beam, l in dic[ep].items():
            print("beam=",beam)
            for desc in l:
                print(desc)
        print('\n')


def init_dict(epochs: List[int], beams: List[str]) -> OrderedDict[int, OrderedDict[str, List[Description]]]:
    test_dict: OrderedDict[int, OrderedDict[str, List[Description]]] = OrderedDict()
    for epoch in epochs:
        test_dict[epoch] = OrderedDict()
        for beam in beams:
            test_dict[epoch][beam] = []
        test_dict[epoch]['nucleus'] = []
    return test_dict


def get_description_list(dic: OrderedDict[int, OrderedDict[str, List[Description]]], epoch: int, beam: str) -> List[Description]:
    inner_dic: OrderedDict[str, List[Description]] = dic[epoch]
    description_list: List[Description] = inner_dic[beam]
    return description_list        


# Parse all the output files and save the data in a dictionary
def get_dictionary(script_folders: List[str], epochs: List[int], beams: List[str]) -> OrderedDict[int, OrderedDict[str, List[Description]]]:
    epoch_dict = init_dict(epochs, beams)
    for epoch in epochs:
        epoch_folders: List[str] = [fol for fol in script_folders if str(epoch) + 'epochs' in fol]
        for beam in beams:
            for current_folder in epoch_folders:
                if beam in current_folder:
                    filename: str = 'samples_' + current_folder
                    newer_data: List[Description] = []
                    with open('outputs/' + current_folder + '/' + filename) as f:
                        data: str = f.read()
                        # Remove the epoch-related information
                        data = data.split('===============================')[0]
                        new_data: List[str] = re.split('-- TEXT [\d]* ---', data)
                        # Remove script name
                        new_data = new_data[1:]
                        # Remove '\n'
                        for el in new_data:
                            newer_data.append(Description(el))
                    epoch_dict[epoch][beam]= newer_data
                elif 'nucleus' in current_folder:
                    nfilename: str = 'samples_' + current_folder
                    nnewer_data: List[Description] = []
                    with open('outputs/' + current_folder + '/' + nfilename) as f:
                        ndata: str = f.read()
                        # Remove the epoch-related information
                        ndata = ndata.split('===============================')[0]
                        nnew_data: List[str] = re.split('-- TEXT [\d]* ---', ndata)
                        # Remove script name
                        nnew_data = nnew_data[1:]
                        # Remove '\n'
                        for el in nnew_data:
                            nnewer_data.append(Description(el))
                    epoch_dict[epoch]['nucleus']= nnewer_data
    #print_dictionary(epoch_dict)
    return epoch_dict
    
# Example of a table row without any evaluation measures    
def generate_table_content(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> str:
    row: str = ""

    for ep in dic:
        row_head: str = str(ep) + ' epochs &'
        row_values: List[int] = []
        for el in dic[ep]:
            l: List[Description] = dic[ep][el]
            row_values.append(len(l))

    row_middle = " & ".join(str(x) for x in row_values) + "\\\\ \\hline \n"
    row += row_head + row_middle
    return row

# Generate evaluation measure to be added to table
# 1. If annotations appear in the generated text
def generate_eval_annotations(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> str:
    row: str = r'''\multicolumn{5}{|l|}{\textbf{Annotations}  } \\ \hline'''

    # For each epoch
    for ep in dic:
        #row_head: str = r'''\multirow{2}{*}{ '''+ str(ep) + ' epochs} &'
        row_head: str = str(ep) + ' epochs &'
        row_values: List[Tuple[int,int]] = []
        all_annotations: List[str] = []
        # dic[ep]: OrderedDict[str, List[Description]]
        # algo: keys in dic[ep], i.e. either beam+number or nucleus
        for algo in dic[ep]:
                annotation_counter: int = 0
                description_list: List[Description] = dic[ep][algo]
                # Index: number of annotations; values: how many descriptions in description_list have that number of annotations
                annotations: List[int] = np.zeros(10, dtype='int')
                

                # Count how many texts contain annotations
                for description in description_list:
                    print(description)
                    if description.number_of_annotations != 0:
                        annotation_counter += 1
                        # Count how many annotations each text has 
                        annotations[description.number_of_annotations] += 1
                    
                    # Turn the results into strings
                    annotations_str: List[str] = []
                    for an_idx in range(0,len(annotations)):
                        if annotations[an_idx] != 0:
                            annotations_str.append("Texts with " + str(an_idx) + " annotation(s): " + str(annotations[an_idx]) + " ")

                all_annotations.append("\\newline ".join(annotations_str))
                row_values.append((annotation_counter, len(description_list)))

        row_middle: str = " & ".join(x for x in all_annotations) + "\\\\ \\hline \n"
        row_end: str = " & " + " & ".join(str(x) for x in row_values) + "\\\\ \\hline \n"
        row += row_head + row_middle  + row_end
    return row

# TODO: give the list of descriptions as argument instead of the whole dictionary
def count_repetitions(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> None:
    windows = [1, 2, 3, 4]
    #for ep in dic:
    #    for algo in dic[ep]:
    list_of_descriptions: List[Description] = get_description_list(dic, 100, '3')
    for description in list_of_descriptions:
        for window in windows:
            sliced_desc = [description.splitted_text[x:x+window] for x in range(0, len(description.splitted_text),window)]
            print(sliced_desc)
            #for el in sliced_desc:
    print("desc", list_of_descriptions)


# 2. Count how many repetitions appear in the texts
def generate_eval_repetitions(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> str:
    row: str = r'''\multicolumn{5}{|l|}{\textbf{Annotations}  } \\ \hline'''

    # For each epoch
    for ep in dic:
        row_head: str = str(ep) + ' epochs &'
        row_values: List[Tuple[int,int]] = []
        all_annotations: List[str] = []
        # dic[ep]: OrderedDict[str, List[Description]]
        # algo: keys in dic[ep], i.e. either beam+number or nucleus
        for algo in dic[ep]:
                annotation_counter: int = 0
                description_list: List[Description] = dic[ep][algo]
                # Index: number of annotations; values: how many descriptions in description_list have that number of annotations
                annotations: List[int] = np.zeros(10, dtype='int')
                

                # Count how many texts contain annotations
                for description in description_list:
                    print(description)
                    if description.number_of_annotations != 0:
                        annotation_counter += 1
                        # Count how many annotations each text has 
                        annotations[description.number_of_annotations] += 1
                    
                    # Turn the results into strings
                    annotations_str: List[str] = []
                    for an_idx in range(0,len(annotations)):
                        if annotations[an_idx] != 0:
                            annotations_str.append("Texts with " + str(an_idx) + " annotation(s): " + str(annotations[an_idx]) + " ")

                all_annotations.append("\\newline ".join(annotations_str))
                row_values.append((annotation_counter, len(description_list)))

        row_middle: str = " & ".join(x for x in all_annotations) + "\\\\ \\hline \n"
        row_end: str = " & " + " & ".join(str(x) for x in row_values) + "\\\\ \\hline \n"
        row += row_head + row_middle  + row_end
    return row

# Create a dictionary of chart category : actual values 
def parse_chart_info(script: str) -> Tuple[Dict[str, List[str]],List[str]]:
    chart_info : Dict[str, List[str]] = {}
    with open("charts_info/" + "info_" + script + ".txt") as f:
        data = f.read()
    lines = data.split("\n")
    # Kick out all the non-label info (for now)
    lines = lines[:7]
    # Kick out the title
    lines = lines[1:]
    for line in lines:
        aux = line.split(" : ")
        processed_aux: str = aux[1].lower()
        processed_aux = processed_aux.split(", ")
        chart_info[aux[0]] = processed_aux
    #print("d=",chart_info)

    # Store the values
    chart_actual_values = []
    for value in chart_info.values():
        for el in value:
            chart_actual_values.append(el)
    print("c=",chart_actual_values)
    return chart_info, chart_actual_values

def count_extra_info(dic: OrderedDict[int, OrderedDict[str, List[Description]]], chrt_inf: Dict[str, List[str]], chrt_vals: List[str], scr: List[str]) -> None:
    list_of_descriptions: List[Description] = get_description_list(dic, 50, '3')


    #TODO: remove the slicing of the list
    list_of_descriptions = list_of_descriptions[20:22]
    


# 3. Count how much information appears in the description that is not in the chart
def generate_eval_extra_info(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> str:
    row: str = r'''
        \multicolumn{5}{|l|}{\textbf{Extra or wrong information}  } \\ \hline
        \multicolumn{5}{|l|}{\textbf{1. Delexicalization}  } \\ \hline
    '''

    # For each epoch
    for ep in dic:
        row_head: str = str(ep) + ' epochs &'
        row_values: List[Tuple[int,int]] = []
        delexi_result: List[str] = []
        # algo: keys in dic[ep], i.e. either beam+number or nucleus
        for algo in dic[ep]:
                print("algo=", algo)
                description_list: List[Description] = dic[ep][algo]
                # Index: number of annotations; values: how many descriptions in description_list have that number of annotations
                print("len=", len(description_list))
                # 1. Delexicalization
                delexi_counter: int = 0
                # Set of strings for ALL descriptions
                all_delexis: Set[str] = set()
                # Count how many texts contain annotations
                for description in description_list:
                    description.count_delexicalizations()
                    #print(description)
                    if description.delexi != []:
                        delexi_counter += 1
                        for el_delexi in description.delexi:
                            print("here2")
                            all_delexis.add(el_delexi)
                        print("all_delexi=", all_delexis, delexi_counter)

                # Turn the results into strings
                delexi_result.append("There are " + str(delexi_counter) + " delexcalization symbols: " + ", ".join(el.replace("_", "\_") for el in all_delexis))
                print("res=",delexi_result)

        row_end: str = " & ".join(x for x in delexi_result) + "\\\\ \\hline \n"
        row += row_head + row_end
    return row



# Generate the latex table with the results
def generate_table_latex(script:str, annons: str, extra_info: str) -> None:
    header = r'''\documentclass[]{article}
    \usepackage{hyperref}
    \usepackage{longtable}
    \usepackage{csquotes}
    \usepackage{adjustbox}
    \usepackage{multirow}
    \usepackage{pdflscape}
    \usepackage[margin=0.5in]{geometry}
    \usepackage{todonotes}
    \usepackage{multirow}
    \usepackage{booktabs}


    %opening
    \title{Evaluation}
    \author{Simina Ana Cotop}
    \date{}
    \frenchspacing
    \begin{document}
    \begin{landscape}
    \maketitle
    '''

    footer = r'''
    \end{landscape}
    \end{document}'''

    table = r'''
    \begin{longtable}{|p{20mm}|p{50mm}|p{50mm}|p{50mm}|p{50mm}|}
	\hline
    \multicolumn{5}{|l|}{Script: '''
    table += script.replace("_", "\_")
    table += r''' } \\
	\hline 
    & \multicolumn{3}{|l|}{Beam search} & Nucleus Sampling   \\ 
	\hline 
	& Beam 3 & Beam 5 & Beam 10 &  \\
	\hline
	\endhead '''
    
    table += annons
    #table += repetitions
    table += extra_info

    table += r'''\end{longtable}'''
    
    with open('evaluation.tex', "w") as f:
        f.write(header)
        f.write(table)
        f.write(footer)
    
    commandLine = subprocess.Popen(['pdflatex', 'evaluation.tex'])
    commandLine.communicate()

    os.unlink('evaluation.aux')
    os.unlink('evaluation.log')
    os.unlink('evaluation.out')
    os.unlink('evaluation.tex')



if __name__ == '__main__':
    script: str = sys.argv[1]
    proc_script: List[str] = script.split("_")
    epochs: List[int] = [10, 20, 50, 100, 200]
    beams: List[str] = ['3', '5', '10']
    # TODO: give a list of scripts as argument, and call each of the following functions on each script
    script_folders = parse_output(script)
    epoch_dict = get_dictionary(script_folders, epochs, beams)
    annons = generate_eval_annotations(epoch_dict)
    #count_repetitions(epoch_dict)
    #repetitions = generate_eval_repetitions(epoch_dict)
    chrt_inf, chrt_vals = parse_chart_info(script)
    #count_extra_info(epoch_dict, chrt_inf, chrt_vals, proc_script)
    extra_info = generate_eval_extra_info(epoch_dict)
    #generate_table_latex(script, annons, repetitions,extra_info)
    generate_table_latex(script, annons, extra_info)