from typing import List, Dict, Tuple, NamedTuple
import matplotlib.pyplot as plt
import os
import glob
import csv
from pprint import pprint
from natsort import natsorted

plt.rcParams["figure.figsize"] = [15, 10]

# Some type aliases for better readability
class RougeValues(NamedTuple):
    recall: float
    precision: float
    fscore: float
GPT2Sentence = Dict[int, Tuple[RougeValues, RougeValues]] # int: 0->9
GPT2Chart = Dict[int, GPT2Sentence] # int: 0->22
GPT2RougeResults = Dict[int, GPT2Chart] # int: 0->9

SelfConfiguration = Dict[int, Tuple[RougeValues, RougeValues]] # int: 0 -> 39
SelfRougeResults = Dict[Tuple[str, int], SelfConfiguration] # str is for algo, int is for epoch


#CHART_chart_SENTENCE_sent_ROUGE-SUX.csv
#CHART_chart_SENTENCE_sent_ROUGE-L.csv
def parse_output_files() -> GPT2RougeResults:
    rouge_results: GPT2RougeResults = {}
    for chart_idx in range(0,10):
        chart: GPT2Chart = {}
        for sentence_idx in range(0,23):
            with open("../summarizer-master/rouge/gpt2_results_OUTPUTS/CHART_" + str(chart_idx) + "_SENTENCE_" + str(sentence_idx) + "_ROUGE-SUX.csv", "r") as f:
                reader = csv.DictReader(f)
                rouge_sux = [RougeValues(float(row["recall"]), float(row["precision"]), float(row["f-score"])) for row in reader]
            with open("../summarizer-master/rouge/gpt2_results_OUTPUTS/CHART_" + str(chart_idx) + "_SENTENCE_" + str(sentence_idx) + "_ROUGE-L.csv", "r") as f:
                reader = csv.DictReader(f)
                rouge_l = [RougeValues(float(row["recall"]), float(row["precision"]), float(row["f-score"])) for row in reader]
            sentence: GPT2Sentence = {idx: (a, b) for idx, (a, b) in enumerate(zip(rouge_sux, rouge_l))}
            chart[sentence_idx] = sentence
        rouge_results[chart_idx] = chart
    return rouge_results


# CHART_BEAM5_20EPOCHS_ROUGE-SUX.csv 
# CHART_BEAM5_20EPOCHS_ROUGE-L.csv 
def parse_output_files_self() -> SelfRougeResults:
    #os.chdir('../summarizer-master/rouge/')
    rouge_results: SelfRougeResults = {}
    for algo in ['BEAM3', 'BEAM5', 'BEAM10', 'NUCLEUS']:
        for epoch in [10, 20, 50, 100, 200]:
            with open(f"../summarizer-master/rouge/CHART_{algo}_{epoch}EPOCHS_ROUGE-SUX.csv", "r") as f:
                reader = csv.DictReader(f)
                rouge_sux = [RougeValues(float(row["recall"]), float(row["precision"]), float(row["f-score"])) for row in reader]
            with open(f"../summarizer-master/rouge/CHART_{algo}_{epoch}EPOCHS_ROUGE-L.csv", "r") as f:
                reader = csv.DictReader(f)
                rouge_l = [RougeValues(float(row["recall"]), float(row["precision"]), float(row["f-score"])) for row in reader]
            sentence: SelfConfiguration = {idx: (a, b) for idx, (a, b) in enumerate(zip(rouge_sux, rouge_l))}
            rouge_results[(algo, epoch)] = sentence
    return rouge_results



