from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from aiconfig import Config
from langchain.messages import HumanMessage, SystemMessage, AIMessage



config = Config()


llm = HuggingFaceEndpoint(
repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
task="text-generation",
max_new_tokens=512,
do_sample=False,
temperature=0.9,
huggingfacehub_api_token=Config.get_huggingFaceKey()
)
print("Model loaded successfully.", Config.get_huggingFaceKey())

messages = [
    SystemMessage(content="You are my teacher. and you will answer the question. " \
    " If you dont know the answer, say I will get back soon" )
]

chat_model = ChatHuggingFace(llm=llm) 


while True:
    user_input = input("User:  ")
    messages.append(HumanMessage(content=user_input)    )
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        exit(0)

   
    result = chat_model.invoke(messages)
    messages.append(AIMessage(content=result.content))
    print(  result.content )
  #  messages.append(result)



#HuggingFaceKey = config.get_huggingFaceKey()
#llm = ChatHuggingFace(hf_api_key=HuggingFaceKey, model_id="meta-llama/Llama-3.2-1B")

print(result)
