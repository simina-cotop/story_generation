import xml.etree.cElementTree as ET
from typing import List, Dict, Tuple, NamedTuple, cast
import matplotlib.pyplot as plt
import os
import glob
import csv
import re
import subprocess
import io
from pprint import pprint

BleuConfig = List[Tuple[int, float]] # int: 0 -> 39
BleuResults = Dict[Tuple[str, int], BleuConfig] # str is for algo, int is for epoch

# Parse .xml file which contains both the human written summaries and the gpt-generated ones
# and output the sentences to a file EACH
def create_human_files():
  summaries = ET.parse('../gpt2/gpt_output.xml').getroot()
  for chart_id, chart in enumerate(summaries):
    if chart.attrib['name'] == 'gender_pay_gap.txt\n':
        for idx, original in enumerate(chart):
          with open(f'output_human_text.txt{idx}', 'w') as g:
            sentence = cast(str, original.text)
            g.write(sentence.casefold())
            # TODO: uncomment this
            """with open('output_gpt_texts.txt', 'w') as h:
              for gpt2 in original:
                  gpt_sent = cast(str,gpt2.text)
                  h.write(gpt_sent.casefold())"""
        


def parse_algo_file(init_filename:str, algo_file_name_part: str, epoch: str) -> None:
    path = f'../model8/outputs/gender_pay_gap_{algo_file_name_part}_{epoch}epochs/{init_filename}'

    with open(path, 'r') as f:
          newer_data: List[str] = []
          data: str = f.read()
          # Remove the epoch-related information
          data = data.split('===============================')[0]
          new_data: List[str] = re.split('\n-- TEXT [\d]+ ---\n', data)
          # Remove script name
          new_data = new_data[1:]

          for idx, el in enumerate(new_data):
              with open(f'output_{algo_file_name_part}_{epoch}epochs_{idx}.txt', 'w') as g:
                el = re.sub(r"\s+", " ", el)
                newer_data.append(el)
                g.write(el.casefold() + "\n")
				




# Taken from util.py from the Few-Shot-NLG project
def bleu_score(labels_file, predictions_path) -> float:
    #bleu_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'multi-bleu.perl')
    bleu_script = os.path.join(os.path.dirname(os.path.realpath(__file__)),'multi-bleu.perl')
    try:
      with io.open(predictions_path, encoding="utf-8", mode="r") as predictions_file:
        bleu_out = subprocess.check_output(
            [bleu_script, labels_file],
            stdin=predictions_file,
            stderr=subprocess.STDOUT)
        bleu_out = bleu_out.decode("utf-8")
        bleu_score = re.search(r"BLEU = (.+?),", bleu_out).group(1)
        #print(bleu_score)
        return float(bleu_score)

    except subprocess.CalledProcessError as error:
      if error.output is not None:
        msg = error.output.strip()
        tf.logging.warning(
            "{} script returned non-zero exit code: {}".format(bleu_script, msg))
      return None


def create_bleu_output() -> BleuResults:
	bleu_results: BleuResults = {}
	for algo, algo_file_name_part in [('beam3', "beam_3"), ('beam5', "beam_5"), ('beam10', "beam_10"), ('nucleus', "nucleus")]:
	#for algo, algo_file_name_part in [('beam3', "beam_3")]:
		for epoch in [10,20,50,100,200]:
			#for epoch in [10]:
			for idx in range(40):
				parse_algo_file(f'samples_gender_pay_gap_{algo_file_name_part}_{epoch}epochs', algo_file_name_part, epoch)
				bs = bleu_score('output_human_text.txt', f'output_{algo_file_name_part}_{epoch}epochs_{idx}.txt')
				#data_per_algo.setdefault(algo, list()).append((epoch, value))
				bleu_results.setdefault((algo, epoch),list()).append((idx, bs))
				if os.path.isfile(f'output_{algo_file_name_part}_{epoch}epochs_{idx}.txt'):
					#print(f'output_{algo_file_name_part}_{epoch}epochs_{idx}.txt') 
					#dir_path = os.path.dirname(os.path.realpath(__file__))
					#print(dir_path)
					os.remove(f'output_{algo_file_name_part}_{epoch}epochs_{idx}.txt')
				else:
					print(f"Error: output_{algo_file_name_part}_{epoch}epochs_{idx}.txt file not found")
	#print(bleu_results)
	return bleu_results


if __name__ == "__main__":
	create_human_files()
	results = create_bleu_output()
	#bleu_score('output_human_text.txt', 'output_gpt_texts.txt')




