import os
import janus_swi as janus
from openai import OpenAI

client = OpenAI()

def run_experiment(text_input):
    
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Prolog translator. Given a natural language statement, output two things:\n"
                    "1. FACTS: valid SWI-Prolog facts (no rules, no comments, no markdown)\n"
                    "2. QUERY: a single Prolog query to verify the main claim\n\n"
                    "Format your response exactly like this:\n"
                    "FACTS:\n<prolog code>\nQUERY:\n<prolog query>"
                )
            },
            {"role": "user", "content": text_input}
        ]
    )

    content = response.choices[0].message.content
    facts = content.split("FACTS:")[1].split("QUERY:")[0].strip()
    query = content.split("QUERY:")[1].strip().rstrip(".")

    print(f"Facts:\n{facts}")
    print(f"Query: {query}")

    with open("temp_logic.pl", "w") as f:
        f.write(facts)

    janus.query_once("consult('temp_logic.pl')")
    result = janus.query_once(query)
    print(f"Result: {result['truth']}")


if __name__ == "__main__":
    run_experiment("Mayank likes mexican food. Mexican food is only at Stevenson dining hall today though.")