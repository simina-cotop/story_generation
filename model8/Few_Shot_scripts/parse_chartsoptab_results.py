# What I did run:
# 1. For chartsoptb --> training: on the correct training data, but only 3 validation lines
#                   --> inference: on the 30 validation lines
# 2. For chartsopta --> training: on the correct training data, with 30 validation lines
#                   --> inference: None


from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import numpy as np
import regex as re
import time, os, sys, shutil, io, subprocess, re
from pprint import pprint


def bleu_score(labels_file, predictions_path):
    bleu_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../BLEU/multi-bleu.perl')
    try:
      with io.open(predictions_path, encoding="utf-8", mode="r") as predictions_file:
        bleu_out = subprocess.check_output(
            [bleu_script, labels_file],
            stdin=predictions_file,
            stderr=subprocess.STDOUT)
        bleu_out = bleu_out.decode("utf-8")
        bleu_score = re.search(r"BLEU = (.+?),", bleu_out).group(1)
        matches = re.search(r"BLEU = (.+?), (.+?)/(.+?)/(.+?)/(.+?)", bleu_out)
        bleu_score1 = float(matches.group(2))
        bleu_score2 = float(matches.group(3))
        bleu_score3 = float(matches.group(4))
        bleu_score4 = float(matches.group(5))
        all_bleus = [bleu_score1,bleu_score2,bleu_score3,bleu_score4]
        #print(bleu_score)
        return float(bleu_score), all_bleus

    except subprocess.CalledProcessError as error:
      if error.output is not None:
        msg = error.output.strip()
        tf.logging.warning(
            "{} script returned non-zero exit code: {}".format(bleu_script, msg))
      return None


def get_gold_text() -> List[str]:
    all_chart_descs: List[str] = []
    filename = '../../../../few_shot_appendix/data_release/chartsopta/original_data/chartsopta.summary' 
    with open(filename, 'r') as gold:
        inline = gold.readline()
        while inline != '':
            all_chart_descs.append(inline.replace("\n", ""))
            inline = gold.readline()
    #pprint(all_chart_descs)
    #print(len(all_chart_descs))
    return all_chart_descs


def generate_gold_files() -> None:
    all_chart_descs = get_gold_text()

    # Split the original chart descriptions in 10 chunks (one chunk per chart), each chunk having 23 descriptions
    i: int = 0
    j: int = 23
    index: int = 0
    for idx, desc in enumerate(all_chart_descs):
        while i < 208 and j < 231:
            #print("idx=", idx, "i=", i, "j=", j, "\n")
            current_desc = all_chart_descs[i:j]
            #print(len(current_desc))
            with open(f'desc_chart_{index}', 'w') as desc_file:
                desc_file.write("\n".join(current_desc))
            index += 1
            i += 23
            j += 23   


def bleu_gold_chartsopta() -> List[List[float]]:
    bleu_results: List[List[float]] = []
    # Compare 10 original descriptions with only one generated one at a time
    #path_to_gen: str = '/mnt/Backup/simina/output_files_aws/inference_only_20200628084433/chartsopta/results/test/'
    #path_to_gen: str = '/mnt/Backup/simina/output_new_folder/20200607003751/chartsopta/results/loads/3/valid/'
    path_to_gen: str = '../../../../output_files_aws/20200627223805/chartsopta/results/loads/23/23/valid/'

    for orig_idx in range(10):
        interm_results: List[float] = []
        for gen_idx in range(0,3):
            new_gen_idx = orig_idx * 3 + gen_idx
            #interm_results.append(bleu_score(f'chartsopta/all_gold/opta_test_{orig_idx}_{gen_idx}', f'{path_to_gen}test_pred_summary_{new_gen_idx}'))
            bleu_score, _ = bleu_score(f'chartsopta/all_gold/opta_valid_{orig_idx}_{gen_idx}', f'{path_to_gen}valid_pred_summary_{new_gen_idx}')
            interm_results.append(bleu_score)
        bleu_results.append(interm_results)
    pprint(bleu_results)
    return bleu_results

