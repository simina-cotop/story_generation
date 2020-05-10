from __future__ import annotations
from collections import OrderedDict
from typing import List, Dict, Tuple, Set, Iterable
from dataclasses import dataclass
from nltk.corpus import stopwords
import os
import sys
import glob
import re
import subprocess
import spacy
import numpy as np
import matplotlib.pyplot as plt


nlp = spacy.load('en')
delexicalization: List[str] = ["NUMBER_HIGHEST", "NUMBER_LEAST", "NUMBER_SCND", "NUMBER_3RD", "NUMBER_4TH", "X_AXIS_HIGHEST", "X_AXIS_LEAST", "X_AXIS_SCND", "X_AXIS_3RD", "X_AXIS_4TH"]
delexicalization_lower: List[str] = [word.lower() for word in delexicalization]


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

    def __str__(self: "Description") -> str:
        return f"{self.length} {self.text} {self.number_of_annotations}\n"

    def count_delexicalizations(self: "Description") -> None:
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
            added: bool = True
            for delexi in delexicalization_lower:
                if delexi in entity.text:
                    added = False
                    break
            if entity.text in chrt_vals:
                added = False 
            if ("<" in entity.text) or (">" in entity.text):
                added = False
            if added == True:        
                self.ner_text.append(entity.text)




        
        
        
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
def generate_eval_annotations(dic: OrderedDict[int, OrderedDict[str, List[Description]]]) -> Tuple[str, Dict[int, Dict[str, List[int]]]]:
    row: str = r'''\multicolumn{5}{|l|}{\textbf{Annotations}  } \\ \hline'''
    # epochs, algorithm, List with index being annotation count and value being the count of descriptions
    annotations_per_config: Dict[int, Dict[str, List[int]]] = {}

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
                    #print(description)
                    if description.number_of_annotations != 0:
                        annotation_counter += 1
                        # Count how many annotations each text has 
                        annotations[description.number_of_annotations] += 1
                annotations_per_config.setdefault(ep, {})[algo] = annotations

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
    return row, annotations_per_config

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



def get_training_data_info() -> Tuple[Dict[str, Dict[str, List[str]]], Dict[str, List[str]]]:
    os.chdir('charts_info')

    training_data_info: Dict[str, Dict[str, List[str]]] = {}
    training_data_values: Dict[str, List[str]] = {}
    
    files = [file for file in glob.glob("*.txt")]
    for fil in files:
        training_data_info[fil] = {}
        training_data_values[fil] = []


    for chart_file in training_data_info:
        chart_info : Dict[str, List[str]] = {}
        chart_actual_values: List[str] = []
        with open(chart_file,'r') as f:
            data = f.read()
        lines = data.split("\n")
        # Kick out all the non-label info (for now)
        lines = lines[:7]
        # Kick out the title
        lines = lines[1:]
        for line in lines:
            aux = line.split(" : ")
            # Category
            processed_aux: str = aux[1].lower()
            # Actual values
            processed_aux = processed_aux.split(", ")
            chart_info[aux[0]] = processed_aux
        # Save only the values in a list
        for value in chart_info.values():
            for el in value:
                chart_actual_values.append(el)
        training_data_info[chart_file] = chart_info
        training_data_values[chart_file] = chart_actual_values
    
    # Print dictionaries
    '''for chart_file in training_data_info:
        print(chart_file)
        for key,val in training_data_info[chart_file].items():
            print(key, val)
        print(training_data_values[chart_file])
        print("\n")
    print("\n\n")'''
    os.chdir('..')
    return training_data_info, training_data_values

    
# Step 3: check if the script appears (TODO: or anything else that was not caught before)
def count_extra_info(info_script: str, all_chrt_vals: Dict[str, List[str]], desc: Description) -> Tuple[int, bool, List[str]]:
    counter_wrong_info: int = 0
    wrong_info: List[str] = []
    has_wrong_info: bool = False
    # If description.text in other_script.description.text -> print and count
    for word in desc.no_punc_desc:
        for chart_file in all_chrt_vals:
            if chart_file != info_script:
                if word in all_chrt_vals[chart_file] and word not in all_chrt_vals[info_script]:
                    #print("vals=", all_chrt_vals[info_script])
                    #print("w=", word)
                    counter_wrong_info += 1
                    has_wrong_info = True
                    wrong_info.append(word)
    return counter_wrong_info, has_wrong_info, wrong_info


