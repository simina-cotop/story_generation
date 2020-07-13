from typing import List, Dict, Tuple, NamedTuple, Set
from pprint import pprint
from gen_few_shot_files_sentences import parse_info_files_per_chart, turn_chart_info_into_sentences

'''xcategories	2755
yvalues	2756
xmajorticks	2757
ymajorticks	2758
yaxisunit	2759
xaxisname	2760
bar1_x_categories 2761
bar2_x_categories 2762
bar3_x_categories 2763
bar4_x_categories 2764
bar5_x_categories 2765
bar1_y_values 2766
bar2_y_values 2767
bar3_y_values 2768
bar4_y_values 2769
bar5_y_values 2771
bar1_diffadd1 2772
bar1_diffadd2 2773
bar1_diffadd3 2774
bar1_diffadd4 2775
bar1_diffadd5 2776
bar2_diffadd1 2777
bar2_diffadd2 2778
bar2_diffadd3 2779
bar2_diffadd4 2780
bar2_diffadd5 2781
bar2_diffadd6 2782
bar3_diffadd1 2783
bar3_diffadd2 2784
bar3_diffadd3 2785
bar3_diffadd4 2786
bar3_diffadd5 2787
bar3_diffadd6 2788
bar3_diffadd7 2789
bar3_diffadd8 2790
bar3_diffadd9 2791
bar4_diffadd1 2792
bar4_diffadd2 2793
bar4_diffadd3 2794
bar4_diffadd4 2795
bar4_diffadd5 2796
bar4_diffadd6 2797
bar5_diffadd1 2798
bar5_diffadd4 2799
bar5_diffadd7 2800
bar5_diffadd8 2801
bar1_diffmul1 2802
bar1_diffmul2 2803
bar1_diffmul3 2804
bar1_diffmul4 2805
bar1_diffmul5 2806
bar1_diffmul7 2807
bar2_diffmul1 2808
bar2_diffmul2 2809
bar2_diffmul3 2810
bar2_diffmul4 2811
bar2_diffmul5 2812
bar2_diffmul6 2813
bar2_diffmul8 2814
bar2_diffmul9 2815
bar3_diffmul1 2816
bar3_diffmul2 2817
bar3_diffmul3 2818
bar3_diffmul4 2819
bar3_diffmul5 2820
bar3_diffmul6 2821
bar3_diffmul7 2822
bar3_diffmul8 2823
bar3_diffmul9 2824
bar4_diffmul1 2825
bar4_diffmul2 2826
bar4_diffmul3 2827
bar4_diffmul4 2828
bar4_diffmul5 2829
bar4_diffmul6 2830
bar5_diffmul1 2831
bar5_diffmul4 2832
bar5_diffmul7 2833
bar5_diffmul8 2834'''



def get_all_unique_annotations(no_delexi_charts: List[str]) -> Set[str]:
    for chart in no_delexi_charts:
        _, reversed_chart_descs = parse_info_files_per_chart(chart)
        all_annotations: List[str] = []
        for keys, all_values in reversed_chart_descs.items():
            for pair in all_values:
                all_annotations.append(pair[0])
        pprint(all_annotations)
        all_unique_annotations = set(all_annotations)
        pprint(all_unique_annotations)
        print(len(all_annotations), len(all_unique_annotations))
        return all_unique_annotations



def append_to_last_line(all_unique_annotations: Set[str]) -> None:
    vocab_file = '../../../../few_shot_appendix/data_release/human_books_songs_films_field_vocab.txt'
    last_line: str = "imagewidth	2754"
    splitted_last_line: List[str] = last_line.split("\t")
    print(splitted_last_line)
    with open(vocab_file, 'a') as vf:
        counter: int = 1
        for annotation in all_unique_annotations:
            vf.write(annotation + "\t" + str(int(splitted_last_line[1]) + counter) + "\n")
            print(annotation + "\t" + str(int(splitted_last_line[1]) + counter))
            counter += 1





if __name__ == '__main__':
    domains = ['chartsopta','chartsoptb','chartssenta','chartssentb','chartssa','chartssb']
    no_delexi_charts = ['women_representation_in_different_sectors.txt', 'gender_pay_gap.txt', 'how_do_young_people_spend_their_evenings.txt', 'Median_salary_of_women.txt', 'median_salary_per_year_for_se_with_respect_to_their_degrees.txt', 'Money_spent_on_higher_education.txt', 'Number_of_top_Unis.txt', 'what_causes_obesity.txt', 'what_do_students_choose_to_study.txt', 'women_representation_in_different_departments.txt']
    
    all_unique_annotations = get_all_unique_annotations(no_delexi_charts)
    append_to_last_line(all_unique_annotations)




    