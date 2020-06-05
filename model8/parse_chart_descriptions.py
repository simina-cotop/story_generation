# Generate input files for the chartsoptb domain, from the training data, i.e. chart descriptions given by humans
# including descriptions of the bars as sentences

from typing import List, Dict, Tuple, NamedTuple, Set
import matplotlib.pyplot as plt
import os
import glob
import csv
import re
from pprint import pprint


def parse_info_files_per_chart(chart_file: str) -> List[str]:
    all_chart_descriptions: Dict[int, List[str]] = {}
    final_chart_descriptions: List[str] = []

    idx: int = 0
    with open("no_delexi_data/" + chart_file, 'r') as fin:
        inline = fin.readline() # Reads ''
        inline = fin.readline()
        # While we did not reach the end of the file        
        while inline != '':
            # Remove the \n from the strings
            inline = inline.replace("\n", "")
            assert(inline != '')
            # Split on the spaces
            if '    ' in inline:
                splited_inline = inline.split('    ')

                # If we have annotated lines
                if (len(splited_inline) == 2):
                    assert(splited_inline[1] != '')
                    all_chart_descriptions.setdefault(idx, list()).append(splited_inline[0])
            else:
                all_chart_descriptions.setdefault(idx, list()).append(inline)
                
            if inline == '<end_of_description>':
                    idx += 1
                    inline = fin.readline()
            else:
                inline = fin.readline()
                
    #pprint(all_chart_descriptions)
    for idx, description in all_chart_descriptions.items():
        desc_str: str = ' '.join(description)
        desc_str = desc_str.strip('<end_of_description>')
        desc_str = desc_str.replace(" .", ".")
        desc_str = desc_str.replace(" %", "%")
        desc_str = desc_str.replace("( ", "(")
        desc_str = desc_str.replace(" )", ")")
        final_chart_descriptions.append(desc_str)
    print(final_chart_descriptions)
    return final_chart_descriptions


if __name__ == "__main__":
    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    
    
    with open('chartsoptb.summary', 'w') as g:
        for chart in no_delexi_charts:
            chart_descs = parse_info_files_per_chart(chart)
            for desc in chart_descs:
                g.write(desc + "\n")
            g.write('\n\n')