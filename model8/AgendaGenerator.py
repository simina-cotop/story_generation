import dill
import configurations
from configurations import Config
import numpy as np
import random

gender_pay_gap = [['<topic>_gender_pay_gap\n'],
                         ['<x_axis_label_highest_value>_gender_pay_gap\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>_gender_pay_gap\n'], 
                         ['<y_axis>_gender_pay_gap\n'], 
                         ['<x_axis_labels>_gender_pay_gap\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>_gender_pay_gap\n'], 
                         ['<x_axis_label_least_value>_gender_pay_gap\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'], 
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>_gender_pay_gap\n'],
                         ['<y_axis>_gender_pay_gap\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ]
median_salary_women = [['<topic>_median_salary_women\n'],
                         ['<x_axis_label_highest_value>_median_salary_women\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>_median_salary_women\n'], 
                         ['<y_axis>_median_salary_women\n'], 
                         ['<x_axis_labels>_median_salary_women\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>_median_salary_women\n'], 
                         ['<x_axis_label_3rd_highest_value>_median_salary_women\n'],
                         ['<x_axis_label_least_value>_median_salary_women\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>_median_salary_women\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ]  

median_salary_se = [['<topic>_median_salary_se\n'],
                         ['<x_axis_label_highest_value>_median_salary_se\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>_median_salary_se\n'], 
                         ['<y_axis>_median_salary_se\n'], 
                         ['<x_axis_labels>_median_salary_se\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>_median_salary_se\n'], 
                         ['<x_axis_label_3rd_highest_value>_median_salary_se\n'],
                         ['<x_axis_label_least_value>_median_salary_se\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>_median_salary_se\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
money_spent_he = [['<topic>_money_spent_he\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
num_top_unis = [['<topic>_num_top_unis\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
obesity = [['<topic>_obesity\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
student_choice_study = [['<topic>_student_choice_study\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
women_study_department = [['<topic>_women_study_department\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
women_work_sector = [['<topic>_women_work_sector\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 
young_evenings = [['<topic>_young_evenings\n'],
                         ['<x_axis_label_highest_value>\n'], 
                         ['<y_axis_highest_value>\n'], 
                         ['<topic_related_property>\n'], 
                         ['<y_axis>\n'], 
                         ['<x_axis_labels>\n'], 
                         ['<order_Scnd>\n'], 
                         ['<x_axis_label_Scnd_highest_value>\n'], 
                         ['<x_axis_label_3rd_highest_value>\n'],
                         ['<x_axis_label_least_value>\n'], 
                         ['<y_axis_least_value>\n'],
                         ['<y_axis_highest_value_val>\n'], 
                         ['<y_x_comparison>\n'], 
                         ['<y_axis_trend>\n'], 
                         ['<y_axis_least_value_val>\n'],
                         ['<y_axis_Scnd_highest_val>\n'],
                         ['<y_axis_3rd_highest_val>\n'],     
                         ['<y_axis_inferred_value>\n'], 
                         ['<x_axis>\n'], 
                         ['<y_axis_approx>\n'],
                         #['<y_axis_trend_down>\n'],
                         ['<final_label_left>\n']
                         ] 


#event_counter_1 = {'<topic>_gender_pay_gap\n':0}

event_counter_1 = {'<topic>_gender_pay_gap\n':0,
                         '<x_axis_label_highest_value>_gender_pay_gap\n':0,
                         '<topic_related_property>_gender_pay_gap\n':0,
                         '<y_axis>_gender_pay_gap\n':0, 
                         '<x_axis_labels>_gender_pay_gap\n':0,
                         '<x_axis_label_Scnd_highest_value>_gender_pay_gap\n':0,
                         '<x_axis_label_3rd_highest_value>_gender_pay_gap\n':0,     
                         '<x_axis_label_least_value>_gender_pay_gap\n':0,
                         '<x_axis>_gender_pay_gap\n':0,
                    

                         '<topic>_median_salary_se\n':0,
                         '<x_axis_label_highest_value>_median_salary_se\n':0,
                         '<topic_related_property>_median_salary_se\n':0,
                         '<y_axis>_median_salary_se\n':0, 
                         '<x_axis_labels>_median_salary_se\n':0,
                         '<x_axis_label_Scnd_highest_value>_median_salary_se\n':0,
                         '<x_axis_label_3rd_highest_value>_median_salary_se\n':0,     
                         '<x_axis_label_least_value>_median_salary_se\n':0,
                         '<x_axis>_median_salary_se\n':0,


                         '<topic>_median_salary_women\n':0,
                         '<x_axis_label_highest_value>_median_salary_women\n':0,
                         '<topic_related_property>_median_salary_women\n':0,
                         '<y_axis>_median_salary_women\n':0, 
                         '<x_axis_labels>_median_salary_women\n':0,
                         '<x_axis_label_Scnd_highest_value>_median_salary_women\n':0,
                         '<x_axis_label_3rd_highest_value>_median_salary_women\n':0,     
                         '<x_axis_label_least_value>_median_salary_women\n':0,
                         '<x_axis>_median_salary_women\n':0,

                         '<topic>_money_spent_he\n':0,
                         '<topic>_num_top_unis\n':0,
                         '<topic>_obesity\n':0,
                         '<topic>_student_choice_study\n':0,
                         '<topic>_women_study_department\n':0,
                         '<topic>_women_work_sector\n':0,
                         '<topic>_young_evenings\n':0,
                         '<x_axis_label_highest_value>\n':0,
                         

                         '<y_axis_highest_value>\n':0, 
                         '<topic_related_property>\n':0, 
                         '<y_axis>\n':0, 
                         '<x_axis_labels>\n':0, 
                         '<order_Scnd>\n':0, 
                         '<x_axis_label_Scnd_highest_value>\n':0,
                         '<x_axis_label_3rd_highest_value>\n':0,     
                         '<x_axis_label_least_value>\n':0, 
                         '<y_axis_least_value>\n':0,
                         '<y_axis_highest_value_val>\n':0, 
                         '<y_x_comparison>\n':0, 
                         '<y_axis_trend>\n':0, 
                         '<y_axis_least_value_val>\n':0,
                         '<y_axis_Scnd_highest_val>\n':0,
                         '<y_axis_3rd_highest_val>\n':0,     
                         '<y_axis_inferred_value>\n':0, 
                         '<x_axis>\n':0, 
                         '<y_axis_approx>\n':0,
                         #'<y_axis_trend_down>\n':0,
                         '<final_label_left>\n':0
                         }

def word_frequencies(file_list):
    """
    Returns a dictionary with the frequencies
    of the annotations occurring on file with name.
    """
    result = event_counter_1
    for file in file_list:
        file1 = open(file, 'r', encoding='latin1')
    
        while True:
            line = file1.readline()
            if line == '':
                break
            words = line.split(' ')
            for word in words:
                if "<" in word:
                    if word.rstrip().strip() in result:
                        result[word.rstrip().strip()] += 1
                    #else:
                    #    result[word.rstrip().strip()] = 1
        file1.close()
    return result
All_files = [
                         'data6u/gender_pay_gap.txt',
                         'data6u/median_salary_se.txt',
                         'data6u/median_salary_women.txt',
                         'data6u/money_spent_he.txt',
                         'data6u/num_top_unis.txt',
                         'data6u/obesity.txt',
                         'data6u/student_choice_study.txt',
                         'data6u/women_study_department.txt',
                         'data6u/women_work_sector.txt',
                         'data6u/young_evenings.txt'
                         ]    
gender_freq = word_frequencies(['data6u/gender_pay_gap.txt'])
median_salary_se_freq = word_frequencies(['data6u/median_salary_se.txt'])
median_salary_women_freq = word_frequencies(['data6u/median_salary_women.txt'])
money_spent_he_freq = word_frequencies(['data6u/money_spent_he.txt'])
num_top_unis_freq = word_frequencies(['data6u/num_top_unis.txt'])
obesity_freq = word_frequencies(['data6u/obesity.txt'])
student_choice_study_freq = word_frequencies(['data6u/student_choice_study.txt'])
women_study_department_freq = word_frequencies(['data6u/women_study_department.txt'])
women_work_sector_freq = word_frequencies(['data6u/women_work_sector.txt'])
young_evenings_freq = word_frequencies(['data6u/young_evenings.txt'])
event_counter = {'gender_pay_gap': gender_freq,
                 'median_salary_se':median_salary_se_freq,
                 'median_salary_women':median_salary_women_freq,
                 'money_spent_he':money_spent_he_freq,
                 'num_top_unis':num_top_unis_freq,
                 'obesity':obesity_freq,
                 'student_choice_study':student_choice_study_freq,
                 'women_study_department':women_study_department_freq,
                 'women_work_sector':women_work_sector_freq,
                 'young_evenings':young_evenings_freq

                }

#print (event_counter_2)
class Agenda(object):
    script_representations = {'gender_pay_gap': gender_pay_gap, 
                              'median_salary_women': median_salary_women, 
                              'median_salary_se': median_salary_se,
                              'money_spent_he': money_spent_he,
                              'num_top_unis': num_top_unis,
                              'obesity': obesity,
                              'student_choice_study': student_choice_study,
                              'women_study_department': women_study_department,
                              'women_work_sector': women_work_sector,
                              'young_evenings': young_evenings,
                              
                              }
    event_counter = event_counter#dill.load(open('e_counters', 'rb'))
    #event_counter = dill.load(open('gender_pay_gap', 'rb'))
    
    #f = open('e_counters', 'rb')
    #fc =  f.read()
    #f.close()
    #print (fc)
    @staticmethod
    def generate_agenda(script, temperature=0.5):
        #print("script is : ")
        #print (script)
        dfa = Agenda.script_representations[script]
        #print("dfa is : ")
        #print (dfa)
        #print (script)
        count = Agenda.event_counter[script]
        #print (count)
        agenda = list()
        #print("script inside generate_agenda is : ")
        #print(script)
        agenda.append('Story_Begin_' + script )
        agenda.append('<topic>_' + script + '\n' )
        for segment in dfa:
            for event in segment:
                sample = np.random.uniform(0, 1)
                if sample < np.power(min(count[event]/100, 1), temperature):
                    agenda.append(event)
        agenda.append('Story_End_' + script)
        #print("agenda = ", agenda)
        return agenda

    @staticmethod
    def generate_random_agenda(script, length):
        dfa = Agenda.script_representations[script]
        agenda = list()
        
        #print("script here is :")
        #print(script)
        agenda.append('Story_Begin_' + script)
        agenda.append('<topic>_' +script + '\n')
        for _ in range(length):
            candidate_list = random.choice(dfa)
            random_event = random.choice(candidate_list)
            agenda.append(random_event)
        agenda.append('Story_End_' + script)
        return agenda

    @staticmethod
    def generate_seed(script, temperature=1):
        # def __init__(self, x_context, e_p_context, e_f_context, agenda)
        x_context = list(['the'])
        #print("script here is :")
        #print(script)
        e_p_context = ['Story_Begin_' + script] * 2
        #e_f_context = ['<Evoking_gender_pay_gap>\n'] * 2
        e_f_context = ['<topic>_' + script + '\n'] * 2

        agenda = Agenda.generate_agenda(script, temperature)
        return Config.Seed(x_context, e_p_context, e_f_context, agenda)

    @staticmethod
    def generate_random_seed(script, length):
        x_context = list(['the'])
        #print("script here is :")
        #print(script)
        e_p_context = ['Story_Begin_' +script] * 2
        #e_f_context = ['<Evoking_gender_pay_gap>\n'] * 2
        
        e_f_context = ['<topic>_'+ script + '\n'] * 2

        agenda = Agenda.generate_random_agenda(script, length)
        return Config.Seed(x_context, e_p_context, e_f_context, agenda)

    @staticmethod
    def generate_seeds(scripts, lengths):
        """
        generate 4 seeds for each script: 2 rational and 2 random of length lengths[script]
        :param scripts:
        :param lengths: dict script->length of agenda
        :return:
        """
        seeds = list()
        for script in scripts:
            seeds.append(Agenda.generate_random_seed(script, lengths[script]))
            seeds.append(Agenda.generate_random_seed(script, lengths[script]))
            seeds.append(Agenda.generate_seed(script))
            seeds.append(Agenda.generate_seed(script))
        return seeds


#ss = Agenda.generate_seeds(['grocery'], {'grocery': 15})

# aa = Agenda.generate_random_seed('bath', 10)

'''
for script in Agenda.script_representations:
    for segment in Agenda.script_representations[script]:
        for event in segment:
            ee = Agenda.event_counter[script]
            if event not in ee:
                print('wo ha ha')
'''


pass
