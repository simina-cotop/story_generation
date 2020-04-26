import os


class Config(object):

    Run_Index = 'test5'
    os.mkdir('outputs/' + Run_Index)

    # TODO: EXP
    Sample_binary_path = 'samples_binary_' + Run_Index
    Event_descriptions = 'event_desc_1.csv'

    # TODO: corpus / data / preprocessing
    Clean_corpus_folder = r'.\clean_data'
    Clean_corpus_6_folder = os.path.join('.', 'data6u')
    CORPUS_FOLDER = r'.\InScript_LREC2016\InScript\corpus'

    Checkpoint_path = 'ghost lol lol '
    Epsilon = 1e-12
    # thres for NORM clipping
    CSV_log_path = 'outputs/' + Run_Index + '/' + r'log' + Run_Index + '.csv'
    LOG_DIR = r'.\tbLOG'
    Sample_path = 'outputs/' + Run_Index + '/samples_' + Run_Index
    # for unix
    # LOG_DIR = r'./LOG'
    Word2Vec_Google_Path = r'/home/simina/GoogleNews-vectors-negative300.bin'
    W2V_wrapper_path = os.path.join('.', 'w2v10')

    Effective_Scripts = [ 
                         'gender_pay_gap',
                         'median_salary_se',
                         'median_salary_women',
                         'money_spent_he',
                         'num_top_unis',
                         'obesity',
                         'student_choice_study',
                         'women_study_department',
                         'women_work_sector',
                         'young_evenings'
                         ]
    
    All_Scripts = [
                         'gender_pay_gap',
                         'median_salary_se',
                         'median_salary_women',
                         'money_spent_he',
                         'num_top_unis',
                         'obesity',
                         'student_choice_study',
                         'women_study_department',
                         'women_work_sector',
                         'young_evenings'
                         ]
    
    Empty_event_label = 'empty'
    End_of_sentence_tokens = list(['.', '!'])
    #End_of_story_label = '<end_of_story>'
    End_of_story_label = '<end_of_description>'

    #Evoking_Event = '<Evoking_gender_pay_gap>\n'
    Evoking_Event = '<topic>'
    Beginning_Event = 'Story_Begin'
    Ending_Event = 'Story_End'
    Invalid_Labels = ['1/2', '1/4']
    # Invalid_Labels = ['UnrelEv', 'RelNScrEv', 'Unclear', '1/2', '1/4', 'ScrEv_other']
    #Post_fix_events = ['UnrelEv', 'RelNScrEv', 'Unclear', 'ScrEv_other', 'Evoking']
    # Post_fix_events = ['Evoking']
    Padding_token = '<pad>'
    Punktuations = [',', '.', '!', ':', ';', '?', '(', ')','-']
    # Punktuation_unified = '.'
    Concatenation_delimiter = '+'
    Universal_number = 'several'

    # for unix:
    # CORPUS_FOLDER = r'./InScript_LREC2016/InScript/corpus'

    # TODO: TEST STABILITY
    #Validation_proportion = 0.025
    Validation_proportion = 0.1
    # TODO: model hypers----------------------------------------------------------------------
    # A_hidden_size = 512
    C_gru_interpolation_coef = 0.1
    # dropout for non-recurrent recurrent connections in RNN and dense layers
    Dropout_rate = 0.5
    # event embedding size equals to size of output o_t
    Event_embedding_size = 256
    Input_Embedding_size = 300

    Max_vocabulary_size = 99999

    # tokens strictly less frequent will be replaced by '<unk>'
    Least_frequency = 1
    # calling dataloader sets these values
    Active_vocabulary_size = 0
    # includes 'story begin', 'story end' labels. these are not included in the corpus.
    Event_vocabulary_size = 0

    RNN_size = 768
    Context_length = 1
    #TODO
    #Context_length = 1
    # training
    #Batch_size = 256
    Batch_size = 64
    Learning_rate = 0.397e-3

    Clipping_threshold = 1e10
    Early_stopping_patience = 1
    Loss_weight_on_a = 1.3
    Max_train_epochs = 1
    # weights_on_cat_of_a_loss
    # wa =
    Weight_on_a1_cross_entropy = [1., 4]
    # TODO: end model hypers-------------------------------------------------------------------
    # TODO: Generation
    # lower temperature -> conservative
    Temperature = .9
    Crucial_temperature = .01
    # the least number of tokens to generate before shifting events. should go well with **C_gru only** models.
    Minimal_event_span = 1

    class Seed(object):
        def __init__(self, x_context, e_p_context, e_f_context, agenda):

            self.scripts = [ 
                          'gender_pay_gap',
                         'median_salary_se',
                         'median_salary_women',
                         'money_spent_he',
                         'num_top_unis',
                         'obesity',
                         'student_choice_study',
                         'women_study_department',
                         'women_work_sector',
                         'young_evenings'                   
                         ]
            self.x_context = x_context
            self.e_p_context = e_p_context
            self.e_f_context = e_f_context
            self.agenda = agenda
            #self.agenda = ['<topic>', '<money>', '<gender>']
            #print (self.scripts)
            self.script = [s for s in self.scripts if self.agenda[0].find(s) != -1][0]

    #x_context = 'this shows gender pay gap'.split()
    x_context = 'the chart shows gender pay gap'.split()
    e_p_context = ['Story_Begin_gender_pay_gap'] * 22 + ['<topic>_gender_pay_gap\n']# ['<Evoking_gender_pay_gap>\n']
    #e_f_context = ['<Evoking_gender_pay_gap>\n'] * 22 #+ #['ScrEv_wash']
    e_f_context = ['<topic>_gender_pay_gap\n'] * 22 + ['<x_axis_label_Scnd_highest_value>\n']#+ #['ScrEv_wash']

    # agenda includes the events to be instantiated. It begins with the last event that was instantiated
    # in the seed.
    agenda_gender = list([#'Story_Begin_gender_pay_gap\n',
                         '<topic>_gender_pay_gap\n',
                         '<x_axis_label_highest_value>_gender_pay_gap\n', 
                         '<y_axis_highest_value>\n', 
                         '<topic_related_property>_gender_pay_gap\n', 
                         '<y_axis>_gender_pay_gap\n', 
                         '<x_axis_labels>_gender_pay_gap\n', 
                         '<order_Scnd>\n', 
                         '<x_axis_label_Scnd_highest_value>_gender_pay_gap\n', 
                         '<x_axis_label_least_value>_gender_pay_gap\n', 
                         '<y_axis_least_value>\n',
                         '<y_axis_highest_value_val>\n', 
                         '<y_x_comparison>\n', 
                         '<y_axis_trend>\n', 
                         '<y_axis_least_value_val>\n',
                         '<y_axis_Scnd_highest_val>\n', 
                         '<y_axis_inferred_value>\n', 
                         '<x_axis>_gender_pay_gap\n', 
                         '<y_axis_approx>\n',
                         #'<y_axis_trend_down>\n',
                         '<final_label_left>\n',
                         'Story_End_gender_pay_gap'
                         ])
    #agenda_money = list(['<gender>'])
    Sample_Seed_gender = Seed(x_context, e_p_context, e_f_context, agenda_gender)

    Seeds = [Sample_Seed_gender]