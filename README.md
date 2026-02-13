This repository is edited version of Ego-R1 project.

original github : https://github.com/egolife-ai/Ego-R1?tab=readme-ov-file#-installation

# What have I done
- added client selection logic, now we can chose whether to use AzureOpenAI or OpenAI.
- added simple test script for RAG search, now we can test only RAG search solely.

# To use
## RAG search tool
- export your openai key

```
export OPENAI_API_KEY=sk-...
```
- download dataset from huggingface (only egolife)
```
hf download Ego-R1/h-rag_database \
  --repo-type dataset \
  --include "egolife/**" \
  --local-dir ./h-rag_database_egolife
```

- change data path (put path of "egolife" folder)

`data_dir:` of egolife.yaml

- set env
```
pip install -e .
```

- start api
```
python api/rag/api_for_egolife.py
```

- test with Ego-R1-Agent/test_rag.py