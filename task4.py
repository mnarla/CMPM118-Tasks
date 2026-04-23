import os
import janus_swi as janus

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_kb.pl")
janus.query_once(f"consult('{KB_PATH}')")

def check_teammates(driver_name):
    print(f"Finding teammates for: {driver_name}")

    query_str = f"teammates({driver_name}, Teammate)"

    with janus.query(query_str) as q:
        found = False
        for res in q:
            print(f"-> {res['Teammate']} is a teammate of {driver_name}.")
            found = True
        if not found:
            print("-> No teammates found in the database.")

if __name__ == "__main__":
    #Tests
    check_teammates("charles_leclerc")
    check_teammates("max_verstappen")
    check_teammates("kimi_antonelli")
    