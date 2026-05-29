import os
import janus_swi as janus
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "f1_kb.pl")

def load_kb():
    if not os.path.exists(KB_PATH):
        raise FileNotFoundError(f"Could not find {KB_PATH}")
    janus.query_once(f"consult('{KB_PATH}')")
    #print(f"Knowledge Base Loaded: {KB_PATH}")

def gpt4_semantic_parser(user_question):
    print(f"Translating question: '{user_question}'")
    
    prompt = f"""
    You are a logic translator.
    Translate the question into a valid Prolog query using ONLY these predicates:
    - driver(Name, Team).
    - teammates(Driver1, Driver2).

    Rules:
    - Names must be lowercase and use underscores (such as lewis_hamilton).
    - End the query with a period.
    
    Examples:
    Input: Is Lewis Hamilton a teammate of Charles Leclerc?
    Output: teammates(lewis_hamilton, charles_leclerc).

    Input: {user_question}
    Output:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0 
    )
    
    logic_query = response.choices[0].message.content.strip().rstrip('.')
    return logic_query

def run_symbolic_prover(prolog_query):
    
    print(f"Generated Logic: {prolog_query}")
    
    try:
        with janus.query(prolog_query) as q:
            results = list(q)
            
            if not results:
                return "False"
            
            if results and isinstance(results[0], dict) and results[0]:
                answers = [str(res[list(res.keys())[0]]) for res in results]
                return f"{', '.join(set(answers))}"
            
            
    except Exception as e:
        return f"Error: ({e})"

def linc_pipeline(question):
    logic_code = gpt4_semantic_parser(question)
    
    final_answer = run_symbolic_prover(logic_code)
    
    print(f"LINC Result: {final_answer}\n")

if __name__ == "__main__":
    load_kb()
        
    # Tests
    linc_pipeline("Is Lewis Hamilton a driver for Ferrari?")
    linc_pipeline("Is Charles Leclerc a teammate of Max Verstappen?")    
    linc_pipeline("Does Kimi Antonelli drive for Mercedes and is he teammates with Lewis Hamilton?")
