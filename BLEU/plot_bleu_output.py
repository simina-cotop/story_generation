from typing import List, Dict, Tuple, NamedTuple
import matplotlib.pyplot as plt
import os
import glob
import csv
from pprint import pprint
from natsort import natsorted
from run_and_plot_bleu import create_bleu_output

plt.rcParams["figure.figsize"] = [15, 10]

# Some type aliases for better readability
GPT2Sentence = List[Tuple[int, float]] # int: 0->9
GPT2Chart = Dict[int, GPT2Sentence] # int: 0->22
GPT2Results = Dict[int, GPT2Chart] # int: 0->9

BleuConfig = List[Tuple[int, float]] # int: 0 -> 39
BleuResults = Dict[Tuple[str, int], BleuConfig] # str is for algo, int is for epoch

bleu_results, gpt_bleu_results = create_bleu_output()





'''def plot_rouge_gpt2(rouge_results: GPT2RougeResults) -> None:
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
    plt.savefig(f"boxplots.pdf", bbox_inches="tight")'''

    

# Generate plot for Rouge-SUX
def plot_bleu_algos(bleu_results: BleuResults) -> None:

    # aggregate the data based on algo, such that each algo can have a single color for all epochs
    data_per_algo :Dict[str, List[Tuple[int, BleuConfig]]]= {}
    for (algo, epoch), value in bleu_results.items():
        data_per_algo.setdefault(algo, list()).append((epoch, value))
    # sort the inner lists of the data_per_algo
    for (key,values) in data_per_algo.items():
        values.sort(key=lambda x: x[0])
    #print(data_per_algo)


    colors = ["pink", "lightblue", "lightgreen", "wheat"]

    # Clear any existing plot data
    plt.clf()
    # Entries are sorted, such that all algo are in order
    for offset, (algo, data) in enumerate(natsorted(data_per_algo.items())):
        epochs = [epoch for epoch, _vals in data]
        vals = [[val[1] for val in values] for _epoch, values in data]
        positions = list(range(offset, len(data)*(len(data_per_algo)+1), len(data_per_algo)+1))
        if offset == 1:
            labels = [f"{algo.replace('beam', 'B').replace('nucleus', 'NS')}\n {epoch} Epochs " for epoch in epochs]
        else:
            labels = [f"{algo.replace('beam', 'B').replace('nucleus', 'NS')}" for epoch in epochs]
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

        # GPT-related 
        gpt_positions = (len(data_per_algo) + 1) * len(next(iter(data_per_algo.values())))
        vals2 = [values[1] for sentences in gpt_bleu_results[4].values() for values in sentences]
        plt.boxplot([vals2, []], positions=[gpt_positions, 0], labels=["GPT-2", ""])
        
        plt.ylim(0, 100)
        plt.vlines(gpt_positions-1, -1, 100)
        
        #plt.xlim(left=-0.5)
        plt.ylim(bottom=-1)
        plt.xlabel("Algorithm and epoch configuration")
        plt.ylabel(f"BLEU Score")
        plt.title(f"BLEU Score for the gender_pay_gap chart")
        plt.savefig(f"BLEU_boxplot.pdf", bbox_inches="tight")
        #plt.savefig("/tmp/123tmp_boxplot.pdf", bbox_inches="tight")

    

if __name__ == "__main__":
    #plot_rouge_gpt2(rouge_results)
    plot_bleu_algos(bleu_results)

