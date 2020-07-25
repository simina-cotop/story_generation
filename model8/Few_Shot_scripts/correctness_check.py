# Implement a correctness check for the test output
from typing import Dict, List, Tuple
from pprint import pprint
from collections import OrderedDict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

unit_mapping = {
    'percentage': ['%'],
    'salary(1000$)': ['1000', '$'],
    ' (million dollar)': ['1000000'],
    'number of university': ['#'],
    'percentage of people': ['%']
}


#!!!TODO:Change this to test once I have the results
def get_original_generated_sentences_opt_domain(domain: str, all_charts: List[str], domain_outputs: str) -> Dict[str, Dict[str, List[Tuple[str,str]]]]:

    #OrderedDict[domain, OrderedDict[chart, List[Tuple[original, generated]]]]
    all_sentences: OrderedDict[str, OrderedDict[str, List[Tuple[str,str]]]] = OrderedDict()
    all_sentences.setdefault(domain, OrderedDict())

    for chart in all_charts:
        all_sentences[domain].setdefault(chart, [])
        
    with open(f'{domain}/original_data/valid.summary','r') as orig:
        with open(f'{domain_outputs}valid_summary.clean.txt', 'r') as gen:

            for idx, (orig_line, gen_line) in enumerate(zip(orig, gen)):

                if domain == 'chartsopta' or domain == 'chartsoptb': #3 generated sentences
                    chart_idx = idx // 3
                    all_sentences[domain][all_charts[chart_idx]].append((orig_line.strip(' \n'), gen_line))

                elif domain == 'chartssenta' or domain == 'chartssentb' or domain == 'chartssa' or domain == 'chartssb': #5 generated sentences
                    chart_idx = idx // 5
                    all_sentences[domain][all_charts[chart_idx]].append((orig_line.strip(' \n'), gen_line))
    
    print("ALL")
    pprint(all_sentences)
    return all_sentences


# Parse the charts_info files and get the pairs containg the x categories and the y values, i.e. turn 
#x categories : Computer Science, Arts, Mathematics, Literature, Engineering
#y values : 20, 60, 10, 70, 30
# into
# (Computer Science, 20), (Arts, 60), (Mathematics, 10), (Literature, 70), (Engineering, 30)
def get_chart_labels(all_charts: List[str]) -> Dict[str, List[Tuple[str,str]]]:
    
    #Dict[chart,List[Tuple[x_cat_val1,y_val1],Tuple[x_cat_val2,y_val2]...]]
    all_info: Dict[str, List[Tuple[str,str]]] = {}
    
    for chart_file in all_charts:
        all_info.setdefault(chart_file,list())

        chart_info : Dict[str, List[str]] = {}

        with open(f'../charts_info/{chart_file}','r') as f:
            data = f.read()
        lines = data.split("\n")
        relevant_lines: List[str] = []

        # Save only the lines we need 
        relevant_lines.append(lines[1]) # x categories
        relevant_lines.append(lines[2]) # y values
        
        
        for line_idx, line in enumerate(relevant_lines):
            aux = line.split(" : ")
            # Category
            processed_aux: str = aux[1].lower()
            # Actual values
            processed_aux = processed_aux.split(", ")
            chart_info[aux[0]] = processed_aux
            
        
        #pprint(chart_info)

        # Save pairs of (xcat,yval)
        
        for xcat, yval in zip(chart_info['x categories'], chart_info['y values']):
            all_info[chart_file].append((xcat,yval))

    '''{'x categories': ['germany', 'spain', 'uk'],
        'y values': ['5', '10', '15']}'''
    #pprint(all_info)
    return all_info

def check_label_occurrences_forwards(full_sentence: str, chart_labels:List[Tuple[str,str]],labels_occurr_dict:Dict[Tuple[str,str],Tuple[bool,int]]) -> Dict[Tuple[str,str],Tuple[bool,int]]:

    for label in chart_labels:
        #print(label[0], full_sentence)

        splitted_sentence = word_tokenize(full_sentence)

        if label[0] in splitted_sentence or label[0].lower() in splitted_sentence:
            
            
            sentence = [word for word in splitted_sentence if not word in stopwords.words('english')]
            
            #Get the index corresponding to the label
            index = sentence.index(label[0])

            for window in range(1,len(sentence)):
                sliced_sent = sentence[index:index+window]
                #print(index,sliced_sent)
                xlabel = False 
                ylabel = False

                if label[0] in sliced_sent or label[0].lower() in sliced_sent:
                    xlabel = True
                    #TODO: will probably need to change this when I incorporate the units
                for el in sliced_sent:
                    if label[1] in el:
                        ylabel = True
                if xlabel == True and ylabel == True:
                    #print(sliced_sent)
                    #print("HERE2")
                    labels_occurr_dict[label] = (True,1)
                if xlabel == True and ylabel == False:
                    labels_occurr_dict[label] = (True,0)    
                xlabel = False
                ylabel = False
        else:
            labels_occurr_dict[label] = (False,0)
    print("forwards")
    pprint(labels_occurr_dict)
    return labels_occurr_dict


