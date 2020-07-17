# Implement a correctness check for the test output
from typing import Dict, List, Tuple
from pprint import pprint


#!!!TODO:Change this to test once I have the results
#!!!TODO:Do not need to pas the chart as argument because the file contains ALL charts
def get_original_generated_sentences_opt_domain(domain: str, chart: str, domain_outputs: str) -> None:
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
        # Kick out all the other lines except the first 2
        lines = lines[:3]
        # Kick out the title
        lines = lines[1:]
        for line in lines:
            aux = line.split(" : ")
            # Category
            processed_aux: str = aux[1].lower()
            # Actual values
            processed_aux = processed_aux.split(", ")
            chart_info[aux[0]] = processed_aux

        # Save pairs of (xcat,yval)
        for xcat, yval in zip(chart_info['x categories'], chart_info['y values']):
            all_info[chart_file].append((xcat,yval))
            
    #pprint(all_info)
    return all_info
    








if __name__ == '__main__':
    domains = ['chartsopta','chartsoptb','chartssenta','chartssentb','chartssa','chartssb']
    domain_outputs = ['../../../../output_files_aws/20200627223805/chartsopta/results/loads/23/23/valid/']
    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    info_charts = ['info_gender_pay_gap.txt', 'info_median_salary_women.txt', 'info_young_evenings.txt', 'info_median_salary_se.txt', 'info_women_study_departments.txt', 'info_num_top_unis.txt', 'info_obesity.txt', 'info_women_work_sector.txt', 'info_student_choice_study.txt', 'info_money_spent_he.txt']
    get_original_generated_sentences_opt_domain(domains[0], no_delexi_charts[0], domain_outputs[0])
    chart_labels = get_chart_labels(info_charts)