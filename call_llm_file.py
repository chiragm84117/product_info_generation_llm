from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate

def get_plm_result(data,count):
    api_key = "AIzaSyC6dRYZHV8VaPCZ-qBRZHNEYu5Lgtt4AWg"
    if(count == 1):
        temp = 0.07
    elif(count == 2):
        temp = 0.5
    llm = GooglePalm(google_api_key=api_key, temperature=temp)

    template1 = '''this is my knowledge array {data} according to the learning from the knowledge array give me the one best  possible name of the product in 2 or 3 words and return only name nothing else'''
    template2 = '''this is my knowledge array {data} according to the learning from the knowledge array give me the approximate price of the product and return only the price in numbers once nothing else , if price is not found return Null'''
    template3 = '''this is my knowledge array {data} according to the learning from the knowledge array give me the one best suited color of the product , also return just colour in one word if not found return NOT FOUND'''
    template4 = '''this is my knowledge array {data} according to the learning from the knowledge array write the best possible description of the product in minimun 40 words and maximun 60 words in your words and return only the description'''

    prompt1 = PromptTemplate(input_variables = ['data'],
                            template = template1,
                            )
    prompt2 = PromptTemplate(input_variables=['data'],
                             template=template2,
                             )
    prompt3 = PromptTemplate(input_variables=['data'],
                             template=template3,
                             )
    prompt4 = PromptTemplate(input_variables=['data'],
                             template=template4,
                             )

    response1 = llm(prompt1.format(data=data))
    response2 = llm(prompt2.format(data=data))
    response3 = llm(prompt3.format(data=data))
    response4 = llm(prompt4.format(data=data))

    response = "Name of product :- " + response1 + "\nProduct price :- " + response2 + "\nColour :- " + response3 + "\nDescription :- " + response4
    return response

def call_llm(data,count):
    if count == 1:
        text1 = get_plm_result(data,count)
        return text1
    elif count == 2:
        text2 = get_plm_result(data,count)
        return text2

