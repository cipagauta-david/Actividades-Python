import os
import json
import re
from datetime import datetime
import concurrent.futures
import matplotlib.pyplot as plt
import numpy as np

print(f"[{datetime.now().isoformat()}] Starting Fiverr Trend Analysis")

# Safe extraction with fixed Notion handling
def safe_extract(result):
    if not isinstance(result, dict):
        return result
    if "data" in result and isinstance(result["data"], dict):
        if "response_data" in result["data"]:
            return result["data"]["response_data"]
        if "data" in result["data"]:
            return result["data"]["data"]
        return result["data"]
    return result

def extract_json(text):
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
    return json.loads(text.strip())

# Get inputs
buyer_name = os.environ.get("buyer_name", "")
niche = os.environ.get("niche", "")
keyword_list = os.environ.get("keyword_list", "")
geography = os.environ.get("geography", "")
timeframe = os.environ.get("timeframe", "")

if not all([buyer_name, niche, keyword_list, geography, timeframe]):
    raise ValueError("All inputs required")

keywords = [k.strip() for k in keyword_list.split(",") if k.strip()]
if not keywords:
    raise ValueError("Need at least one keyword")

order_id = f"#{datetime.now().strftime('%Y%m%d%H%M%S')}"
print(f"Order: {order_id}, Keywords: {len(keywords)}")

# Create Notion page
print(f"[{datetime.now().isoformat()}] Creating Notion record...")
notion_result, notion_error = run_composio_tool(
      "NOTION_INSERT_ROW_DATABASE",
    {
          "database_id": "2a3c26c2-89a3-8193-9792-d497f0c68065",
        "properties": [
              {"name": "Order ID", "type": "title", "value": order_id},
            {"name": "Client Name", "type": "rich_text", "value": buyer_name},
            {"name": "Date Received", "type": "date", "value": datetime.now().isoformat()},
            {"name": "Geography", "type": "select", "value": geography},
            {"name": "Keywords", "type": "rich_text", "value": keyword_list},
            {"name": "Niche", "type": "rich_text", "value": niche},
            {"name": "Status", "type": "select", "value": "🔄 Processing"},
            {"name": "Timeframe", "type": "select", "value": timeframe},
            {"name": "Revenue", "type": "number", "value": "100"},
        ],
    },
)

if notion_error:
    print(f"Notion error: {notion_error}")
    notion_page_id = None
    notion_page_url = None
else:
    notion_data = safe_extract(notion_result)
    notion_page_id = notion_data.get("id")
    notion_page_url = notion_data.get("url")
    print(f"Notion page: {notion_page_id}")

# Collect data in parallel
print(f"[{datetime.now().isoformat()}] Collecting data...")

def fetch_trends():
    r, e = run_composio_tool("COMPOSIO_SEARCH_TRENDS", {"query": f"{niche} {keywords[0]}", "data_type": "TIMESERIES"})
    return ("trends", r, e)

def fetch_web():
    r, e = run_composio_tool("COMPOSIO_SEARCH_WEB", {"query": f"{niche} market trends {geography}"})
    return ("web", r, e)

def fetch_news():
    r, e = run_composio_tool("COMPOSIO_SEARCH_NEWS", {"query": f"{niche} trends", "when": "m"})
    return ("news", r, e)

def fetch_scholar():
    r, e = run_composio_tool("COMPOSIO_SEARCH_SCHOLAR", {"query": f"{niche} trends"})
    return ("scholar", r, e)

results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(fn) for fn in [fetch_trends, fetch_web, fetch_news, fetch_scholar]]
    for future in concurrent.futures.as_completed(futures, timeout=180):
        try:
            src, data, err = future.result()
            results[src] = safe_extract(data) if not err else {}
        except Exception as e:
            print(f"Fetch error: {e}")

print(f"Data collected: {len(results)} sources")

# AI analysis
print(f"[{datetime.now().isoformat()}] AI analysis...")
data_summary = json.dumps(results, default=str)[:50000]

