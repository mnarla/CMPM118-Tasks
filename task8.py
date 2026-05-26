import os
import janus_swi as janus
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "f1_kb2.pl") # my kb from previous tasks but with more facts and rules

# load the prolog KB into janus
def load_knowledge_base():
    if not os.path.exists(KB_PATH):
      #  print(f"couldn't find the KB file at {KB_PATH}")
        return
    janus.query_once(f"consult('{KB_PATH}')")
   # print("loaded f1_kb2.pl into prolog ok")

# basic RAG that scans the .pl file for lines that match keywords in the question
def get_relevant_context(user_query):
    matches = []
    keywords = user_query.lower().split()

    with open(KB_PATH, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        for kw in keywords:
            if len(kw) > 3 and kw in line.lower():
                matches.append(line)
                break  

    if not matches:
        return "none"

    return "\n".join(matches[:6])

# use langchain to translate the natural language question into a prolog query
def translate_to_prolog(question, rag_context):
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.0)

    prompt_template = PromptTemplate(
        input_variables=["rag_context", "question"],
        template="""
You are helping translate a natural language question into a Prolog query.

Here are some relevant facts/rules from the knowledge base to help you pick the right predicates:
{rag_context}

Rules:
- return ONLY the prolog query, nothing else
- no markdown, no backticks, no explanation
- use lowercase with underscores for names and teams (ex. lewis_hamilton, red_bull, aston_martin)

Question: {question}
Prolog Query:"""
    )

    # put the prompt into the model, and this is the langchain chain pattern
    chain = prompt_template | model
    response = chain.invoke({"rag_context": rag_context, "question": question})

    # clean up the output
    query = response.content.strip().replace("`", "")
    if query.endswith("."):
        query = query[:-1]

    return query


# run the full pipeline and print an inference trace
def run_query(user_question):
    print(f"\nquestion: {user_question}")

    context = get_relevant_context(user_question)
    prolog_query = translate_to_prolog(user_question, context)
    print(f"prolog query: {prolog_query}.")

    try:
        results = list(janus.query(prolog_query))
        is_true = len(results) > 0

        print(f"result: {str(is_true).upper()}")
        print("inference trace:")

        if is_true:
            print("fact or rule matched in KB")
            if results and isinstance(results[0], dict):
                for i, binding in enumerate(results):
                    for var, val in binding.items():
                        if var != "truth":  
                            print(f"[{i+1}] {var} = {val}")
        else:
            print("no matching facts or rules found, query failed")

    except Exception as e:
        print(f"result: ERROR")
        print(f"prolog threw an exception: {e}")


if __name__ == "__main__":
    load_knowledge_base()
    # tests
    run_query("Is Ferrari a works team?")
    run_query("Is McLaren a customer team?")
    run_query("Are Lewis Hamilton and Max Verstappen rivals?")
    run_query("Is George Russell a race winner?")
    run_query("Is Charles Leclerc a teammate of Lewis Hamilton?")
    run_query("Is Max Verstappen a veteran driver?")