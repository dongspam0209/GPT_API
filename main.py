from openai import OpenAI
from openai import RateLimitError
import backoff
import pandas as pd

client=OpenAI(api_key='your openai api key')

input_csv_path='input.csv'
output_csv_path='output.csv'
column_to_translate='anonym'

df=pd.read_csv(input_csv_path)

@backoff.on_exception(backoff.expo,RateLimitError)
def translate_text(text):
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role" : "system", "content" : "너는 영어와 한글에 능통한 전문 간호사야."},
            {"role" : "user", "content" : "업로드한 파일을 영어로 변역해줘."},    
            {"role" : "assistant", "content" : "Yes."},       
            {"role" : "user", "content" : text}  
        ],
    )
    translate_result=response.choices[0].message.content
    return translate_result
    

for idx,row in df.iterrows():
    try:
        translated_text=translate_text(row[column_to_translate])
        df.at[idx,'GPT-3.5_translation_result']=translated_text
    except Exception as e:
        print(f"error in {idx}:{e}")
    
    if idx%10==0:
        df.to_csv(output_csv_path,index=False)
        print(f"saved at {idx}")

df.to_csv(output_csv_path,index=False)
print("translate completed")