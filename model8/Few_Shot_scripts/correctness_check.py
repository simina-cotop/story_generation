# Implement a correctness check for the test output
from typing import Dict, List, Tuple
from pprint import pprint

unit_mapping = {
    'percentage': ['%'],
    'salary(1000$)': ['1000', '$'],
    ' (million dollar)': ['1000000'],
    'number of university': ['#'],
    'percentage of people': ['%']
}


#!!!TODO:Change this to test once I have the results
#!!!TODO:Do not need to pass the chart as argument because the file contains ALL charts
def get_original_generated_sentences_opt_domain(domain: str, chart: str, domain_outputs: str) -> Dict[str, Dict[str, List[Tuple[str,str]]]]:
    #Dict[domain, Dict[chart, List[Tuple[original, generated]]]]
    all_sentences: Dict[str, Dict[str, List[Tuple[str,str]]]] = {}
    all_sentences.setdefault(domain, {})
    all_sentences[domain].setdefault(chart, [])
    with open(f'{domain}/original_data/valid.summary','r') as orig:
        with open(f'{domain_outputs}valid_summary.clean.txt', 'r') as gen:
            for orig_line, gen_line in zip(orig, gen):
                all_sentences[domain][chart].append((orig_line.strip(' \n'), gen_line))
    #for el in all_sentences[domain][chart]:
    #    print(el[0] + '\t' + el[1] + '\n\n\n')
    return all_sentences


# Parse the charts_info files and get the pairs containg the x categories and the y values, i.e. turn 
#x categories : Computer Science, Arts, Mathematics, Literature, Engineering
#y values : 20, 60, 10, 70, 30
# into
# (Computer Science, 20), (Arts, 60), (Mathematics, 10), (Literature, 70), (Engineering, 30)
def get_chart_labels(all_charts: List[str]) -> Dict[str, Dict[str, List[Tuple[str,str]]]]:
    
    #Dict[chart,List[Tuple[x_cat_val1,y_val1],Tuple[x_cat_val2,y_val2]...]]
    all_info: Dict[str, Dict[str,List[Tuple[str,str]]]] = {}
    
    for chart_file in all_charts:
        all_info.setdefault(chart_file,{})

        chart_info : Dict[str, List[str]] = {}

        with open(f'../charts_info/{chart_file}','r') as f:
            data = f.read()
        lines = data.split("\n")
        relevant_lines: List[str] = []

        # Save only the lines we need 
        relevant_lines.append(lines[1]) # x categories
        relevant_lines.append(lines[2]) # y values
        relevant_lines.append(lines[5]) # y axis unit
        
        for line_idx, line in enumerate(relevant_lines):
            if line_idx == 0 or line_idx == 1:
                aux = line.split(" : ")
                # Category
                processed_aux: str = aux[1].lower()
                # Actual values
                processed_aux = processed_aux.split(", ")
                chart_info[aux[0]] = processed_aux
            else:
                aux = line.split(" : ")
                chart_info[aux[0]] = []
                chart_info[aux[0]].append(aux[1].lower())

        for unit in chart_info['y axis unit']:
            all_info[chart_file][unit] = []

        pprint(chart_info)

        # Save pairs of (xcat,yval)
        for unit in chart_info['y axis unit']:
            for xcat, yval in zip(chart_info['x categories'], chart_info['y values']):
                all_info[chart_file][unit].append((xcat,yval))
            
    pprint(all_info)
    return all_info

