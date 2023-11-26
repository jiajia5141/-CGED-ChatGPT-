import openai
import time
proxies = {'http':"http://127.0.0.1:7890", 'http':"http://127.0.0.1:7890"}
openai.proxy = proxies
openai.api_key = 'YOUR API-KEY'
import pandas as pd
def get_data():
    df = pd.read_excel('C:/Users/HP/Desktop/data.xlsx')
    sentences = []
    for sent in df['sent']:
        sent = sent.replace('\n', ' ').strip()
        sentences.append(sent)
    return sentences
def prompt_design_fn(sent):
    instruction = 'Please modify the grammatical errors in the following Chinese sentence according to the Minimal Edit principle\
 and output the correct version without giving reasons:\n'
    prompt = instruction + sent
    return prompt
def chatgpt_fn(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        result = response["choices"][0]["message"]["content"]
        return result
    except Exception as e:
        print(e)
        return 'broken'
def process_fn(sentences):
    result = []
    for i in range(len(sentences)):
        sent = sentences[i]
        prompt = prompt_design_fn(sent)
        chatgpt_output = chatgpt_fn(prompt)
        while chatgpt_output == 'broken':
            time.sleep(10)
            chatgpt_output = chatgpt_fn(prompt)
        else:
            print(f'Inferring: [{i + 1}/{len(sentences)}]')
            print(prompt)
            print(f'ChatGPT Output: {chatgpt_output}')
            print('\n')
            temp_dict = {
                '原句': sent,
                'ChatGPT纠错结果': chatgpt_output
            }
            result.append(temp_dict)
    result = pd.DataFrame(result)
    result.to_excel('C:/Users/HP/Desktop/chatgpt纠错.xlsx')
if __name__ == '__main__':
    sentences = get_data()
    process_fn(sentences)




