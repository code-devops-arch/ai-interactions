from concurrent.futures import thread
import json
import os
 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openAIKey = os.getenv("openAIKey")

print("OpenAI Key loaded successfully:", openAIKey)

# Store temperatures for cities in a dictionary.
CITY_TEMPERATURES = {
    "New York": 15,
    "London": 10,
    "Tokyo": 20,
    "Mumbai": 30,
    "Sydney": 22,
    "Moscow": 5
    }


def getTemperature(city: str):
    """Return the temperature for a given city from the local dictionary."""
    return CITY_TEMPERATURES.get(city)



def ask_chatgpt_for_city_temperature(SYSTEM_PROMPT: str, USER_PROMPT: str = None):
    """Send a prompt to ChatGPT and let it call getTemperature to retrieve the temperature."""
 
    openai = OpenAI(api_key=openAIKey)  
    tools = [
        {
            "tool_call_id": "d8cdd56d-98e1-4dea-ae3a-2b23",
            "type": "function",
            "name": "getTemperature",
            "description": "Get the temperature for a city", 
                "parameters": {
                    "type": "object",
                    "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
              }
            
        }
    ]
    web_search_tool = [
        { "type" : "web_search"} 

    ]
 
    if SYSTEM_PROMPT == None or SYSTEM_PROMPT == "" or SYSTEM_PROMPT.strip() == "":
      
        SYSTEM_PROMPT = "You are a Temperature assistant with start, plan, action, observation and output state." \
        "Wait for the user prompt and first plan using available tools. " \
        "After planning, take action by calling the appropriate tool with the right arguments and wait for observation."     \
        "After getting the observation, update your plan and take next action until you have the final answer to the user prompt using JSON. " \
        " Dont assume any values and strictly use the available tools." \
        
        "Example:" \
        "Start" \
        '{"type": "user", "user": "what is the sum of the temperatures of Mumbai and Tokyo?"}' \
        '{"type": "plan", "plan": "I need getTemperature  get the current temperature for Mumbai."}' \
        '{"type": "action", "function getTemperature" , "input": "Mumbai"}'\
        '{"type": "observation", "observation": "30"}' \
        '{"type": "plan", "plan": " I need getTemperature to get the current temperature for Tokyo."}' \
        '{"type": "action", "function getTemperature" , "input": "Tokyo"}' \
        '{"type": "observation", "observation": "20"}' \
        '{"type": "output", "output": "The value of temperature of Mumbai and Tokyo is 50 degree Celsius."}' \
        "Available tools:" \
        "getTemperature(city: string) -> number: Get the temperature for a city"

    if SYSTEM_PROMPT == None or SYSTEM_PROMPT.strip() == "":    
        USER_PROMPT = "Which city has the maximum temprature between Sydney, Mumbai, and Tokyo? Reponse should be in JSON format only."
    messages = []
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": USER_PROMPT}) 
    Model = "gpt-5.5" 

    print("Sending prompt to ChatGPT...")
    response = None
    
    #response = openai.chat.completions.create(
    #    model=Model,
    #    messages=messages, 
    #    tools=web_search_tool 

    #) 

    response = openai.responses.create(
        model=Model,    
        tools=tools,
        input=messages
    )

    print("Response from ChatGPT:", response) 
    print("-------------------------------------------") 

    #for tool_call in response.choices[0].message.tool_calls: 
    #    functionName = tool_call.function.name
    #    functionArguments =  json.loads(tool_call.function.arguments)
    #    print(f"ChatGPT called function: {functionName} with arguments: {functionArguments}")
    #    func = globals()[functionName+""]   
    #    temp = func(functionArguments["city"])
    #    messages.append({"role": "developer", "content": '{"observation": "' + str(temp) + '"}'})

    for item in response.output:
       if item.type == "function_call":
            functionName = item.name
            functionArguments = json.loads(item.arguments).get("city")
            func = globals()[functionName+""]   
            temp = func(functionArguments)
            print(f"ChatGPT called function: {functionName} with arguments: {functionArguments} and got the result: {temp}")

            messages.append({"role": "developer", "content": '{"observation": "' + str(temp) + '"}'})
    response = openai.chat.completions.create(
        model=Model,
        messages=messages
    ) 
    finalOutput = json.loads(response.choices[0].message.content)
    print("Final Response from ChatGPT:",  finalOutput["output"])


SYSTEM_PROMPT = "You are a Temperature assistant with start, plan, action, observation and output state." \
        " Wait for the user prompt and first plan using available tools. " \
        " After planning, take action by calling the appropriate tool with the right arguments and" \
        " wait for observation if needed."     \
        " After getting the observation, update your plan and take next action until you have the " \
        " final answer to the user prompt using JSON. " \
        " Dont assume any values and strictly use the available tools." \
        " Available tools:" \
        " getTemperature(city: string) -> number: Get the temperature for a city" \
        " Wrap your response in JSON format with the output key:  Example of the output is given below as OUTPUT_EXAMPLE"  \
        ' OUTPUT_EXAMPLE : {"output": {"entity" : "Mumbai"}, {"value": "20"} }' \
        " To calulate sum , product, or difference of temprature, use the following format in your output:" \
         'OUTPUT_EXAMPLE : {"output": {"value" : "50"} }'  \
        " Dont make any assumptions if you dont find any value from the method getTemperature. Then search the web for the accurate value. " \
        " Even after that you are not able to find the value, then respond with the output as value Not Applicable. " \

print("OUTPUT_EXAMPLE:", SYSTEM_PROMPT)

USER_PROMPT = "What is the sum of the temperatures of Sydney, Moscow, Florida, and Tokyo? "
ask_chatgpt_for_city_temperature(SYSTEM_PROMPT, USER_PROMPT)