# 3. Count how much information appears in the description that is not in the chart
def generate_eval_extra_info(dic: OrderedDict[int, OrderedDict[str, List[Description]]], info_script: str, all_chrt_vals: Dict[str, List[str]]) -> Tuple[str, OrderedDict[int, List[Tuple[str, int]]], OrderedDict[int, List[Tuple[str, int]]]]:
    row: str = r'''
        \multicolumn{5}{|l|}{\textbf{Extra or wrong information}  } \\ \hline
        \multicolumn{5}{|l|}{\textbf{1. Delexicalization}  } \\ \hline
        \multicolumn{5}{|l|}{\textbf{2. Wrong information}  } \\ \hline
    '''
    all_delexi_counts: OrderedDict[int, List[Tuple[str, int]]] = OrderedDict()
    all_wrong_info_counts: OrderedDict[int, List[Tuple[str, int]]] = OrderedDict()
    # For each epoch
    for ep in dic:
        #print("ep=", ep)
        row_head: str = str(ep) + ' epochs &'
        delexi_result: List[str] = []
        wrong_info_result: List[str] = []
        all_delexi_counts[ep] = []
        all_wrong_info_counts[ep] = []
        # algo: keys in dic[ep], i.e. either beam+number or nucleus
        for algo in dic[ep]:
                #print("algo=", algo)
                description_list: List[Description] = dic[ep][algo]
                #print("len=", len(description_list))

                delexi_counter: int = 0
                ner_counter: int = 0
                wrong_info_counter: int = 0
                # Set of strings for ALL descriptions
                all_delexis: Set[str] = set()
                all_ners: Set[str] = set()
                all_wrong_info: Set[str] = set()
                
                for description in description_list:
                    # 1. Count how many texts contain delexicalizations
                    description.count_delexicalizations()
                    if description.delexi != []:
                        delexi_counter += 1
                        for el_delexi in description.delexi:
                            all_delexis.add(el_delexi)
                        #print("all_delexi=", all_delexis, delexi_counter)

                    # 2. Count NERs
                    '''description.count_ners(chrt_vals)
                    if description.ner_text != []:
                        ner_counter += 1
                        for el_ner in description.ner_text:
                            all_ners.add(el_ner)
                        print("all_ners=", all_ners, ner_counter)'''
                    # 2. Count the extra information    
                    counter_wrong_info, has_wong_info, wrong_info = count_extra_info(info_script, all_chrt_vals, description)
                    if has_wong_info == True:
                        wrong_info_counter += 1
                    for info in wrong_info:
                        all_wrong_info.add(info)
                #print(all_wrong_info)

                all_delexi_counts[ep].append((algo, delexi_counter))
                all_wrong_info_counts[ep].append((algo, wrong_info_counter))
                #print("all=", all_delexi_counts)
                # Turn the results into strings
                delexi_result.append("There are " + str(delexi_counter) + " delexcalization symbols: " + ", ".join(el.replace("_", "\_") for el in all_delexis))
                #print("res=",delexi_result)
                wrong_info_result.append("There are " + str(wrong_info_counter) + " wrong words: " + ", ".join(el for el in all_wrong_info))
                #print("res=",wrong_info_result)
        row_delexi: str = " & ".join(x for x in delexi_result) + "\\\\ \\hline \n"
        #print("HERE\n")
        row_wrong_info: str = " & ".join(x for x in wrong_info_result) + "\\\\ \\hline \n"
        row += row_head + row_delexi + row_head + row_wrong_info
        #print(row)
    return row, all_delexi_counts, all_wrong_info_counts



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


def plot_delexi(delexis: OrderedDict[int, List[Tuple[str, int]]]) -> None:
    plt.clf()
    #print(delexis)
    all_vals: OrderedDict[str, List[int]] = OrderedDict()

    for key, values in delexis.items():
        for val in values:
            all_vals.setdefault(val[0], []).append(val[1])
    #print("all_vals=", all_vals)
    num_epoch = len(all_vals['3'])
    num_algos = len(all_vals)
    plt.bar(range(0, (num_algos+1)*num_epoch, num_algos+1), all_vals['3'], label="Beam 3")
    plt.bar(range(1, (num_algos+1)*num_epoch, num_algos+1), all_vals['5'], label="Beam 5")
    plt.bar(range(2, (num_algos+1)*num_epoch, num_algos+1), all_vals['10'], label="Beam 10")
    plt.bar(range(3, (num_algos+1)*num_epoch, num_algos+1), all_vals['nucleus'], label="Nucleus Sampling")

    plt.ylim(0, 40)
    plt.xlabel("Epochs")
    plt.ylabel("Number of descriptions containing any delexicalization symbol")
    plt.xticks(np.arange(num_algos/2-.5, (num_algos+1)*num_epoch, num_algos+1), ["10", "20", "50", "100", "200"])
    plt.title(f"Delexicalization")
    plt.legend()
    plt.savefig("delexi.pdf", bbox_inches="tight")

