# KIE Document Extractor — Custom GPT

Artifacts for publishing a **Custom GPT** on the [OpenAI GPT Store](https://chatgpt.com/gpts) that lets ChatGPT users extract structured data from documents without writing code.

## What's inside

```
custom-gpt/
├── README.md              # This file — setup instructions
├── openapi.yaml           # OpenAPI 3.1 spec for the extractDocument action
└── system_prompt.md       # GPT system instructions + example schemas
```

## How it works

```
ChatGPT user                Custom GPT                    KIE API
─────────────         ─────────────────────         ──────────────────
 Upload PDF  ───────▶  Build extraction schema  ──▶  POST /v1/extract
             ◀───────  Format & present results ◀──  { extracted JSON }
```

The Custom GPT acts as a conversational front-end: it converts the user's natural-language request into a structured schema, base64-encodes the uploaded document, calls your KIE extraction API via the OpenAPI action, and formats the results as a readable table.

## Setup (one-time, ~10 minutes)

### Prerequisites

- A [ChatGPT Plus, Team, or Enterprise](https://openai.com/chatgpt/pricing/) subscription (required to create GPTs).
- Your KIE API deployed behind HTTPS (e.g. `https://api.dillydally.dev/v1/extract`).

### Steps

1. **Go to the GPT builder**

   Visit [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor) or click **+ Create** on the [GPT Store](https://chatgpt.com/gpts).

2. **Configure the GPT**

   | Field | Value |
   |-------|-------|
   | **Name** | KIE Document Extractor |
   | **Description** | Extract structured data from invoices, receipts, tax forms, and more. Upload a document and tell me what fields you need. |
   | **Instructions** | Paste the contents of [`system_prompt.md`](system_prompt.md) |

3. **Add the Action**

   - Click **Create new action**.
   - Under **Authentication**, select **None** (or configure API key auth if your endpoint requires it).
   - In the **Schema** box, paste the contents of [`openapi.yaml`](openapi.yaml).
   - Verify the action preview shows `extractDocument` under **Available actions**.

4. **Upload knowledge files** (optional)

   Upload [`system_prompt.md`](system_prompt.md) as a knowledge file so the GPT can reference the example schemas directly when helping users.

5. **Test**

   Use the **Preview** panel to upload a sample document and ask the GPT to extract fields. Verify the action fires and results appear correctly.

6. **Publish**

   - Click **Save** → choose **Everyone** to publish to the GPT Store, or **Only people with a link** for limited access.
   - Share the link or wait for it to appear in the GPT Store search.

## Updating the server URL

If your API endpoint changes, edit the `servers` block in `openapi.yaml`:

```yaml
servers:
  - url: https://your-new-domain.com
    description: Production
```

Then re-paste the updated spec in the GPT builder's Action schema.

## Authentication (optional)

If your KIE API requires an API key, update the action in the GPT builder:

1. Under **Authentication**, select **API Key**.
2. Choose **Custom Header** and set the header name (e.g. `Authorization`).
3. Enter your API key value.

The key is stored securely by OpenAI and sent with every action request.

## Limitations

- **File size:** ChatGPT's file upload limit applies (~512 MB). Very large documents may time out.
- **Base64 encoding:** The GPT must base64-encode uploaded files before calling the action. For very large files, this may be slow.
- **Rate limits:** Subject to both ChatGPT's and your KIE API's rate limits.

## Related integrations

| Integration | Audience | Directory |
|-------------|----------|-----------|
| Custom GPT (this) | Non-developers via ChatGPT | `custom-gpt/` |
| MCP Server | Claude.ai / Cursor / Claude Code | [`mcp-server/`](../mcp-server/) |
| OpenAI Function | Developers using the OpenAI SDK | [`openai-function/`](../openai-function/) |
| LangChain Tool | Developers using LangChain | [`langchain-tool/`](../langchain-tool/) |
| Claude Skill | Claude Code users | [`claude-skill/`](../claude-skill/) |