def check_label_occurrences_forwards(sentence: List[str], chart_labels:List[Tuple[str,str]],labels_occurr_dict:Dict[Tuple[str,str],int]) -> Dict[Tuple[str,str],int]:
    for label in chart_labels:
        
        if label[0] in sentence:
            
            #Get the index corresponding to the label
            index = sentence.index(label[0])

            for window in range(1,4):
                sliced_sent = sentence[index:index+window]
                #print(index,sliced_sent)
                xlabel = False 
                ylabel = False

                if label[0] in sliced_sent:
                    xlabel = True
                #TODO: will probably need to change this when I incorporate the units
                for el in sliced_sent:
                    if label[1] in el:
                        ylabel = True
                if xlabel == True and ylabel == True:
                    #print(sliced_sent)
                    print("HERE2")
                    if labels_occurr_dict[label] == 0:
                        labels_occurr_dict[label] = 1
                    
                xlabel = False
                ylabel = False
    print("forwards")
    pprint(labels_occurr_dict)
    return labels_occurr_dict


def check_label_occurrences_backwards(sentence: List[str], chart_labels:List[Tuple[str,str]],labels_occurr_dict:Dict[Tuple[str,str],int]) -> Dict[Tuple[str,str],int]:

    for label in chart_labels:
        
        if label[0] in sentence:
            
            #Get the index corresponding to the label
            index = sentence.index(label[0])
    
            for window in range(0,6):
                sliced_sent = sentence[index-window:index+1]
    
                print(sliced_sent)
                xlabel = False 
                ylabel = False

                if label[0] in sliced_sent:
                    xlabel = True
                #TODO: will probably need to change this when I incorporate the units
                for el in sliced_sent:
                    if label[1] in el:
                        ylabel = True
                if xlabel == True and ylabel == True:
                    print("HERE")
                    if labels_occurr_dict[label] == 0:
                        labels_occurr_dict[label] = 1
                
                
                xlabel = False
                ylabel = False

    print("backwards") 
    pprint(labels_occurr_dict)
    return labels_occurr_dict


#TODO: integrate the units
#Takes as input the chart and its corresponding label information and checks if that information appears correctly in the generated text
def check1(chart: str, chart_labels:List[Tuple[str,str]], all_sentences: Dict[str, Dict[str, List[Tuple[str,str]]]], units_maps: List[str]) -> None:
    #pprint(all_sentences)
    one_pair = all_sentences['chartsopta']['gender_pay_gap.txt'][3]
    print(one_pair, chart_labels)
    
    processed_original: List[str] = one_pair[0].lower().split(" ")
    processed_generated: List[str] = one_pair[1].lower().split(" ")
    print("processed_original=", processed_original)
    print("processed_generated=", processed_generated)
    
    #TODO: create one dict per chart
    labels_occurr_dict: Dict[Tuple[str,str],int] = {}
    for label in chart_labels:
        labels_occurr_dict[label] = 0
    for_labels_occur_dict = correct_labels_forwards = check_label_occurrences_forwards(processed_generated, chart_labels,labels_occurr_dict)
    final_labels_occur_dict = correct_labels_backwards = check_label_occurrences_backwards(processed_generated,chart_labels,for_labels_occur_dict)
    print("FINAL")
    pprint(final_labels_occur_dict)        
    #chart_correct_labels = correct_labels_backwards / len(chart_labels)
    #print(correct_labels_backwards, len(chart_labels), chart_correct_labels)

    








if __name__ == '__main__':
    domains = ['chartsopta','chartsoptb','chartssenta','chartssentb','chartssa','chartssb']
    domain_outputs = ['../../../../output_files_aws/20200627223805/chartsopta/results/loads/23/23/valid/']
    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    info_charts = ['info_gender_pay_gap.txt', 'info_median_salary_women.txt', 'info_young_evenings.txt', 'info_median_salary_se.txt', 'info_women_study_departments.txt', 'info_num_top_unis.txt', 'info_obesity.txt', 'info_women_work_sector.txt', 'info_student_choice_study.txt', 'info_money_spent_he.txt']

    all_sentences = get_original_generated_sentences_opt_domain(domains[0], no_delexi_charts[1], domain_outputs[0])
    chart_labels = get_chart_labels(info_charts)
    check1(no_delexi_charts[1], chart_labels['info_gender_pay_gap.txt']['percentage'], all_sentences, unit_mapping['percentage'])