prompt = f"""Analyze this {niche} trend data for {geography} market:

Keywords: {keyword_list}
Data: {data_summary}

Return ONLY valid JSON:
{{
    "executive_summary": "3-sentence summary",
  "keyword_trends": [{{"keyword": "gym", "status": "RISING", "rationale": "brief reason"}}],
  "forecasts": [
      {{"timeframe": "0-3 months", "prediction": "...", "confidence": "HIGH", "key_metric": "..."}},
    {{"timeframe": "3-12 months", "prediction": "...", "confidence": "MED", "key_metric": "..."}},
    {{"timeframe": "12-36 months", "prediction": "...", "confidence": "LOW", "key_metric": "..."}}
  ],
  "tactical_90_day_plan": [
      {{"priority": 1, "category": "Marketing", "action": "...", "rationale": "..."}},
    {{"priority": 2, "category": "Product", "action": "...", "rationale": "..."}},
    {{"priority": 3, "category": "Pricing", "action": "...", "rationale": "..."}}
  ],
  "validation_checklist": ["step1", "step2", "step3"],
  "data_sources": [{{"source": "Google Trends", "url": "...", "explanation": "..."}}],
  "trend_rating": "RISING"
}}"""

analysis_text, llm_err = invoke_llm(prompt)
if llm_err:
    raise Exception(f"LLM failed: {llm_err}")

try:
    analysis = extract_json(analysis_text)
except Exception as e:
    raise Exception(f"JSON parse failed: {e}")

print(f"Analysis complete: {analysis.get('trend_rating', 'N/A')}")

