from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from openai import BaseModel

from agent.aiconfig import Config 
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
 
from langchain_core.runnables import RunnableLambda


def llmOutput(result: str):
    return {"result": result}



output_parser = StrOutputParser()

Config = Config() 
domain_designation = "SME"
domain = "AI"

SYSTEM_MESSAGE = "You are a {domain_designation} that answers questions about {domain}."
systemPromptTemplate = SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE)

systemPromptTemplateVariables = {"domain_designation": domain_designation, "domain": domain} 
systemPromptMessage = systemPromptTemplate.format_messages(**systemPromptTemplateVariables)

humanPromptTemplate = HumanMessagePromptTemplate.from_template("how many Modules are there in {domain}?") 
humanPromptMessage = humanPromptTemplate.format_messages(**systemPromptTemplateVariables) 

llm = HuggingFaceEndpoint(
repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
task="text-generation",
max_new_tokens=512,
do_sample=False,
temperature=0.9,
huggingfacehub_api_token=Config.get_huggingFaceKey()
)

system_detail_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant that provides detailed explanation on {topic}."
)

human_detail_message = HumanMessagePromptTemplate.from_template(
    "Explain  {topic} in simple terms suitable for a beginner." 
)

detail_chat_prompt = ChatPromptTemplate.from_messages([system_detail_message, human_detail_message])

chat_model = ChatHuggingFace(llm=llm) 

detail_chain = detail_chat_prompt | chat_model

system_summary_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant that provides summary of the content strictly in bullet points."
)

human_summary_message = HumanMessagePromptTemplate.from_template(
    "Provide a summary in 5 sentences of the text below: \n {result}"
)

detail_chat_prompt = ChatPromptTemplate.from_messages([system_detail_message, human_detail_message])
summary_chat_prompt = ChatPromptTemplate.from_messages([system_summary_message, human_summary_message])


print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

entire_chain =detail_chat_prompt | chat_model | RunnableLambda(lambda x: llmOutput(x.content))  | summary_chat_prompt | chat_model | output_parser
newresult = entire_chain.invoke({"topic": "geography"})

print(newresult)