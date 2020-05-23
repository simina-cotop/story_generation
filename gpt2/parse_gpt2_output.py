import xml.etree.cElementTree as ET
from typing import List, Dict, Tuple, Set, Optional, cast
from yattag import Doc
import sys
import re

def create_human_file(sentence: str, filename: str, folder: str) -> None:
    with open('../summarizer-master/rouge/' + folder + '/models/'+ filename + '.txt', 'w') as f:
        f.write(sentence)
        

def create_gpt2_file(sentence: str, filename: str, folder: str) -> None:
    with open('../summarizer-master/rouge/' + folder + '/systems/' + filename + '.txt', 'w') as f:
        f.write(sentence)


def create_settings_template() -> str:
    return  """<EVAL ID="{eval_id}">
<PEER-ROOT>
{peer_root}
</PEER-ROOT>
<MODEL-ROOT>
{model_root}
</MODEL-ROOT>
<INPUT-FORMAT TYPE="SPL">
</INPUT-FORMAT>
<PEERS>
{peers}
</PEERS>
<MODELS>
{models}
</MODELS>
</EVAL>

"""

def parse_algo_file(filename:str) -> List[str]:
    path = '../model8/outputs/gender_pay_gap_beam_3_10epochs/' + filename
    with open(path, 'r') as f:
        newer_data: List[str] = []
        data: str = f.read()
        # Remove the epoch-related information
        data = data.split('===============================')[0]
        new_data: List[str] = re.split('-- TEXT [\d]* ---', data)
        # Remove script name
        new_data = new_data[1:]
        # Remove '\n'
        for el in new_data:
            newer_data.append(el)
    return newer_data


def create_settings_xml_gpt2(summaries: ET.Element, peer_root: str, model_root: str) -> None:
    template = create_settings_template()

    for settings_id, chart in enumerate(summaries):
        for eval_id, original in enumerate(chart):
            settings_content = """<ROUGE-EVAL version="1.55">\n"""
            models = []
            for idx in range(23):
                models.append(f"""<M ID="{idx}">original_{settings_id}_{idx}.txt</M>""")
            model = '\n'.join(models)

            peers = []
            for peer_id, gpt2 in enumerate(original):
                peers.append(f"""<P ID="{settings_id}_{eval_id}_{peer_id}">gpt2_{settings_id}_{eval_id}_{peer_id}.txt</P>""")
            peer = '\n'.join(peers)

            settings_content += template.format(eval_id=eval_id, peer_root=peer_root, model_root=model_root, peers=peer, models=model)
    
            settings_content += """</ROUGE-EVAL>\n"""
            with open(f"../summarizer-master/rouge/gpt2_results/settings_{settings_id}_{eval_id}.xml", "w+") as settings:
                settings.write(settings_content)


def create_settings_xml_beam3(summaries: ET.Element, peer_root: str, model_root: str) -> None:
    template = create_settings_template()

    for settings_id, chart in enumerate(summaries):
        print(repr(chart.attrib['name']))
        if chart.attrib['name'] == 'gender_pay_gap.txt\n':
            print("HERE\n")
            for eval_id, original in enumerate(chart):
                settings_content = """<ROUGE-EVAL version="1.55">\n"""
                models = []
                for idx in range(23):
                    models.append(f"""<M ID="{idx}">original_{settings_id}_{idx}.txt</M>""")
                model = '\n'.join(models)

                peers = []
                #all_descriptions = parse_algo_file('')
                #for peer_id, gpt2 in enumerate(original):
                for idx in range(41):
                    peers.append(f"""<P ID="{settings_id}_{eval_id}_{idx}">beam3_{settings_id}_{eval_id}_{idx}.txt</P>""")
                peer = '\n'.join(peers)

                settings_content += template.format(eval_id=eval_id, peer_root=peer_root, model_root=model_root, peers=peer, models=model)
        
                settings_content += """</ROUGE-EVAL>\n"""
                with open(f"../summarizer-master/rouge/beam3_results/settings_{settings_id}_{eval_id}.xml", "w+") as settings:
                    settings.write(settings_content)




if __name__ == '__main__':
    ## GPT2-related; it is commented out since I do not want to run it again
    '''summaries = ET.parse('gpt_output.xml').getroot()
    create_settings_xml_gpt2(summaries, "./gpt2_results/systems/", "./gpt2_results/models/")
    for chart_id, chart in enumerate(summaries):
        original_counter: int = 0
        for original in chart:
            gpt2_counter: int = 0
            original_filename = 'original_' + str(chart_id) + '_' + str(original_counter)
            #print("of=",original_filename)
            create_human_file(cast(str,original.text), original_filename)
            
            for gpt2 in original:
                #print(gpt2.tag, gpt2.attrib)
                gpt2_filename = 'gpt2_' + str(chart_id) + '_' + str(original_counter) + '_' + str(gpt2_counter)
                #print("gf=", gpt2_filename)
                create_gpt2_file_gpt2(cast(str,gpt2.text), gpt2_filename)
                gpt2_counter += 1
            original_counter += 1 '''

    # Can only do this for gender_pay_gap
    #for algo in ['beam3', 'beam5', 'beam10', 'nucleus']:
       #for epoch in ['10','20','50','100','200']:
    summaries = ET.parse('gpt_output.xml').getroot()
    create_settings_xml_beam3(summaries, "./beam3_results/systems/", "./beam3_results/models/")
    for chart_id, chart in enumerate(summaries):
        original_counter: int = 0
        for original in chart:
            original_filename = 'original_' + str(chart_id) + '_' + str(original_counter)
            #print("of=",original_filename)
            create_human_file(cast(str,original.text), original_filename, 'beam3_results')
            original_counter += 1
            
    all_descriptions = parse_algo_file('samples_gender_pay_gap_beam_3_10epochs')
    for idx, desc in enumerate(all_descriptions):
        beam3_filename = 'gpt2_' + str(chart_id) + '_' + str(original_counter) + '_' + str(idx)
        create_gpt2_file(desc, beam3_filename, 'beam3_results')