def check_label_occurrences_backwards(full_sentence: str, chart_labels:List[Tuple[str,str]], labels_occurr_dict:Dict[Tuple[str,str],Tuple[bool,int]]) -> Dict[Tuple[str,str],Tuple[bool,int]]:
    
    for label in chart_labels:
        splitted_sentence = word_tokenize(full_sentence)
        if label[0] in splitted_sentence or label[0].lower() in splitted_sentence:
            
            
            
            sentence = [word for word in splitted_sentence if not word in stopwords.words('english')]

            #Get the index corresponding to the label
            index = sentence.index(label[0])
    
            for window in range(0,6):
                sliced_sent = sentence[index-window:index+1]
    
                #print(sliced_sent)
                xlabel = False 
                ylabel = False

                if label[0] in sliced_sent or label[0].lower() in sliced_sent:
                    xlabel = True
                #TODO: will probably need to change this when I incorporate the units
                for el in sliced_sent:
                    if label[1] in el:
                        ylabel = True
                if xlabel == True and ylabel == True:
                    if labels_occurr_dict[label] == (None, None):
                        labels_occurr_dict[label] = (True,1)

                if xlabel == True and ylabel == False:
                    if labels_occurr_dict[label] == (None, None):
                        labels_occurr_dict[label] = (True,0)    

                xlabel = False
                ylabel = False
        else:
            if labels_occurr_dict[label] == (None, None):
                labels_occurr_dict[label] = (False,0)

    print("backwards") 
    pprint(labels_occurr_dict)
    return labels_occurr_dict


#TODO: integrate the units
#Takes as input the chart and its corresponding label information and checks if that information appears correctly in the generated text
def check1(all_charts: List[str], domain: str, chart_labels:Dict[str, List[Tuple[str,str]]], all_sentences: Dict[str, Dict[str, List[Tuple[str,str]]]], info_charts:List[str]) -> None:

    global_dict: Dict[str, Dict[Tuple[str,str],Tuple[bool,int]]] = {}

    for chart_idx, chart in enumerate(all_charts):
        global_dict[chart] = {}
        current_chart_labels = chart_labels[info_charts[chart_idx]]
        for idx, el in enumerate(all_sentences[domain][chart]):
            # one_pair[0] is the original sentence
            # one_pair[1] is the generated sentence
            one_pair = all_sentences[domain][chart][idx]
            print("el ", one_pair, current_chart_labels)
        
            #TODO: create one dict per chart
            '''{('germany', '5'): (True, 1),
                ('spain', '10'): (True, 0),
                ('uk', '15'): (True, 1)}'''
            labels_occurr_dict: Dict[Tuple[str,str],Tuple[bool,int]] = {}
            for label in current_chart_labels:
                labels_occurr_dict[label] = (None, None)
            
            for_labels_occur_dict = check_label_occurrences_forwards(one_pair[1].lower(), current_chart_labels, labels_occurr_dict)
            final_labels_occur_dict = check_label_occurrences_backwards(one_pair[1].lower(), current_chart_labels, for_labels_occur_dict)
            print("FINAL")
            pprint(final_labels_occur_dict)        
            #chart_correct_labels = correct_labels_backwards / len(chart_labels)
            #print(correct_labels_backwards, len(chart_labels), chart_correct_labels)

        global_dict[chart] = labels_occurr_dict
    pprint(global_dict)








if __name__ == '__main__':
    domains = ['chartsopta','chartsoptb','chartssenta','chartssentb','chartssa','chartssb']
    domain_outputs = ['../../../../output_files_aws/20200627223805/chartsopta/results/loads/23/23/valid/']

    no_delexi_charts = [
    'women_representation_in_different_sectors.txt', 
    'gender_pay_gap.txt', 
    'how_do_young_people_spend_their_evenings.txt', 
    'Median_salary_of_women.txt', 
    'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 
    'Money_spent_on_higher_education.txt', 
    'Number_of_top_Unis.txt', 
    'what_causes_obesity.txt', 
    'what_do_students_choose_to_study.txt', 
    'women_representation_in_different_departments.txt']

    info_charts = [
    'info_women_work_sector.txt', 
    'info_gender_pay_gap.txt', 
    'info_young_evenings.txt', 
    'info_median_salary_women.txt',
    'info_median_salary_se.txt', 
    'info_money_spent_he.txt',
    'info_num_top_unis.txt', 
    'info_obesity.txt', 
    'info_student_choice_study.txt', 
    'info_women_study_departments.txt'    
    ]

    all_sentences = get_original_generated_sentences_opt_domain(domains[0], no_delexi_charts, domain_outputs[0])
    chart_labels = get_chart_labels(info_charts)
    check1(no_delexi_charts, domains[0], chart_labels, all_sentences, info_charts)