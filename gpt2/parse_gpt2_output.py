import xml.etree.cElementTree as ET
from typing import List, Dict, Tuple, Set, Optional, cast
from yattag import Doc
import sys

def create_human_html(sentence: str, filename: str) -> None:
    with open('../summarizer-master/rouge/gpt2_results/models/'+ filename + '.txt', 'w') as f:
        f.write(sentence)
        

def create_gpt2_html(sentence: str, filename: str) -> None:
    with open('../summarizer-master/rouge/gpt2_results/systems/' + filename + '.txt', 'w') as f:
        f.write(sentence)

def create_settings_xml(summaries: ET.Element, peer_root: str, model_root: str) -> None:
    template = """<EVAL ID="{eval_id}">
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

    for settings_id, chart in enumerate(summaries):
        for eval_id, original in enumerate(chart):
            settings_content = """<ROUGE-EVAL version="1.55">\n"""
            # model = f"""<M ID="{eval_id}">original_{settings_id}_{eval_id}.txt</M>"""
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



if __name__ == '__main__':
    summaries = ET.parse('gpt_output.xml').getroot()
    create_settings_xml(summaries, "./gpt2_results/systems/", "./gpt2_results/models/")
    for chart_id, chart in enumerate(summaries):
        original_counter: int = 0
        for original in chart:
            gpt2_counter: int = 0
            #print(original.tag, original.attrib)
            original_filename = 'original_' + str(chart_id) + '_' + str(original_counter)
            print("of=",original_filename)
            create_human_html(cast(str,original.text), original_filename)
            
            for gpt2 in original:
                #print(gpt2.tag, gpt2.attrib)
                gpt2_filename = 'gpt2_' + str(chart_id) + '_' + str(original_counter) + '_' + str(gpt2_counter)
                print("gf=", gpt2_filename)
                create_gpt2_html(cast(str,gpt2.text), gpt2_filename)
                gpt2_counter += 1
            original_counter += 1    