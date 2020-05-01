from typing import List, Dict
import os
import sys
import glob
import re
import subprocess


def parse_output(script:str) -> List[str]:
    dirs = os.listdir("outputs")
    dirs_script = [d for d in dirs if script in d]
    return dirs_script

def print_dictionary(dic: Dict[int, Dict[str, List[str]]]) -> None:
    for ep in dic:
        print("ep=",ep,'\n')
        for beam in dic[ep]:
            print("beam=",beam,'\n')
            l = dic[ep][beam]
            print(l[:5],'\n\n')
        print('\n\n')

def get_dictionary(script_folders: List[str], epochs: List[int], beams: List[str]) -> Dict[int, Dict[str, List[str]]]:
    epoch_dict: Dict[int, Dict[str, List[str]]] = {}
    for epoch in epochs:
        epoch_dict[epoch] = {}
        epoch_folders: List[str] = [fol for fol in script_folders if str(epoch) + 'epochs' in fol]
        for beam in beams:
            for current_folder in epoch_folders:
                if beam in current_folder:
                    filename: str = 'samples_' + current_folder
                    newer_data: List[str] = []
                    with open('outputs/' + current_folder + '/' + filename) as f:
                        data: str = f.read()
                        # Remove the epoch-related information
                        data = data.split('===============================')[0]
                        new_data = re.split('-- TEXT [\d]* ---', data)
                        # Remove script name
                        new_data = new_data[1:]
                        # Remove '\n'
                        for el in new_data:
                            el = el.replace('\n', ' ')
                            newer_data.append(el)
                    epoch_dict[epoch][beam]= newer_data[:10]
                elif 'nucleus' in current_folder:
                    nfilename: str = 'samples_' + current_folder
                    nnewer_data: List[str] = []
                    with open('outputs/' + current_folder + '/' + nfilename) as f:
                        ndata: str = f.read()
                        # Remove the epoch-related information
                        ndata = ndata.split('===============================')[0]
                        nnew_data = re.split('-- TEXT [\d]* ---', ndata)
                        # Remove script name
                        nnew_data = nnew_data[1:]
                        # Remove '\n'
                        for el in nnew_data:
                            el = el.replace('\n', ' ')
                            nnewer_data.append(el)
                    epoch_dict[epoch]['nucleus']= nnewer_data[:10]

    print_dictionary(epoch_dict)
    return epoch_dict
    
def generate_table_content(dic: Dict[int, Dict[str, List[str]]]) -> str:
    row: str = 

    for ep in dic:
        row_head: str = str(ep) + ' epochs &'
        row_values: List[int] = []
        for el in dic[ep]:
            l = dic[ep][el]
            row_values.append(len(l))

    row_middle = " & ".join(str(x) for x in row_values) + "\\\\ \\hline \n"
    row += row_head + row_middle
    return row

def generate_table_latex(script:str, content: str) -> None:
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
    \begin{longtable}{|p{17mm}|p{45mm}|p{45mm}|p{45mm}|p{45mm}|}
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
    
    table += content

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
    epochs: List[int] = [10, 20, 50, 100, 200]
    beams: List[str] = ['3', '5', '10']
    # TODO: give a list of scripts as argument, and call each of the following functions on each script
    script_folders = parse_output(script)
    epoch_dict = get_dictionary(script_folders, epochs, beams)
    content = generate_table_content(epoch_dict)
    generate_table_latex(script, content)