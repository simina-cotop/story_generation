from typing import List, Dict, Tuple, NamedTuple
import matplotlib.pyplot as plt
import os
import glob
import csv
from pprint import pprint

plt.rcParams["figure.figsize"] = [15, 10]

# Some type aliases for better readability
class RougeValues(NamedTuple):
    recall: float
    precision: float
    fscore: float
Sentence = Dict[int, Tuple[RougeValues, RougeValues]] # int: 0->9
Chart = Dict[int, Sentence] # int: 0->22
RougeResults = Dict[int, Chart] # int: 0->9

#CHART_chart_SENTENCE_sent_ROUGE-SUX.csv
#CHART_chart_SENTENCE_sent_ROUGE-L.csv

def parse_output_files() -> RougeResults:
    rouge_results: RougeResults = {}
    os.chdir('../summarizer-master/rouge/')
    # files = [file for file in glob.glob("CHART_*.csv")]
    for chart_idx in range(0,10):
        chart: Chart = {}
        for sentence_idx in range(0,23):
            with open("CHART_" + str(chart_idx) + "_SENTENCE_" + str(sentence_idx) + "_ROUGE-SUX.csv", "r") as f:
                reader = csv.DictReader(f)
                rouge_sux = [RougeValues(float(row["recall"]), float(row["precision"]), float(row["f-score"])) for row in reader]
            with open("CHART_" + str(chart_idx) + "_SENTENCE_" + str(sentence_idx) + "_ROUGE-L.csv", "r") as f:
                reader = csv.DictReader(f)
                rouge_l = [RougeValues(float(row["recall"]), float(row["precision"]), float(row["f-score"])) for row in reader]
            sentence: Sentence = {idx: (a, b) for idx, (a, b) in enumerate(zip(rouge_sux, rouge_l))}
            chart[sentence_idx] = sentence
        rouge_results[chart_idx] = chart
    # print(files)
        
    return rouge_results


def plot_rouge(rouge_results: RougeResults) -> None:
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
    #plt.savefig(f"boxplots.png", bbox_inches="tight")
    plt.savefig(f"boxplots.pdf", bbox_inches="tight")

if __name__ == "__main__":
    rouge_results = parse_output_files()
    plot_rouge(rouge_results)

