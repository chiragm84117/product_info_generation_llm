# from langchain.prompts import PromptTemplate
import google.generativeai as genAi

genAi.configure(api_key="AIzaSyDmwZiI6Ob9VA-CsfzWRGE0Bo-LE07eS0g")

def call_llm(data, count):
    if count == 1:
        temp = 0.5
    elif count == 2:
        temp = 0.7

    # Define the prompts
    prompt1 = f"This is my knowledge array {data}. According to the learning from the knowledge array, give me the one best possible name of the product in 2 or 3 words and return only the name, nothing else."
    # prompt2 = f"This is my knowledge array {data}. According to the learning from the knowledge array, give me the price of the product from that knowledge it should be just numerical value else say 'NOT FOUND'."
    prompt3 = f"This is my knowledge array {data}. According to the learning from the knowledge array, give me the one best-suited color of the product, return just the color in one word, if not found return 'NOT FOUND'."
    prompt4 = f"This is my knowledge array {data}. According to the learning from the knowledge array, write the best possible description of the product in a minimum of 10 words and a maximum of 25 words each line and there sould be excat 3 lines. Return only the description."

    # Initialize the model
    model = genAi.GenerativeModel("gemini-1.5-flash")
    generate_config = genAi.types.GenerationConfig(temperature=temp,
                                                   max_output_tokens=100,
                                                   candidate_count=1)
    # Generate responses using the specified prompts
    response1 = model.generate_content(prompt1, generation_config=generate_config)
    # response2 = model.generate_content(prompt2, generation_config=generate_config)
    response3 = model.generate_content(prompt3, generation_config=generate_config)
    response4 = model.generate_content(prompt4, generation_config=generate_config)

    # Extract text from the responses
    response = f"Name of product: {response1.text} \nColor: {response3.text}\nDescription: \n{response4.text}"
    return response,response1.text