def bleu_gold_chartsoptb() -> List[List[float]]:
    bleu_results: List[List[float]] = []
    # Compare 10 original descriptions with only one generated one at a time
    #path_to_gen: str = '/mnt/Backup/simina/output_files_aws/inference_only_20200628084549/chartsoptb/results/test/'
    #path_to_gen: str = '/mnt/Backup/simina/output_new_folder/20200606102406/chartsoptb/results/loads/5/valid/'
    path_to_gen: str = 'output_files_aws/20200628011521/chartsoptb/results/loads/23/23/valid/'
    
    for orig_idx in range(10):
        interm_results: List[float] = []
        for gen_idx in range(0,3):
            new_gen_idx = orig_idx * 3 + gen_idx
            #interm_results.append(bleu_score(f'chartsopta/all_gold/opta_test_{orig_idx}_{gen_idx}', f'{path_to_gen}test_pred_summary_{new_gen_idx}'))
            bleu_score, _ =  bleu_score(f'chartsopta/all_gold/opta_valid_{orig_idx}_{gen_idx}', f'{path_to_gen}valid_pred_summary_{new_gen_idx}')
            interm_results.append(bleu_score)
        bleu_results.append(interm_results)
    pprint(bleu_results)
    return bleu_results



def plot_bleu_gold_chartsopta(results: List[List[float]]) -> None:
    plt.clf()
    bars1: List[float] = []
    bars2: List[float] = []
    bars3: List[float] = []
    for chart_list in results:
        bars1.append(chart_list[0])
        bars2.append(chart_list[1])
        bars3.append(chart_list[2])
    
    barWidth = 0.25
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    plt.figure(figsize=(8, 4.5))
    plt.bar(r1, bars1, width=barWidth, edgecolor='white', label='Sentence1')
    plt.bar(r2, bars2, width=barWidth, edgecolor='white', label='Sentence2')
    plt.bar(r3, bars3, width=barWidth, edgecolor='white', label='Sentence3')
    plt.legend()
    plt.xlabel('Charts')
    plt.xticks(r1+3*barWidth/3., ['Chart1', 'Chart2', 'Chart3', 'Chart4', 'Chart5','Chart6', 'Chart7', 'Chart8', 'Chart9', 'Chart10'])
    plt.xlim(0-(0.4-3*barWidth/2),len(bars1)-(0.4-3*barWidth/2))
 
    plt.ylabel(f"BLEU Score")
    plt.title(f"BLEU Score for OptA Representation")
    #plt.savefig("blue_opta_test.pdf", bbox_inches="tight")
    plt.savefig("blue_opta_valid.pdf", bbox_inches="tight")


def plot_bleu_gold_chartsoptb(results: List[List[float]]) -> None:
    plt.clf()
    
    bars1: List[float] = []
    bars2: List[float] = []
    bars3: List[float] = []
    for chart_list in results:
        bars1.append(chart_list[0])
        bars2.append(chart_list[1])
        bars3.append(chart_list[2])
    
    barWidth = 0.25
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    plt.figure(figsize=(8, 4.5))
    plt.bar(r1, bars1, width=barWidth, edgecolor='white', label='Sentence1')
    plt.bar(r2, bars2, width=barWidth, edgecolor='white', label='Sentence2')
    plt.bar(r3, bars3, width=barWidth, edgecolor='white', label='Sentence3')
    plt.legend()
    plt.xlabel('Charts')
    plt.xticks(r1+3*barWidth/3., ['Chart1', 'Chart2', 'Chart3', 'Chart4', 'Chart5','Chart6', 'Chart7', 'Chart8', 'Chart9', 'Chart10'])
    plt.xlim(0-(0.6-3*barWidth/2),len(bars1)-(0.6-3*barWidth/2))
    
    plt.ylabel(f"BLEU Score")
    plt.title(f"BLEU Score for OptB Representation")
    #plt.savefig("blue_optb_test.pdf", bbox_inches="tight")
    plt.savefig("blue_optb_valid.pdf", bbox_inches="tight")



if __name__ == '__main__':
    generate_gold_files()

    res_opta = bleu_gold_chartsopta()
    plot_bleu_gold_chartsopta(res_opta)

    res_optb = bleu_gold_chartsoptb()
    plot_bleu_gold_chartsoptb(res_optb)
