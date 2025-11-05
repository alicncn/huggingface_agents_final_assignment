# Phase 2 - Information Retrieval Tools

## ✅ Completed Tasks

### 1. Web Search Integration
- ✅ Integrated **Tavily API** for web search
- ✅ Created `web_search` tool for general web queries
- ✅ Created `web_search_wikipedia` tool for Wikipedia-specific searches
- ✅ Support for answer generation and multiple results

### 2. Document/URL Processing
- ✅ Created `read_url` tool to extract content from any webpage
- ✅ Created `extract_links` tool to get all links from a page
- ✅ Created `search_in_document` tool to find specific text with context
- ✅ Robust error handling for network issues and malformed pages

### 3. Dependencies
- ✅ Installed `tavily-python==0.5.0` for web search
- ✅ Installed `beautifulsoup4==4.12.3` for HTML parsing
- ✅ Installed `requests==2.32.3` for HTTP requests
- ✅ Installed `lxml` and `html5lib` for better HTML parsing

## 🛠️ Tools Added (5 Total)

### 1. `web_search(query, max_results=5)`
**Purpose:** Search the web using Tavily API  
**Example:** "Search for Mercedes Sosa discography"  
**Returns:** AI-generated answer + search results with titles, URLs, and snippets

### 2. `web_search_wikipedia(query, year=None)`
**Purpose:** Search Wikipedia specifically  
**Example:** "Search Wikipedia for Mercedes Sosa in 2022"  
**Returns:** Wikipedia-focused search results

### 3. `read_url(url, extract_text_only=True)`
**Purpose:** Read and extract content from any URL  
**Example:** "Read https://en.wikipedia.org/wiki/Mercedes_Sosa"  
**Returns:** Clean text content from the webpage (up to 10,000 chars)

### 4. `extract_links(url, filter_text=None)`
**Purpose:** Extract all links from a webpage  
**Example:** "Get all links from https://example.com"  
**Returns:** List of links with their text and URLs (up to 50 links)

### 5. `search_in_document(url, search_term, context_chars=200)`
**Purpose:** Find specific text in a webpage with surrounding context  
**Example:** "Search for 'award number' in https://example.com/paper.html"  
**Returns:** All occurrences with context before and after

## 🔑 Configuration Required

### Tavily API Key (Required for Web Search)

1. **Get a free API key:**
   - Visit: https://tavily.com
   - Sign up for a free account
   - Copy your API key

2. **Add to `.env` file:**
   ```
   TAVILY_API_KEY=tvly-your_actual_key_here
   ```

3. **Verify setup:**
   ```bash
   python verify_phase2.py
   ```

## 📊 Challenge Prompts Now Solvable

With Phase 2 tools, the agent can now solve:

### ✅ Prompt 1: Mercedes Sosa Albums
**Task:** Count albums released between 1990-2000  
**Solution Path:**
1. `web_search_wikipedia("Mercedes Sosa discography", 2022)`
2. `read_url(wikipedia_url)`
3. Parse content to find albums in date range

### ✅ Prompt 5: Wikipedia Nominator
**Task:** Find who nominated an article for featured status  
**Solution Path:**
1. `web_search("Wikipedia featured article nomination [article name]")`
2. `read_url(nomination_page)`
3. `search_in_document(url, "nominated by")`

### ✅ Prompt 8: Veterinarian Surname
**Task:** Find veterinarian name in online textbook  
**Solution Path:**
1. `web_search("veterinary textbook [title]")`
2. `read_url(textbook_chapter_url)`
3. Extract surname from content

### ✅ Prompt 15: NASA Award Number
**Task:** Multi-step research from news to paper  
**Solution Path:**
1. `web_search("NASA exoplanet discovery news")`
2. `extract_links(news_url, "research paper")`
3. `read_url(paper_url)`
4. `search_in_document(paper_url, "award number")`

### ✅ Prompt 16: Specimen Deposition
**Task:** Find specimen location in scientific paper  
**Solution Path:**
1. `web_search("[paper title] specimen")`
2. `read_url(paper_url)`
3. `search_in_document(paper_url, "deposited")`

## 🧪 Testing Phase 2

### Quick Tests (No API Key Required)
```bash
python main.py
```

Try these prompts:
1. "Read the content from https://example.com"
2. "Extract all links from https://news.ycombinator.com"
3. "Search for the word 'domain' in https://example.com"

### Full Tests (Requires Tavily API Key)
```bash
python main.py
```

Try these prompts:
1. "Search the web for information about Python programming"
2. "Search Wikipedia for information about AI"
3. "Find and read the Wikipedia article about Mercedes Sosa"

### View Example Prompts
```bash
python examples_phase2.py
```

## 🏗️ How It Works

### Tool Registration
```python
# tools/registry.py
from tools.web_search import web_search, web_search_wikipedia
from tools.document_reader import read_url, extract_links, search_in_document

tools = [
    web_search,
    web_search_wikipedia,
    read_url,
    extract_links,
    search_in_document,
]
```

### Agent Decision Flow
```
User: "Find Mercedes Sosa albums from 1990-2000"
  ↓
Agent: Decides to use web_search_wikipedia
  ↓
Tool: Returns Wikipedia search results
  ↓
Agent: Decides to use read_url on Wikipedia link
  ↓
Tool: Returns full article content
  ↓
Agent: Analyzes content and counts albums
  ↓
Response: "Mercedes Sosa released X albums between 1990-2000"
```

## 🔄 Multi-Step Reasoning Example

**Prompt:** "Find the NASA award number in the exoplanet discovery paper"

**Agent's Plan:**
1. 🔍 `web_search("NASA exoplanet discovery")` → Get news article
2. 📄 `read_url(news_article_url)` → Read article
3. 🔗 `extract_links(news_url, "paper")` → Find paper link
4. 📄 `read_url(paper_url)` → Read paper
5. 🔎 `search_in_document(paper_url, "award")` → Find award number
6. ✅ Extract and return the award number

## ⚙️ Technical Details

### Error Handling
- Network timeouts (10 seconds)
- Invalid URLs
- Missing API keys
- Malformed HTML
- Content size limits (10,000 chars for read_url)

### Content Processing
- Removes script, style, nav, footer, header tags
- Cleans excessive whitespace
- Makes relative URLs absolute
- Limits output to prevent token overflow

### Search Features
- AI-generated quick answers (Tavily)
- Multiple result sources
- Relevance-ranked results
- Content snippets included

## 📈 Metrics

- **Tools Added:** 5
- **Dependencies Added:** 4
- **Challenge Prompts Solvable:** 5 (Prompts 1, 5, 8, 15, 16)
- **Lines of Code:** ~300

## ⏭️ Next Phase

**Phase 3: Multimedia Analysis Tools**
- Audio transcription (Whisper)
- Video analysis (frame extraction + vision)
- Image recognition (Gemini Vision)
- Support for prompts 2, 4, 7, 11, 14

## 🐛 Troubleshooting

### "TAVILY_API_KEY not found"
- Add your Tavily API key to `.env` file
- Get a free key at https://tavily.com

### "Request timed out"
- Check your internet connection
- The timeout is set to 10 seconds
- Some websites may block automated requests

### "No results found"
- Try a different search query
- Some searches may return no results
- Verify the URL is accessible

### "Content truncated"
- This is normal for large pages
- The tool limits content to 10,000 characters
- Use `search_in_document` to find specific text

## 📚 Resources

- Tavily API Docs: https://docs.tavily.com
- BeautifulSoup Docs: https://www.crummy.com/software/BeautifulSoup/
- Requests Docs: https://requests.readthedocs.io