def plot_wrong_info(wrong_info: OrderedDict[int, List[Tuple[str, int]]]) -> None:
    plt.clf()
    #print(delexis)
    all_vals: OrderedDict[str, List[int]] = OrderedDict()

    for key, values in wrong_info.items():
        for val in values:
            all_vals.setdefault(val[0], []).append(val[1])
    #print("all_vals=", all_vals)
    num_epoch = len(all_vals['3'])
    num_algos = len(all_vals)
    plt.bar(range(0, (num_algos+1)*num_epoch, num_algos+1), all_vals['3'], label="Beam 3")
    plt.bar(range(1, (num_algos+1)*num_epoch, num_algos+1), all_vals['5'], label="Beam 5")
    plt.bar(range(2, (num_algos+1)*num_epoch, num_algos+1), all_vals['10'], label="Beam 10")
    plt.bar(range(3, (num_algos+1)*num_epoch, num_algos+1), all_vals['nucleus'], label="Nucleus Sampling")

    plt.ylim(0, 40)
    plt.xlabel("Epochs")
    plt.ylabel("Number of descriptions containing words from the training data")
    plt.xticks(np.arange(num_algos/2-.5, (num_algos+1)*num_epoch, num_algos+1), ["10", "20", "50", "100", "200"])
    plt.title(f"Wrong information")
    plt.legend()
    plt.savefig("wrong_info.pdf", bbox_inches="tight")

def plot_annotations(annotations_per_config: Dict[int, Dict[str, List[int]]]) -> None:
    plt.clf()

    all_vals: Dict[str, Dict[int, List[int]]] = {}
    for epoch, values in annotations_per_config.items():
        for algo, vals in values.items():
            all_vals.setdefault(algo, {})[epoch] = np.cumsum([0] + vals)

    max_annotations = len(next(iter(next(iter(all_vals.values())).values())))
    num_epoch = len(next(iter(all_vals.values())))
    num_algos = len(all_vals)
    colors = ["r", "g", "b", "orange"]
    hatches = [" ", "//", "\\\\", "*", "-", "o", "|", "O"]

    for i in range(1, min(max_annotations, len(hatches)+1)):
        def plot_bar(values: Iterable[List[int]], offset: int, idx: int, label: str) -> None:
            bottom = np.array([x[idx-1] for x in values])
            value = np.array([x[idx] for x in values])
            height = value-bottom
            args = {}
            if idx == 1:
                args["label"] = label
            plt.bar(
                range(offset, (num_algos+1)*num_epoch, num_algos+1),
                height=height,
                bottom = bottom,
                color = colors[offset],
                alpha = .5 if idx % 2 == 0 else 1,
                hatch = hatches[idx-1],
                **args
            )

        plot_bar(all_vals['3'].values(), 0, i, "Beam 3")
        plot_bar(all_vals['5'].values(), 1, i, "Beam 5")
        plot_bar(all_vals['10'].values(), 2, i, "Beam 10")
        plot_bar(all_vals['nucleus'].values(), 3, i, "Nucleus Sampling")

    plt.ylim(0, 40)
    plt.xlabel("Epochs")
    plt.ylabel("Number of annotations")
    plt.xticks(np.arange(num_algos/2-.5, (num_algos+1)*num_epoch, num_algos+1), ["10", "20", "50", "100", "200"])
    plt.title(f"Annotations")
    plt.legend()
    plt.savefig("annotations.pdf", bbox_inches="tight")


if __name__ == '__main__':
    script: str = sys.argv[1]
    proc_script: List[str] = script.split("_")
    info_script = "info_" + script + ".txt"
    epochs: List[int] = [10, 20, 50, 100, 200]
    beams: List[str] = ['3', '5', '10']
    # TODO: give a list of scripts as argument, and call each of the following functions on each script
    script_folders = parse_output(script)
    epoch_dict = get_dictionary(script_folders, epochs, beams)
    annons, annotations_per_config = generate_eval_annotations(epoch_dict)
    #count_repetitions(epoch_dict)
    #repetitions = generate_eval_repetitions(epoch_dict)
    training_data_inf, training_data_vals = get_training_data_info()
    chrt_inf: Dict[str, List[str]] = training_data_inf[info_script]
    chrt_vals: List[str] = training_data_vals[info_script]
    print("chrt_inf", chrt_inf)
    print("chrt_vals", chrt_vals)
    #extra_info = count_extra_info(script, chrt_inf, chrt_vals)
    row_extra_info, delexis, extra_info = generate_eval_extra_info(epoch_dict, info_script, training_data_vals)
    plot_delexi(delexis)
    plot_wrong_info(extra_info)
    plot_annotations(annotations_per_config)
    #generate_table_latex(script, annons, repetitions,extra_info)
    #generate_table_latex(script, annons, row_extra_info)