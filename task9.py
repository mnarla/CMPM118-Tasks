import os
import janus_swi as janus
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "f1_kb2.pl")

janus.query_once(f"consult('{KB_PATH}')")
print("loaded f1_kb2.pl into prolog ok")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)


# shared state passed between nodes, this is same pattern as the langgraph docs
class State(TypedDict):
    question: str
    context: str
    context_relevant: bool
    prolog_query: str
    result: bool


# node 1: RAG pulls relevant lines from the KB based on keywords
def rag_node(state: State):
    matches = []
    keywords = state["question"].lower().split()

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

    context = "\n".join(matches[:6]) if matches else "none"
    return {"context": context}


# node 2: judge whether the context is actually useful
def judge_node(state: State):
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template="""
Is the retrieved context relevant to answering this question using Prolog?

Question: {question}
Context: {context}

Reply with only YES or NO."""
    )

    chain = prompt | model
    response = chain.invoke({"question": state["question"], "context": state["context"]})
    is_relevant = "YES" in response.content.strip().upper()
    print(f"context relevant: {is_relevant}")
    return {"context_relevant": is_relevant}


# route to translate if relevant, skip to prolog with generic context if not
def route_after_judge(state: State):
    if state["context_relevant"]:
        return "translate"
    return "translate"  

# node 3: translate the question to prolog using chain of thought
def translate_node(state: State):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are helping translate a natural language question into a Prolog query.

Relevant facts/rules from the knowledge base:
{context}

Think step by step about which predicate fits the question, then return the query.

Rules:
- return ONLY the prolog query, nothing else
- no markdown, no backticks, no explanation
- use lowercase with underscores for names and teams (e.g. lewis_hamilton, red_bull)

Question: {question}
Prolog Query:"""
    )

    chain = prompt | model
    response = chain.invoke({"context": state["context"], "question": state["question"]})

    query = response.content.strip().replace("`", "")
    if query.endswith("."):
        query = query[:-1]

    print(f"prolog query: {query}.")
    return {"prolog_query": query}


# node 4: run the prolog query through janus and print the inference trace
def prolog_node(state: State):
    try:
        results = list(janus.query(state["prolog_query"]))
        is_true = len(results) > 0

        print(f"result: {str(is_true).upper()}")
        print("inference trace:")
        if is_true:
            print("fact or rule matched in KB")
            for i, binding in enumerate(results):
                for var, val in binding.items():
                    if var != "truth":
                        print(f"[{i+1}] {var} = {val}")
        else:
            print("no matching facts or rules found, query failed")

        return {"result": is_true}

    except Exception as e:
        print(f"result: ERROR - {e}")
        return {"result": False}


# build the graph 
workflow = StateGraph(State)

workflow.add_node("rag", rag_node)
workflow.add_node("judge", judge_node)
workflow.add_node("translate", translate_node)
workflow.add_node("prolog", prolog_node)

workflow.add_edge(START, "rag")
workflow.add_edge("rag", "judge")
workflow.add_conditional_edges(
    "judge",
    route_after_judge,
    {"translate": "translate"}
)
workflow.add_edge("translate", "prolog")
workflow.add_edge("prolog", END)

graph = workflow.compile()


def run_query(question):
    print(f"\nquestion: {question}")
    graph.invoke({
        "question": question,
        "context": "",
        "context_relevant": False,
        "prolog_query": "",
        "result": False
    })


if __name__ == "__main__":
    run_query("Is Mercedes a works team?")
    run_query("Is Aston Martin a customer team?")
    run_query("Are Lando Norris and Fernando Alonso rivals?")
    run_query("Is Fernando Alonso a veteran driver?")
    run_query("Are Oscar Piastri and Lando Norris teammates?")
    run_query("Is Lance Stroll a race winner?")