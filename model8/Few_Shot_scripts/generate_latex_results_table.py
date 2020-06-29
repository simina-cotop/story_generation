from parse_chartsoptab_results import bleu_gold_chartsopta, bleu_score
from pprint import pprint

#def generate_content(gold, test, valid):




def generate_opta_table():
	gold_path = 'chartsopta/all_gold/'
	test_path = '/mnt/Backup/simina/output_files_aws/inference_only_20200628084433/chartsopta/results/test/'
	valid_path = '/mnt/Backup/simina/output_new_folder/20200607003751/chartsopta/results/loads/3/valid/'

	all_results = bleu_gold_chartsopta()
	print(all_results)

	global_dict = {}
	sent_a_table_header = r'''\section{SentA}

\begin{longtable}{|p{13mm}|p{57mm}|p{57mm}|p{57mm}|p{57mm}|}
	\hline 
	Chart & Human Description & Validation & Human Description & Test  \\ 
	\hline 
	\endhead'''

	


	for orig_idx in range(10):
		
		row = r'''\multirow{2}{*}{Chart ''' + str(orig_idx) + '}' 
		for gen_idx in range(0,3):
			global_dict[orig_idx] = []
			intermList = []
			new_gen_idx = orig_idx * 3 + gen_idx
			with open(f'chartsoptb/original_data/test.summary', 'r') as test1:
				gold_text = test1.readline()
				gold_text = gold_text.replace('%','\%')
				gold_text = gold_text.replace('$','\$')
				gold_text = gold_text.replace('\\\\n','')
				intermList.append(gold_text)
			with open(f'{test_path}test_pred_summary_{new_gen_idx}', 'r') as test2:
				test_score = bleu_score(f'chartsopta/all_gold/opta_test_{orig_idx}_{gen_idx}', f'{test_path}test_pred_summary_{new_gen_idx}')
				print("test_score", test_score)
				test_sent = test2.read()
				test_sent = test_sent.replace('%','\%')
				test_sent = test_sent.replace('$','\$')
				test_sent = test_sent.replace('\\\\n','')
				print("test_sent", test_sent)
				intermList.append(test_sent + "\\newline" + " \textbf{BLEU Score: }" + str(test_score))
			with open(f'chartsoptb/original_data/valid.summary', 'r') as valid1:
				#gold_text.append(valid1.readline())
				valid_read = valid1.readline()
				valid_read = valid_read.replace('%','\%')
				valid_read = valid_read.replace('$','\$')
				valid_read = valid_read.replace('\\\\n','')
				intermList.append(valid_read)
			with open(f'{valid_path}valid_pred_summary_{new_gen_idx}', 'r') as valid2:
				valid_score = bleu_score(f'chartsopta/all_gold/opta_valid_{orig_idx}_{gen_idx}', f'{valid_path}valid_pred_summary_{new_gen_idx}')
				valid_sent = valid2.read()
				valid_sent = valid_sent.replace('%','\%')
				valid_sent = valid_sent.replace('$','\$')
				valid_sent = valid_sent.replace('\\\\n','')
				intermList.append(valid_sent + "\\newline" + " \textbf{BLEU Score: }" + str(valid_score)) 
		
		global_dict[orig_idx] = intermList
		row += "&" + " & ".join(x for x in intermList) + "\\\\ \\hline \n"
				#pprint(gold_text)
	#pprint(generated_test)
		sent_a_table_header += row 
	sent_a_table_header += r'''\hline  \end{longtable}'''

	
	pprint(global_dict)
	with open('aux.txt', 'w') as aux:
		aux.write(sent_a_table_header)
		



'''\multirow{2}{*}{Chart 1} & desc & desc & 31.00 & 31.00\\ \cline{2-4}
						  & desc & desc & 31.00 & 31.00\\ \cline{2-4}
		 				  & desc & desc & 31.00 & 31.00\\ \cline{2-4}
				     	  & desc & desc & 31.00 & 31.00\\ \cline{2-4}
			 	          & desc & desc & 31.00 & 31.00\\ \cline{2-4}
	\hline 
\multirow{ 2}{*}{Chart 2} & desc & desc & 31.00 \\
	& desc & desc & 31.00\\
	& desc & desc & 31.00\\
	& desc & desc & 31.00\\
	& desc & desc & 31.00\\'''





if __name__ == '__main__':
    generate_opta_table()
    #generate_sentb_table()

    #generate_opt_table()

    #generate_s_table()