def plot_rouge_gpt2(rouge_results: GPT2RougeResults) -> None:
    def accessor(x: RougeValues) -> float:
        return x.precision

    for chart_name, chart in rouge_results.items():
        plt.clf()

        vals = [[accessor(values[0]) for values in sentence.values()] for sentence in chart.values()]
        positions = list(chart.keys())
        plt.boxplot(vals, positions=positions, labels=list(map(str, chart.keys())))

        plt.vlines(len(vals), 0, 1)

        vals = [[accessor(values[1]) for values in sentence.values()] for sentence in chart.values()]
        positions = list(map(lambda x: x+len(vals)+1, chart.keys()))
        plt.boxplot(vals, positions=positions, labels=list(map(str, chart.keys())))

        plt.ylim(0, 0.6)
        plt.xlabel("Original Sentence (left SUX / right L)")
        plt.ylabel("Rouge Score")
        plt.title(f"Rouge Score for Chart {chart_name}")
        #plt.savefig(f"boxplot{chart_name}.png", bbox_inches="tight")
        plt.savefig(f"boxplot{chart_name}.pdf", bbox_inches="tight")

    plt.clf()

    vals = [[accessor(values[0]) for sentence in chart.values() for values in sentence.values()] for chart in rouge_results.values()]
    positions = list(rouge_results.keys())
    plt.boxplot(vals, positions=positions, labels=list(map(str, rouge_results.keys())))

    plt.vlines(len(vals), 0, 1)

    vals = [[accessor(values[1]) for sentence in chart.values() for values in sentence.values()] for chart in rouge_results.values()]
    positions = list(map(lambda x: x+len(vals)+1, rouge_results.keys()))
    plt.boxplot(vals, positions=positions, labels=list(map(str, rouge_results.keys())))

    plt.ylim(0, 0.6)
    plt.xlabel("Chart (left SUX / right L)")
    plt.ylabel("Rouge Score")
    plt.title(f"Rouge Scores")
    plt.savefig(f"boxplots.pdf", bbox_inches="tight")

    

# Generate plot for Rouge-SUX
def plot_rouge_self_sux(rouge_results: SelfRougeResults, gpt_rouge_results: GPT2RougeResults) -> None:
    def accessor(x: RougeValues) -> float:
        return x.fscore

    # aggregate the data based on algo, such that each algo can have a single color for all epochs
    data_per_algo :Dict[str, List[Tuple[int, SelfConfiguration]]]= {}
    for (algo, epoch), value in rouge_results.items():
        data_per_algo.setdefault(algo, list()).append((epoch, value))
    # sort the inner lists of the data_per_algo
    for (key,values) in data_per_algo.items():
        values.sort(key=lambda x: x[0])

    colors = ["pink", "lightblue", "lightgreen", "wheat"]

    for rouge_index, rouge_type in [(0, "SUX"), (1, "L")]:
        # Clear any existing plot data
        plt.clf()
        # Entries are sorted, such that all algo are in order
        for offset, (algo, data) in enumerate(natsorted(data_per_algo.items())):
            epochs = [epoch for epoch, _vals in data]
            vals = [[accessor(val[rouge_index]) for val in values.values()] for _epoch, values in data]
            positions = list(range(offset, len(data)*(len(data_per_algo)+1), len(data_per_algo)+1))
            if offset == 1:
                labels = [f"{algo.replace('BEAM', 'B').replace('NUCLEUS', 'NS')}\n {epoch} Epochs " for epoch in epochs]
            else:
                labels = [f"{algo.replace('BEAM', 'B').replace('NUCLEUS', 'NS')}" for epoch in epochs]
            bplots = plt.boxplot(vals,
                # x positions
                positions=positions,
                # x labels
                labels=labels,
                # for coloring
                patch_artist=True
            )
            for box in bplots['boxes']:
                box.set_facecolor(colors[offset])

        gpt_positions = (len(data_per_algo) + 1) * len(next(iter(data_per_algo.values())))
        vals2 = [accessor(values[rouge_index]) for sentences in gpt_rouge_results[4].values() for values in sentences.values()]
        plt.boxplot([vals2, []], positions=[gpt_positions, -100], labels=["GPT-2", ""])
        
        if rouge_index == 0:
            plt.ylim(0, 0.4)
            plt.vlines(gpt_positions-1, 0, 0.4)
        else:
            plt.ylim(0, 0.7)
            plt.vlines(gpt_positions-1, 0, 0.7)
        plt.xlim(left=-0.5)
        plt.xlabel("Algorithm and epoch configuration")
        plt.ylabel(f"ROUGE-{rouge_type} Score")
        plt.title(f"ROUGE-{rouge_type} Score for the gender_pay_gap chart")
        plt.savefig(f"ROUGE-{rouge_type}_boxplot.pdf", bbox_inches="tight")
        #plt.savefig("/tmp/123tmp_boxplot.pdf", bbox_inches="tight")

    

if __name__ == "__main__":
    gpt_rouge_results = parse_output_files()
    self_rouge_results = parse_output_files_self()
    #plot_rouge_gpt2(rouge_results)
    plot_rouge_self_sux(self_rouge_results, gpt_rouge_results)