# Generate charts
print(f"[{datetime.now().isoformat()}] Creating charts...")
fig, ax = plt.subplots(figsize=(10, 6))
forecasts = analysis.get("forecasts", [])
timeframes = [f["timeframe"] for f in forecasts]
confidences = [{"LOW": 0.3, "MED": 0.6, "HIGH": 0.9}.get(f["confidence"], 0.5) for f in forecasts]
bars = ax.bar(timeframes, confidences, color=["#FF6B6B", "#4ECDC4", "#45B7D1"])
ax.set_ylim(0, 1)
ax.set_ylabel("Confidence", fontsize=12)
ax.set_title(f"Forecast Confidence - {niche}", fontsize=14, fontweight="bold")
for i, (bar, conf) in enumerate(zip(bars, confidences)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, forecasts[i]["confidence"], ha="center", fontweight="bold")
plt.tight_layout()
chart1 = "/tmp/forecast.png"
plt.savefig(chart1, dpi=300, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
kw_trends = analysis.get("keyword_trends", [])
kws = [k["keyword"] for k in kw_trends]
statuses = [k["status"] for k in kw_trends]
colors = [{"HOT": "#FF4757", "RISING": "#2ED573", "PLATEAU": "#FFA502", "DECLINING": "#747D8C"}.get(s, "#95A5A6") for s in statuses]
y_pos = np.arange(len(kws))
bars = ax.barh(y_pos, [1]*len(kws), color=colors)
ax.set_yticks(y_pos)
ax.set_yticklabels(kws)
ax.set_title(f"Keyword Status - {niche}", fontsize=14, fontweight="bold")
ax.set_xticks([])
for i, (bar, st) in enumerate(zip(bars, statuses)):
    ax.text(0.5, bar.get_y() + bar.get_height()/2, st, ha="center", va="center", fontweight="bold", color="white")
plt.tight_layout()
chart2 = "/tmp/keywords.png"
plt.savefig(chart2, dpi=300, bbox_inches="tight")
plt.close()

# Generate report
print(f"[{datetime.now().isoformat()}] Creating report...")
report = f"""# Trend Analysis: {niche}

**Client:** {buyer_name}  
**Order:** {order_id}  
**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Geography:** {geography}  
**Timeframe:** {timeframe}

## Executive Summary

{analysis.get('executive_summary', 'N/A')}

**Trend Rating:** {analysis.get('trend_rating', 'N/A')}

## Keywords
"""

for kt in kw_trends:
    report += f"### {kt['keyword']}\
**Status:** {kt['status']} - {kt['rationale']}\
\
"

report += "\
## Forecasts\
"
for fc in forecasts:
    report += f"### {fc['timeframe']}\
**Prediction:** {fc['prediction']}  \
**Confidence:** {fc['confidence']}  \
**Key Metric:** {fc['key_metric']}\
\
"

report += "\
## 90-Day Plan\
"
for act in analysis.get("tactical_90_day_plan", []):
    report += f"### Priority {act['priority']}: {act['category']}\
**Action:** {act['action']}  \
**Rationale:** {act['rationale']}\
\
"

md_path = "/tmp/report.md"
with open(md_path, "w") as f:
    f.write(report)

# Convert to PDF
print(f"[{datetime.now().isoformat()}] Converting to PDF...")
pdf_result, pdf_err = run_composio_tool("TEXT_TO_PDF_CONVERT_TEXT_TO_PDF", {"text": report, "file_type": "markdown"})
if pdf_err:
    raise Exception(f"PDF failed: {pdf_err}")

pdf_data = safe_extract(pdf_result)
pdf_url = pdf_data.get("file", {}).get("s3url", "") if isinstance(pdf_data.get("file"), dict) else ""
if not pdf_url:
    raise Exception("No PDF URL")

print(f"PDF: {pdf_url[:50]}...")

# Upload to Drive
print(f"[{datetime.now().isoformat()}] Uploading to Drive...")
FOLDERS = ["1kxZOQ3ZbOvQqu2U6xxKl_C5XrF795cL2", "1auHTHgYWev8H_1h9ngui6WgfEKI65kSo"]

def upload_to_drive(path, folder_idx, name, mime):
    temp, err = upload_local_file(path)
    if err:
        return None
    s3key = safe_extract(temp).get("key")
    if not s3key:
        return None
    dr, e = run_composio_tool("GOOGLEDRIVE_UPLOAD_FILE", {
          "file_to_upload": {"name": name, "mimetype": mime, "s3key": s3key},
        "folder_to_upload_to": FOLDERS[folder_idx]
    })
    if e:
        return None
    return safe_extract(dr).get("webViewLink")

md_url = upload_to_drive(md_path, 1, f"{order_id}_report.md", "text/markdown") or ""
c1_url = upload_to_drive(chart1, 0, f"{order_id}_forecast.png", "image/png") or ""
c2_url = upload_to_drive(chart2, 0, f"{order_id}_keywords.png", "image/png") or ""

print(f"Uploaded: MD={bool(md_url)}, C1={bool(c1_url)}, C2={bool(c2_url)}")

# Update Notion
if notion_page_id:
    print(f"[{datetime.now().isoformat()}] Updating Notion...")
    files_txt = f"📄 PDF: {pdf_url}\
📝 Markdown: {md_url}\
📊 Forecast: {c1_url}\
📈 Keywords: {c2_url}"
    upd, upd_err = run_composio_tool("NOTION_UPDATE_ROW_DATABASE", {
          "row_id": notion_page_id,
        "properties": [
              {"name": "Status", "type": "select", "value": "🟡 Waiting client review"},
            {"name": "Date Delivered", "type": "date", "value": datetime.now().isoformat()},
            {"name": "Trend Rating", "type": "select", "value": analysis.get("trend_rating", "RISING")},
            {"name": "Executive Summary", "type": "rich_text", "value": analysis.get("executive_summary", "")[:2000]},
            {"name": "Files", "type": "rich_text", "value": files_txt[:2000]},
        ],
    })
    if upd_err:
        print(f"Notion update warning: {upd_err}")

print(f"[{datetime.now().isoformat()}] Complete!")

output = {
      "order_id": order_id,
    "executive_summary": analysis.get("executive_summary"),
    "pdf_report_url": pdf_url,
    "markdown_report_url": md_url,
    "chart_forecast_url": c1_url,
    "chart_keywords_url": c2_url,
    "notion_page_url": notion_page_url,
    "trend_rating": analysis.get("trend_rating"),
}
output