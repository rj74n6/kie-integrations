# KIE Document Extractor — LangChain Tool

A [LangChain Tool](https://python.langchain.com/docs/concepts/tools/) that wraps the KIE document extraction API for use in LangChain agents and chains.

## Installation

```bash
uv sync --package kie-langchain
```

## Usage

### With a LangGraph agent

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from kie_langchain import KIEExtractDocumentTool

llm = ChatOpenAI(model="gpt-4o")
tools = [KIEExtractDocumentTool()]

agent = create_react_agent(llm, tools)

result = agent.invoke({
    "messages": [("user", "Extract the vendor and total from invoice.pdf")]
})
```

### Direct invocation

```python
from kie_langchain import KIEExtractDocumentTool

tool = KIEExtractDocumentTool()

# Sync
result = tool.invoke({
    "document_path": "invoice.pdf",
    "schema": {"vendor_name": "string", "total_amount": "number"},
})

# Async
result = await tool.ainvoke({
    "document_path": "invoice.pdf",
    "schema": {"vendor_name": "string", "total_amount": "number"},
})
```

## Exports

| Name | Description |
|------|-------------|
| `KIEExtractDocumentTool` | LangChain `BaseTool` subclass with sync and async support |
| `ExtractDocumentInput` | Pydantic input schema (used as `args_schema`) |

### Input schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `document_path` | `str` | Yes | Path to the document (PDF or image) |
| `schema` | `dict` | Yes | JSON schema defining the fields to extract |
| `model` | `str \| None` | No | Optional model ID for extraction |

## File structure

```
langchain-tool/
├── README.md
├── pyproject.toml
├── src/
│   └── kie_langchain/
│       ├── __init__.py
│       └── tool.py              # KIEExtractDocumentTool + input schema
└── tests/
    ├── conftest.py
    └── test_tool.py
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

## Dependencies

- `kie-core` — shared extraction client (workspace dependency)
- `langchain-core` — for `BaseTool` base class

## Testing

```bash
uv run pytest langchain-tool/tests/ -v
```
