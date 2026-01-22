# Cloud LLM Setup Guide

## Overview

JARVIS now supports both OpenAI (ChatGPT) and Google Gemini Pro APIs. You can use either or both, with automatic fallback.

## Setup

### 1. Get API Keys

#### OpenAI (ChatGPT)
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)

#### Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### 2. Set Environment Variables

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY = "sk-your-openai-key-here"
$env:GEMINI_API_KEY = "your-gemini-key-here"
```

#### Windows (Command Prompt)
```cmd
set OPENAI_API_KEY=sk-your-openai-key-here
set GEMINI_API_KEY=your-gemini-key-here
```

#### Linux/macOS
```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
export GEMINI_API_KEY="your-gemini-key-here"
```

#### Permanent Setup (Linux/macOS)
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
export GEMINI_API_KEY="your-gemini-key-here"
```

### 3. Configure JARVIS

Edit `config_pi.py`:
```python
# Cloud LLM Settings
PREFER_CLOUD_LLM = True  # Use cloud LLM if available
OPENAI_MODEL = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper
GEMINI_MODEL = "gemini-pro"
```

### 4. Install Dependencies

```bash
pip install openai google-generativeai
```

Or update requirements:
```bash
pip install -r requirements_pi.txt
```

## Usage

### Automatic Selection

JARVIS will automatically:
1. Use cloud LLM if `PREFER_CLOUD_LLM = True` and API keys are set
2. Fall back to local Ollama if cloud is unavailable
3. Prefer OpenAI if both are available (unless configured otherwise)

### Manual Selection

```python
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM

# Setup manager
manager = CloudLLMManager()

# Add OpenAI
openai_llm = OpenAILLM(api_key="sk-...", model="gpt-4")
manager.add_provider('openai', openai_llm, set_default=True)

# Add Gemini
gemini_llm = GeminiLLM(api_key="...", model="gemini-pro")
manager.add_provider('gemini', gemini_llm)

# Use specific provider
llm = manager.get_provider('openai')  # or 'gemini'
response = llm.chat("Hello!")
```

## Models Available

### OpenAI
- `gpt-4` - Most capable (default)
- `gpt-4-turbo` - Faster GPT-4
- `gpt-3.5-turbo` - Faster and cheaper

### Gemini
- `gemini-pro` - Standard model (default)
- `gemini-pro-vision` - With vision capabilities

## Cost Considerations

### OpenAI Pricing (as of 2024)
- GPT-4: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- GPT-3.5-turbo: ~$0.0015 per 1K input tokens, ~$0.002 per 1K output tokens

### Gemini Pricing (as of 2024)
- Free tier: 60 requests/minute
- Pro: Check current pricing

**Tip**: Use `gpt-3.5-turbo` for faster/cheaper responses, or `gpt-4` for best quality.

## Testing

### Test OpenAI
```python
from llm.cloud_llm import OpenAILLM
import os

llm = OpenAILLM(api_key=os.getenv('OPENAI_API_KEY'))
if llm.check_available():
    response = llm.chat("Hello!")
    print(response)
```

### Test Gemini
```python
from llm.cloud_llm import GeminiLLM
import os

llm = GeminiLLM(api_key=os.getenv('GEMINI_API_KEY'))
if llm.check_available():
    response = llm.chat("Hello!")
    print(response)
```

## Streaming

Both providers support streaming:

```python
# OpenAI streaming
for chunk in openai_llm.stream_chat("Tell me a story"):
    print(chunk, end='', flush=True)

# Gemini streaming
for chunk in gemini_llm.stream_chat("Tell me a story"):
    print(chunk, end='', flush=True)
```

## Troubleshooting

### "API key not set"
- Check environment variables: `echo $OPENAI_API_KEY`
- Verify keys are correct
- Restart JARVIS after setting variables

### "API error"
- Check internet connection
- Verify API key is valid
- Check API quota/limits
- Review error message in logs

### "Provider not found"
- Ensure API keys are set
- Check `check_available()` returns True
- Verify dependencies are installed

## Best Practices

1. **Use environment variables** - Never hardcode API keys
2. **Monitor usage** - Set up billing alerts
3. **Use caching** - JARVIS caches responses automatically
4. **Fallback enabled** - Keep local Ollama as backup
5. **Rate limiting** - Be aware of API rate limits

## Security

- **Never commit API keys** to git
- **Use .env file** for local development
- **Rotate keys** periodically
- **Monitor usage** for unauthorized access

## Example .env File

Create `.env` in project root:
```
OPENAI_API_KEY=sk-your-key-here
GEMINI_API_KEY=your-key-here
```

Then load with:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

**Enjoy powerful cloud LLM capabilities with JARVIS!**
