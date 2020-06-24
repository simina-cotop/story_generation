# What I did run:
# 1. For chartssentb 
# 2. For chartssenta 


from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import numpy as np
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
        #bleu_score = re.search(r"BLEU = (.+?),", bleu_out).group(1)
        matches = re.search(r"BLEU = (.+?), (.+?)/(.+?)/(.+?)/(.+?)", bleu_out)
        bleu_score1 = float(matches.group(2))
        bleu_score2 = float(matches.group(3))
        bleu_score3 = float(matches.group(4))
        bleu_score4 = float(matches.group(5))
        avg = (bleu_score1 + bleu_score2 + bleu_score3 + bleu_score4) / 4
        #print(bleu_score)
        return avg

    except subprocess.CalledProcessError as error:
      if error.output is not None:
        msg = error.output.strip()
        tf.logging.warning(
            "{} script returned non-zero exit code: {}".format(bleu_script, msg))
      return None


def get_gold_text() -> List[str]:
    all_chart_descs: List[str] = []
    filename = '../../../../few_shot_appendix/data_release/chartssenta/original_data/chartssenta.summary' 
    with open(filename, 'r') as gold:
        inline = gold.readline()
        while inline != '':
            all_chart_descs.append(inline.replace("\n", ""))
            inline = gold.readline()
    #pprint(all_chart_descs)
    #print(len(all_chart_descs))
    return all_chart_descs


def bleu_gold_chartssenta() -> List[List[float]]:
    bleu_results: List[List[float]] = []
    # Compare 10 original descriptions with only one generated one at a time
    path_to_gen: str = '/mnt/Backup/simina/output_final_folder/20200618114823/chartssenta/results/loads/8/valid/'
    for orig_idx in range(10):
        interm_results: List[float] = []
        for gen_idx in range(0,5):
            gen_idx = orig_idx * 5 + gen_idx
            interm_results.append(bleu_score(f'desc_sent_{orig_idx}', f'{path_to_gen}valid_pred_summary_{gen_idx}'))
        bleu_results.append(interm_results)
    pprint(bleu_results)
    return bleu_results

def bleu_gold_chartssentb() -> List[List[float]]:
    bleu_results: List[List[float]] = []
    # Compare 10 original descriptions with only one generated one at a time
    path_to_gen: str = '/mnt/Backup/simina/output_final_folder/20200619230445/chartssentb/results/loads/25/valid/'
    for orig_idx in range(10):
        interm_results: List[float] = []
        for gen_idx in range(0,5):
            gen_idx = orig_idx * 5 + gen_idx
            interm_results.append(bleu_score(f'desc_sent_{orig_idx}', f'{path_to_gen}valid_pred_summary_{gen_idx}'))
        bleu_results.append(interm_results)
    pprint(bleu_results)
    return bleu_results


#TODO: the input list has a different type now, so I have to update that too
def plot_bleu_gold_chartssenta(results: List[List[float]]) -> None:
    plt.clf()
    bars1: List[float] = []
    bars2: List[float] = []
    bars3: List[float] = []
    bars4: List[float] = []
    bars5: List[float] = []
    for chart_list in results:
        bars1.append(chart_list[0])
        bars2.append(chart_list[1])
        bars3.append(chart_list[2])
        bars4.append(chart_list[3])
        bars5.append(chart_list[4])
    
    barWidth = 1/(5 + 3)
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    plt.figure(figsize=(9, 5))
    # !!! We generate 5 sentences for EACH chart
    plt.bar(r1, bars1, width=barWidth, edgecolor='white', label='Sentence1')
    plt.bar(r2, bars2, width=barWidth, edgecolor='white', label='Sentence2')
    plt.bar(r3, bars3, width=barWidth, edgecolor='white', label='Sentence3')
    plt.bar(r4, bars4, width=barWidth, edgecolor='white', label='Sentence4')
    plt.bar(r5, bars5, width=barWidth, edgecolor='white', label='Sentence5')
    plt.legend()
    plt.xlabel('Charts')
    plt.xticks(r1+5*barWidth/2.5, ['Chart1', 'Chart2', 'Chart3', 'Chart4', 'Chart5','Chart6', 'Chart7', 'Chart8', 'Chart9', 'Chart10'])
    plt.xlim(0-(0.4-3*barWidth/2),len(bars1)-(0.4-3*barWidth/2))
 
    plt.ylabel(f"BLEU Average Score")
    plt.title(f"BLEU Average Score for SentA Representation")
    plt.savefig("blue_senta.pdf", bbox_inches="tight")


def plot_bleu_gold_chartssentb(results: List[List[float]]) -> None:
    plt.clf()
    
    bars1: List[float] = []
    bars2: List[float] = []
    bars3: List[float] = []
    bars4: List[float] = []
    bars5: List[float] = []
    for chart_list in results:
        bars1.append(chart_list[0])
        bars2.append(chart_list[1])
        bars3.append(chart_list[2])
        bars4.append(chart_list[3])
        bars5.append(chart_list[4])
    
    barWidth = 1/(5 + 3)
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    plt.figure(figsize=(9, 5))
    plt.bar(r1, bars1, width=barWidth, edgecolor='white', label='Sentence1')
    plt.bar(r2, bars2, width=barWidth, edgecolor='white', label='Sentence2')
    plt.bar(r3, bars3, width=barWidth, edgecolor='white', label='Sentence3')
    plt.bar(r4, bars4, width=barWidth, edgecolor='white', label='Sentence4')
    plt.bar(r5, bars5, width=barWidth, edgecolor='white', label='Sentence5')
    plt.legend()
    plt.xlabel('Charts')
    plt.xticks(r1+5*barWidth/2.5, ['Chart1', 'Chart2', 'Chart3', 'Chart4', 'Chart5','Chart6', 'Chart7', 'Chart8', 'Chart9', 'Chart10'])
    plt.xlim(0-(0.6-3*barWidth/2),len(bars1)-(0.6-3*barWidth/2))
    
    plt.ylabel(f"BLEU Average Score")
    plt.title(f"BLEU Average Score for SentB Representation")
    plt.savefig("blue_sentb.pdf", bbox_inches="tight")



if __name__ == '__main__':
    res_senta = bleu_gold_chartssenta()
    plot_bleu_gold_chartssenta(res_senta)

    res_sentb = bleu_gold_chartssentb()
    plot_bleu_gold_chartssentb(res_sentb)
