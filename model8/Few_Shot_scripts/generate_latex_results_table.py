from parse_chartsoptab_results import bleu_gold_chartsopta, bleu_score
from pprint import pprint
import subprocess


def generate_opta_table() -> None:
	gold_path = 'chartsopta/all_gold/'
	test_path = '../../../../output_files_aws/inference_only_20200628084433/chartsopta/results/test/'
	valid_path = '../../../../output_new_folder/20200607003751/chartsopta/results/loads/3/valid/'

	all_results = bleu_gold_chartsopta()
	print(all_results)

	global_dict = {}
	sent_a_table_header = r'''\section{OptA}

	\begin{longtable}{|p{13mm}|p{57mm}|p{57mm}|p{57mm}|p{57mm}|}
	\hline 
	Chart & Human Description & Test  \\ 
	\hline 
	\endhead'''

	with open(f'chartsoptb/original_data/test.summary', 'r') as test1:

		for orig_idx in range(10):
			global_dict.setdefault(orig_idx, dict())
			row = r'''\multirow{2}{*}{Chart ''' + str(orig_idx) + '}' 
			for gen_idx in range(0,3):

				intermList = global_dict[orig_idx].setdefault(gen_idx, list())
				new_gen_idx = orig_idx * 3 + gen_idx

				gold_text = test1.readline()
				gold_text = gold_text.replace('%','\%')
				gold_text = gold_text.replace('$','\$')
				gold_text = gold_text.replace('\\\\n','')
				intermList.append(gold_text)
				print("gold=",gold_text)

				with open(f'{test_path}test_pred_summary_{new_gen_idx}', 'r') as test2:
					test_score = bleu_score(f'chartsopta/all_gold/opta_test_{orig_idx}_{gen_idx}', f'{test_path}test_pred_summary_{new_gen_idx}')
					print("test_score", test_score)
					test_sent = test2.read()
					test_sent = test_sent.replace('%','\%')
					test_sent = test_sent.replace('$','\$')
					test_sent = test_sent.replace('\\\\n','')
					print("test_sent", test_sent)
					intermList.append(test_sent + "\\newline" + " \\textbf{BLEU Score: }" + str(test_score))
					print("test=",test_sent)
					row += "&" + " & ".join(x for x in intermList) + "\\\\ \\cline{2-5}"
			row += "\\hline"
			sent_a_table_header += row 
	sent_a_table_header += r''' \end{longtable}'''

	
	pprint(global_dict)

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
    \title{Evaluation Appendix}
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


	with open('test.tex', "w") as f:
		f.write(header)
		f.write(sent_a_table_header)
		f.write(footer)
    
	commandLine = subprocess.Popen(['pdflatex', 'test.tex'])
	commandLine.communicate()

    #os.unlink('test.aux')
    #os.unlink('test.log')
    #os.unlink('test.out')
    #os.unlink('test.tex')
		



def generate_sb_table() -> None:
	gold_path = 'chartssenta/all_gold/'
	test_path = '../../../../output_files_aws/inference_only_20200629025149/chartssb/results/test/'
	valid_path = '../../../../output_files_aws/20200628222148/chartssb/results/loads/52/valid/'

	all_results = bleu_gold_chartsopta()
	print(all_results)

	global_dict = {}
	sent_a_table_header = r'''\section{SB}

	\begin{longtable}{|p{13mm}|p{57mm}|p{57mm}|p{57mm}|p{57mm}|}
	\hline 
	Chart & Human Description & Validation & Human Description & Test  \\ 
	\hline 
	\endhead'''

	


	for orig_idx in range(10):
		global_dict.setdefault(orig_idx, dict())
		row = r'''\multirow{2}{*}{Chart ''' + str(orig_idx) + '}' 
		for gen_idx in range(0,3):
			
			intermList = global_dict[orig_idx].setdefault(gen_idx, list())
			new_gen_idx = orig_idx * 3 + gen_idx
			if gen_idx == 0:
				with open(f'chartssentb/original_data/test.summary', 'r') as test1:
					gold_text = test1.readline()
					gold_text = gold_text.replace('%','\%')
					gold_text = gold_text.replace('$','\$')
					gold_text = gold_text.replace('\\\\n','')
					intermList.append(gold_text)
			else:
				intermList.append("")
			with open(f'{test_path}test_pred_summary_{new_gen_idx}', 'r') as test2:
				test_score = bleu_score(f'chartssenta/all_gold/senta_test_{orig_idx}_{gen_idx}', f'{test_path}test_pred_summary_{new_gen_idx}')
				print("test_score", test_score)
				test_sent = test2.read()
				test_sent = test_sent.replace('%','\%')
				test_sent = test_sent.replace('$','\$')
				test_sent = test_sent.replace('\\\\n','')
				print("test_sent", test_sent)
				intermList.append(test_sent + "\\newline" + " \\textbf{BLEU Score: }" + str(test_score))
			if gen_idx == 0:
				with open(f'chartssentb/original_data/valid.summary', 'r') as valid1:
					#gold_text.append(valid1.readline())
					valid_read = valid1.readline()
					valid_read = valid_read.replace('%','\%')
					valid_read = valid_read.replace('$','\$')
					valid_read = valid_read.replace('\\\\n','')
					intermList.append(valid_read)
			else:
				intermList.append("")
			with open(f'{valid_path}valid_pred_summary_{new_gen_idx}', 'r') as valid2:
				valid_score = bleu_score(f'chartssenta/all_gold/senta_valid_{orig_idx}_{gen_idx}', f'{valid_path}valid_pred_summary_{new_gen_idx}')
				valid_sent = valid2.read()
				valid_sent = valid_sent.replace('%','\%')
				valid_sent = valid_sent.replace('$','\$')
				valid_sent = valid_sent.replace('\\\\n','')
				intermList.append(valid_sent + "\\newline" + " \\textbf{BLEU Score: }" + str(valid_score)) 
			#intermList.append("\\\\ \\cline{2-5}")
			
			row += "&" + " & ".join(x for x in intermList) + "\\\\ \\cline{2-5}"
		row += "\\hline"
				#pprint(gold_text)
	#pprint(generated_test)
		sent_a_table_header += row 
	sent_a_table_header += r''' \end{longtable}'''

	
	pprint(global_dict)
	with open('aux2.txt', 'w') as aux:
		aux.write(sent_a_table_header)


if __name__ == '__main__':
    generate_opta_table()
    #generate_sentb_table()


    #generate_sb_table()