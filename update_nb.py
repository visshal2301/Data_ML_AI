import json

path = r"d:\Padai\Python\Krish\workshop\level\level-2\langchain_learn\CH2\4_conditional_chains.ipynb"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for cell in data.get("cells", []):
    if cell.get("cell_type") == "code":
        src_blocks = cell.get("source", [])
        src = "".join(src_blocks)
        if "chain_linkedin" in src or "conditional_chain = RunnableBranch(" in src:
            if "movie_reviewer" not in src:
                new_src = [
                    "from langchain_core.runnables import RunnableBranch\n",
                    "conditional_chain = RunnableBranch(\n",
                    "    (lambda x: \"positive\" in x, movie_reviewer),\n",
                    "     movie_chain_runnable\n",
                    ")\n",
                    "\n",
                    "final_orchestrator = prompt_template | llm_structured_output | pydantic_json_lambda | conditional_chain"
                ]
                cell["source"] = new_src

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1)

print("done")
