from langchain.llms import OpenAI
from langchain.prompts import ProjectTemplate
from langchain.chains import  LLMChain
from dotenv import load_dotenv
from langchain.agents import load_tools, initialize_agent, AgentType
load_dotenv()

def generate_names(gender, hair_color):
    prompt_template_name = ProjectTemplate(
        input_variables = ['gender', 'hair_color'],
        template=[f"My friend is having a baby {gender} with {hair_color} hair and they need help naming it. Can you suggest 5 badass names for them?"]
    )
    llm = OpenAI(temperature=0.7)
    name_chain = LLMChain(llm=llm, prompt = prompt_template_name, output_key = 'baby_name')
    response = name_chain({'gender': gender, 'hair_color': hair_color})
    return response

def langchain_agent():
    llm = OpenAI(temperature=0.7)
    tools = load_tools(['wikipedia', 'llm-math'], llm = llm)
    agent = initialize_agent(
        tools, llm, agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True
    )
    result = agent.run(
        "What is the average gestation time for a baby?",
        "Multiply that by 42"
    )
    print(result)

if __name__ == '__main__':
    langchain_agent()
