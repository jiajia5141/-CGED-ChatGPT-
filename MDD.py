import pandas as pd
from ltp import LTP
ltp = LTP()
def get_data():
    df = pd.read_excel('C:/Users/HP/PycharmProjects/依存/data2.xlsx')
    sentences = []
    for sent in df['sent']:
        sent = sent.replace('\n', ' ').strip()
        sentences.append(sent)
    return sentences

def dep_dist(sent):
    output = ltp.pipeline(sent, tasks=['cws', 'pos', 'dep'])
    dep = output.dep
    dependency_position = dep['head']
    labels = dep['label']
    target_element = 'WP'
    punctuation_indices = [i for i, x in enumerate(labels) if x == 'WP']
    total_distance = 0
    total_words = len(dependency_position)
    for i, position in enumerate(dependency_position):
        if i in punctuation_indices:
            continue
        if position == 0:
            continue
        distance = abs(i + 1 - position)
        total_distance += distance
    average_distance = total_distance / (total_words - len(punctuation_indices) - 1)
    return average_distance
def process_fn(sentences):
    result = []
    for i in range(len(sentences)):
        sent = sentences[i]
        mean_dep_dist = dep_dist(sent)
        print(f'Inferring: [{i + 1}/{len(sentences)}]')
        print(f'平均依存距离: {mean_dep_dist}')
        print('\n')
        temp_dict = {
            '原句': sent,
            '平均依存距离': mean_dep_dist
         }
        result.append(temp_dict)
    result = pd.DataFrame(result)
    result.to_excel('C:/Users/HP/Desktop/依存距离.xlsx')

if __name__ == '__main__':
    sentences = get_data()
    process_fn(sentences)