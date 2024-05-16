from openai import OpenAI
import pandas as pd

client=OpenAI(api_key='user api key')

input_csv_path='test.csv'
output_csv_path='translate_result.csv'
column_to_translate='emr_nsgrec'

df=pd.read_csv(input_csv_path)

def translate_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role" : "system", "content" : "너는 파일의 영어로 된 글을 한국어로 번역하는 번역가고 이 분야의 최고 전문가야."},
            {"role" : "user", "content" : "업로드한 파일을 한국어로 변역해줘"},    
            {"role" : "assistant", "content" : "Yes."},       
            {"role" : "user", "content" : text}  
        ],
    )
    translate_result=response.choices[0].message.content
    return translate_result

df['translate_result']=df[column_to_translate].apply(translate_text)

df.to_csv(output_csv_path,index=False)
print("translate completed")