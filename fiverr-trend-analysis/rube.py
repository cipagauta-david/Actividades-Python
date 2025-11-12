#!/usr/bin/env python3
"""
trend_workflow.py

Two-mode runner:
- COMPOSIO_MODE=1 : expects the Composio runtime to provide run_composio_tool, invoke_llm, upload_local_file, etc.
- COMPOSIO_MODE=0 : runs locally with mocks; optional OpenAI usage if OPENAI_API_KEY provided.
"""

import os
import json
import re
from datetime import datetime, UTC
import concurrent.futures
import csv
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

COMPOSIO_MODE = os.environ.get("COMPOSIO_MODE", "0") == "1"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# ----- Helper: safe extraction & JSON parsing (kept from your original code) -----
def safe_extract(result, key="data"):
    if not isinstance(result, dict):
        print(f"[{datetime.now(UTC).isoformat()}] Warning: Expected dict, got {type(result)}")
        return result
    data = result.get(key, result)
    if isinstance(data, dict) and key in data and isinstance(data[key], (dict, list)):
        print(f"[{datetime.now(UTC).isoformat()}] Debug: Found nested {key} structure")
        return data[key]
    if isinstance(data, (dict, list, str, int, float)):
        return data
    print(f"[{datetime.now(UTC).isoformat()}] Warning: {key} is unexpected type: {type(data)}")
    return {}

def extract_json_from_text(text):
    if "```json" in text:
        candidate = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        candidate = text.split("```", 1)[1].split("```", 1)[0].strip()
    else:
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            candidate = text[first : last + 1]
        else:
            candidate = text
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        fixed = candidate.replace("'", '"')
        fixed = re.sub(r",\s*}", "}", fixed)
        fixed = re.sub(r",\s*]", "]", fixed)
        try:
            return json.loads(fixed)
        except Exception:
            raise Exception(f"Failed to parse LLM output as JSON. Error: {e}. Snippet: {candidate[:1000]}")

# ----- Composio tool stubs / wrappers -----
if COMPOSIO_MODE:
    # In the Composio runtime the tool functions should be provided globally.
    # We'll reference them directly and raise if missing.
    try:
        run_composio_tool  # type: ignore
        invoke_llm  # type: ignore
        upload_local_file  # type: ignore
    except NameError:
        raise RuntimeError("COMPOSIO_MODE=1 but Composio helper functions (run_composio_tool/invoke_llm/upload_local_file) are not available in the runtime. Ensure you run inside Composio or provide the platform helpers.")
else:
    # Local mock implementations (allow you to run and test locally without Composio)
    print(f"[{datetime.now(UTC).isoformat()}] Running in LOCAL/MOCK mode (COMPOSIO_MODE=0).")

    # Optional: use OpenAI for the LLM if key available.
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            # Test that the key works
            client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            print("OpenAI library not available or invalid key:", e)
            OPENAI_API_KEY = ""

    def run_composio_tool(tool_name, params):
        """Mock: Return realistic-ish data per tool name."""
        print(f"[{datetime.now(UTC).isoformat()}] Mock run_composio_tool called: {tool_name}")
        if tool_name == "NOTION_INSERT_ROW_DATABASE":
            return ({"id": "mock-notion-id", "url": "https://notion.example/mock-notion-id"}, None)
        if tool_name == "COMPOSIO_SEARCH_TRENDS":
            # return a timeseries-like structure
            return ({"data": [{"date": "2025-01-01", "value": 10}, {"date": "2025-02-01", "value": 15}]}, None)
        if tool_name == "COMPOSIO_SEARCH_WEB":
            return ({"data": [{"title": "Market size report", "url": "https://example.com/report"}]}, None)
        if tool_name == "COMPOSIO_SEARCH_NEWS":
            return ({"data": [{"headline": "New product launch", "url": "https://news.example/article"}]}, None)
        if tool_name == "COMPOSIO_SEARCH_SCHOLAR":
            return ({"data": [{"title": "Consumer behaviour study", "url": "https://scholar.example/paper"}]}, None)
        if tool_name == "TEXT_TO_PDF_CONVERT_TEXT_TO_PDF":
            # pretend returned file structure
            return ({"file": {"s3url": "https://s3.mock.bucket/trend_report.pdf"}}, None)
        if tool_name == "GOOGLEDRIVE_UPLOAD_FILE":
            return ({"webViewLink": "https://drive.google.com/mock-file-link"}, None)
        # default
        return ({}, None)

    def invoke_llm(prompt):
        """Mock LLM. If OPENAI_API_KEY set, call OpenAI; otherwise return a conservative sample JSON string."""
        print(f"[{datetime.now(UTC).isoformat()}] Mock invoke_llm called (length {len(prompt)} chars)")
        if OPENAI_API_KEY:
            # call OpenAI ChatCompletion (simple, small)
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",  # or "gpt-4o" depending on availability
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=600,
                    temperature=0.2,
                )
                text = resp.choices[0].message.content
                return (text, None)
            except Exception as e:
                print("OpenAI call failed:", e)
        # fallback sample JSON (keeps same required schema)
        sample = {
            "executive_summary": "Short three-sentence executive summary about the niche trend.",
            "keyword_trends": [
                {"keyword": "wireless earbuds", "status": "RISING", "rationale": "search interest up 30%"},
                {"keyword": "true wireless", "status": "PLATEAU", "rationale": "stable interest"},
            ],
            "forecasts": [
                {"timeframe": "0-3 months", "prediction": "Slight increase in demand", "confidence": "MED", "key_metric": "search_volume"},
                {"timeframe": "3-12 months", "prediction": "Moderate growth", "confidence": "MED", "key_metric": "sales_growth"},
                {"timeframe": "12-36 months", "prediction": "Plateau as market matures", "confidence": "LOW", "key_metric": "market_saturation"},
            ],
            "tactical_90_day_plan": [
                {"priority": 1, "category": "Marketing", "action": "Run PPC tests", "rationale": "quick signal"},
                {"priority": 2, "category": "Product", "action": "Bundle accessories", "rationale": "increase AOV"},
                {"priority": 3, "category": "Pricing", "action": "Intro discount", "rationale": "acquire early adopters"},
            ],
            "validation_checklist": ["Check GA traffic for keywords", "Run 2-week PPC", "Pre-order landing page"],
            "data_sources": [
                {"source": "MockTrends", "url": "https://trends.example", "explanation": "trend timeseries sample"},
            ],
            "trend_rating": "RISING",
        }
        return (json.dumps(sample), None)

    def upload_local_file(local_file_path):
        """Mock: pretend to upload a file to Composio temporary storage."""
        print(f"[{datetime.now(UTC).isoformat()}] Mock upload_local_file called for {local_file_path}")
        # return a minimal success structure with a 'key'
        return ({"key": f"mock/{os.path.basename(local_file_path)}"}, None)

# ----- Begin actual workflow (mostly your original logic) -----
print(f"[{datetime.now(UTC).isoformat()}] Starting Fiverr Trend Analysis workflow")

# --- get inputs ---
buyer_name = os.environ.get("buyer_name", "")
niche = os.environ.get("niche", "")
keyword_list = os.environ.get("keyword_list", "")
geography = os.environ.get("geography", "")
timeframe = os.environ.get("timeframe", "")

if not all([buyer_name, niche, keyword_list, geography, timeframe]):
    raise ValueError("All inputs are required: buyer_name, niche, keyword_list, geography, timeframe")

keywords = [k.strip() for k in keyword_list.split(",") if k.strip()]

order_id = f"#{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
print(f"[{datetime.now(UTC).isoformat()}] Inputs validated: {len(keywords)} keywords for {niche} (order {order_id})")

# --- Notion record ---
print(f"[{datetime.now(UTC).isoformat()}] Creating Notion record")
notion_result, notion_error = run_composio_tool(
    "NOTION_INSERT_ROW_DATABASE",
    {
        "database_id": "2a3c26c2-89a3-8193-9792-d497f0c68065",
        "properties": [
            {"name": "Order ID", "type": "title", "value": order_id},
            {"name": "Client Name", "type": "rich_text", "value": buyer_name},
            {"name": "Date Received", "type": "date", "value": datetime.now(UTC).isoformat()},
            {"name": "Geography", "type": "select", "value": geography},
            {"name": "Keywords", "type": "rich_text", "value": keyword_list},
            {"name": "Niche", "type": "rich_text", "value": niche},
            {"name": "Status", "type": "select", "value": "🔄 Processing"},
            {"name": "Timeframe", "type": "select", "value": timeframe},
            {"name": "Files", "type": "rich_text", "value": ""},
            {"name": "Date Delivered", "type": "date", "value": datetime.now(UTC).isoformat()},
            {"name": "Executive Summary", "type": "rich_text", "value": ""},
            {"name": "Trend Rating", "type": "select", "value": ""},
            {"name": "Revenue", "type": "number", "value": "100"},
        ],
    },
)
if notion_error:
    print(f"[{datetime.now(UTC).isoformat()}] Warning: Notion creation failed: {notion_error}")
    notion_page_id = None
    notion_page_url = None
else:
    notion_data = safe_extract(notion_result)
    notion_page_id = notion_data.get("id")
    notion_page_url = notion_data.get("url")
    print(f"[{datetime.now(UTC).isoformat()}] Notion record created: {notion_page_id} / {notion_page_url}")

# --- Parallel data collection ---
print(f"[{datetime.now(UTC).isoformat()}] Starting parallel data collection")
def fetch_trends():
    return ("trends",) + run_composio_tool("COMPOSIO_SEARCH_TRENDS", {"query": f"{niche} {keywords[0]}", "data_type":"TIMESERIES"})
def fetch_web():
    return ("web",) + run_composio_tool("COMPOSIO_SEARCH_WEB", {"query": f"{niche} market size trends {geography}"})
def fetch_news():
    return ("news",) + run_composio_tool("COMPOSIO_SEARCH_NEWS", {"query": f"{niche} industry news trends", "when":"m"})
def fetch_scholar():
    return ("scholar",) + run_composio_tool("COMPOSIO_SEARCH_SCHOLAR", {"query": f"{niche} consumer behavior trends"})

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(fn) for fn in [fetch_trends, fetch_web, fetch_news, fetch_scholar]]
    results = {}
    try:
        for fut in concurrent.futures.as_completed(futures, timeout=240):
            try:
                source, data, error = fut.result()
            except Exception as e:
                print(f"[{datetime.now(UTC).isoformat()}] Warning: fetch worker raised: {e}")
                continue
            if error:
                print(f"[{datetime.now(UTC).isoformat()}] Warning: {source} failed: {error}")
                results[source] = {}
            else:
                results[source] = safe_extract(data)
    except concurrent.futures.TimeoutError:
        print(f"[{datetime.now(UTC).isoformat()}] Warning: Data collection timed out (240s). Proceeding with partial results.")
        for f in futures:
            if not f.done():
                f.cancel()
print(f"[{datetime.now(UTC).isoformat()}] Data collection complete: sources: {list(results.keys())}")

# --- AI synthesis ---
print(f"[{datetime.now(UTC).isoformat()}] Starting AI analysis")

def safe_truncate_json(data, max_chars=100000):
    try:
        json_str = json.dumps(data, indent=2, default=str)
    except Exception:
        return json.dumps({"_summary": "non-serializable data", "type": str(type(data))})
    if len(json_str) <= max_chars:
        return json_str
    if isinstance(data, list):
        summary = {"_type":"list","length":len(data),"sample":data[:5]}
        return json.dumps(summary, indent=2, default=str)
    if isinstance(data, dict):
        keys = list(data.keys())[:20]
        summary = {"_type":"dict","num_keys":len(data),"keys_sample":keys,"note":"full payload truncated"}
        return json.dumps(summary, indent=2, default=str)
    return json_str[:max_chars] + "\n... (truncated)"

analysis_prompt = f"""You are a professional trend analyst. Analyze the following data and produce a structured report.

Client: {buyer_name}
Niche: {niche}
Keywords: {keyword_list}
Geography: {geography}
Timeframe: {timeframe}

Data collected:
{safe_truncate_json(results, 100000)}

Tasks (FOLLOW THIS EXACT STRUCTURE):
1) Executive Summary: Give a 3-sentence summary of the current state of this trend.
2) Keyword Trends: For EACH keyword ({keyword_list}), provide:
   - Status: HOT / RISING / PLATEAU / DECLINING
   - One-line rationale
3) Forecasts: Produce 3 forecasts:
   - 0-3 months: prediction, confidence (LOW/MED/HIGH), key metric to watch
   - 3-12 months: prediction, confidence, key metric
   - 12-36 months: prediction, confidence, key metric
4) 90-Day Tactical Plan: Provide 3 prioritized actions:
   - Priority 1 (Marketing): specific action + rationale
   - Priority 2 (Product): specific action + rationale
   - Priority 3 (Pricing): specific action + rationale
5) Validation Checklist: Provide steps for the client to run themselves to validate this trend.
6) Sources: List all data sources with URLs and 1-line explanation of what the data shows.

Return ONLY valid JSON in this exact format:
{{"executive_summary": "...", "keyword_trends":[{{"keyword":"...","status":"...","rationale":"..."}}], "forecasts":[{{"timeframe":"...","prediction":"...","confidence":"...","key_metric":"..."}}], "tactical_90_day_plan":[{{"priority":1,"category":"...","action":"...","rationale":"..."}}], "validation_checklist":["..."], "data_sources":[{{"source":"...","url":"...","explanation":"..."}}], "trend_rating":"..."}}
"""

analysis_result, analysis_error = invoke_llm(analysis_prompt)
if analysis_error:
    raise Exception(f"AI analysis failed: {analysis_error}")

try:
    analysis = extract_json_from_text(analysis_result)
    print(f"[{datetime.now(UTC).isoformat()}] AI analysis completed successfully")
except Exception as e:
    print(f"[{datetime.now(UTC).isoformat()}] JSON parse error: {e}")
    raise

# validation of fields
required_fields = ["executive_summary","keyword_trends","forecasts","tactical_90_day_plan","validation_checklist","data_sources","trend_rating"]
for f in required_fields:
    if f not in analysis or not analysis[f]:
        raise Exception(f"AI analysis missing required field: {f}")

# --- Charts ---
print(f"[{datetime.now(UTC).isoformat()}] Generating charts")
try:
    fig, ax = plt.subplots(figsize=(10,6))
    forecasts = analysis.get("forecasts", [])
    timeframes = [f["timeframe"] for f in forecasts]
    confidences = [{"LOW":0.3,"MED":0.6,"HIGH":0.9}.get(f["confidence"],0.5) for f in forecasts]
    bars = ax.bar(timeframes, confidences)
    ax.set_ylim(0,1)
    ax.set_ylabel("Confidence Level")
    ax.set_xlabel("Timeframe")
    ax.set_title(f"Trend Forecast Confidence - {niche}")
    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.3)
    for i,(bar,conf) in enumerate(zip(bars, confidences)):
        ax.text(bar.get_x() + bar.get_width()/2.0, bar.get_height()+0.02, f'{forecasts[i]["confidence"]}', ha="center")
    plt.tight_layout()
    chart1_path = os.path.join(tempfile.gettempdir(), "forecast_chart.png")
    plt.savefig(chart1_path, dpi=200, bbox_inches="tight")
    plt.close()

    # keywords chart
    fig, ax = plt.subplots(figsize=(10,6))
    keyword_trends = analysis.get("keyword_trends", [])
    keywords_chart = [kt["keyword"] for kt in keyword_trends]
    statuses = [kt["status"] for kt in keyword_trends]
    status_colors = {"HOT":"#FF4757","RISING":"#2ED573","PLATEAU":"#FFA502","DECLINING":"#747D8C"}
    colors = [status_colors.get(s,"#95A5A6") for s in statuses]
    y_pos = np.arange(len(keywords_chart))
    bars = ax.barh(y_pos, [1]*len(keywords_chart), color=colors)
    ax.set_yticks(y_pos); ax.set_yticklabels(keywords_chart)
    ax.set_xticks([])
    ax.set_title(f"Keyword Trend Status - {niche}")
    for i,(bar,status) in enumerate(zip(bars, statuses)):
        ax.text(0.5, bar.get_y() + bar.get_height()/2.0, status, ha="center", va="center", color="white", fontweight="bold")
    plt.tight_layout()
    chart2_path = os.path.join(tempfile.gettempdir(), "keyword_status_chart.png")
    plt.savefig(chart2_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"[{datetime.now(UTC).isoformat()}] Charts generated: {chart1_path}, {chart2_path}")
except Exception as e:
    print(f"[{datetime.now(UTC).isoformat()}] Chart generation failed: {e}")
    raise

# --- Markdown report ---
print(f"[{datetime.now(UTC).isoformat()}] Generating markdown report")
report_md = f"# Trend Analysis Report: {niche}\n\n**Client:** {buyer_name}\n**Order ID:** {order_id}\n**Date:** {datetime.now(UTC).strftime('%B %d, %Y')}\n**Geography:** {geography}\n**Timeframe:** {timeframe}\n\n---\n\n## Executive Summary\n\n{analysis.get('executive_summary','N/A')}\n\n**Overall Trend Rating:** {analysis.get('trend_rating','N/A')}\n\n---\n\n## Keyword Trend Analysis\n\n"
for kt in analysis.get("keyword_trends", []):
    report_md += f"### {kt['keyword']}\n**Status:** {kt['status']}\n**Rationale:** {kt['rationale']}\n\n"
report_md += "---\n\n## Market Forecasts\n\n"
for fc in analysis.get("forecasts", []):
    report_md += f"### {fc['timeframe']}\n**Prediction:** {fc['prediction']}\n**Confidence:** {fc['confidence']}\n**Key Metric to Watch:** {fc['key_metric']}\n\n"
report_md += "---\n\n## 90-Day Tactical Action Plan\n\n"
for action in analysis.get("tactical_90_day_plan", []):
    report_md += f"### Priority {action['priority']}: {action['category']}\n**Action:** {action['action']}\n**Rationale:** {action['rationale']}\n\n"
report_md += "---\n\n## Validation Checklist\n\n"
for i, step in enumerate(analysis.get("validation_checklist", []), 1):
    report_md += f"{i}. {step}\n"
report_md += "\n---\n\n## Data Sources\n\n"
for source in analysis.get("data_sources", []):
    report_md += f"- **{source.get('source','') }**: {source.get('explanation','')}\n"
    if source.get("url"):
        report_md += f"  {source.get('url')}\n"
    report_md += "\n"
markdown_path = os.path.join(tempfile.gettempdir(), "trend_report.md")
with open(markdown_path, "w", encoding="utf-8") as f:
    f.write(report_md)
print(f"[{datetime.now(UTC).isoformat()}] Markdown report written to {markdown_path}")

# --- Convert to PDF via composio tool (or mock) ---
print(f"[{datetime.now(UTC).isoformat()}] Converting to PDF")
pdf_result, pdf_error = run_composio_tool("TEXT_TO_PDF_CONVERT_TEXT_TO_PDF", {"text": report_md, "file_type": "markdown"})
if pdf_error:
    raise Exception(f"PDF conversion failed: {pdf_error}")
pdf_data = safe_extract(pdf_result)
pdf_s3_url = ""
if 'file' in pdf_data and isinstance(pdf_data['file'], dict):
    pdf_s3_url = pdf_data['file'].get('s3url','')
if not pdf_s3_url:
    raise Exception("Failed to obtain pdf s3 url from conversion result")
print(f"[{datetime.now(UTC).isoformat()}] PDF created at {pdf_s3_url}")

# --- Upload files to Google Drive (uses run_composio_tool mock or real) ---
print(f"[{datetime.now(UTC).isoformat()}] Uploading files to Google Drive (via GOOGLED RIVE UPLOAD tool)")
def upload_file_to_google_drive(local_file_path, folder_number, drive_filename="", mimetype=""):
    # Drive folder ids - keep same as your original mapping
    DRIVE_FOLDERS = [
        "1kxZOQ3ZbOvQqu2U6xxKl_C5XrF795cL2",
        "1u3N35rlIOXJsAWEQT-dY_Zl-Tthpbr3T",
        "15roNpcqV5cPe2EITbyAFFa9PKJlxK1oZ",
        "1auHTHgYWev8H_1h9ngui6WgfEKI65kSo",
    ]
    try:
        temp_upload, upload_err = upload_local_file(local_file_path)
        if upload_err:
            return None, f"Failed to upload to Composio storage: {upload_err}"
        upload_data = safe_extract(temp_upload) if isinstance(temp_upload, dict) else (temp_upload or {})
        s3key = upload_data.get("key")
        if not s3key:
            return None, "Failed to get s3key from Composio storage upload"
        drive_result, drive_err = run_composio_tool("GOOGLEDRIVE_UPLOAD_FILE", {"file_to_upload": {"name": drive_filename, "mimetype": mimetype, "s3key": s3key}, "folder_to_upload_to": DRIVE_FOLDERS[folder_number]})
        if drive_err:
            return None, f"Failed to upload to Google Drive: {drive_err}"
        drive_data = safe_extract(drive_result)
        drive_link = drive_data.get("webViewLink")
        if not drive_link:
            return None, "Failed to get Google Drive link from upload result"
        return drive_link, None
    except Exception as e:
        return None, str(e)

markdown_url, markdown_err = upload_file_to_google_drive(markdown_path, 3, f"{order_id}_trend_report.md", "text/markdown")
chart1_url, err1 = upload_file_to_google_drive(chart1_path, 0, f"{order_id}_forecast_chart.png", "image/png")
chart2_url, err2 = upload_file_to_google_drive(chart2_path, 0, f"{order_id}_keyword_status_chart.png", "image/png")
if markdown_err: print("Markdown upload warning:", markdown_err)
if err1 or err2: print("Chart upload warnings:", err1, err2)

# create CSVs and upload
csv_urls = {}
for source_name, source_data in results.items():
    csv_path = os.path.join(tempfile.gettempdir(), f"{order_id}_{source_name}_data.csv")
    try:
        if isinstance(source_data, dict):
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Key", "Value"])
                def flatten_dict(d, parent_key="", sep="_"):
                    items = []
                    for k, v in d.items():
                        new_key = f"{parent_key}{sep}{k}" if parent_key else k
                        if isinstance(v, dict):
                            items.extend(flatten_dict(v, new_key, sep=sep).items())
                        elif isinstance(v, list):
                            for i, item in enumerate(v):
                                if isinstance(item, dict):
                                    items.extend(flatten_dict(item, f"{new_key}_{i}", sep=sep).items())
                                else:
                                    items.append((f"{new_key}_{i}", str(item)))
                        else:
                            items.append((new_key, str(v)))
                    return dict(items)
                flattened = flatten_dict(source_data)
                for key, value in flattened.items():
                    writer.writerow([key, value])
        elif isinstance(source_data, list):
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if source_data and isinstance(source_data[0], dict):
                    writer.writerow(list(source_data[0].keys()))
                    for item in source_data:
                        writer.writerow(list(item.values()))
                else:
                    writer.writerow(["Index","Value"])
                    for i, item in enumerate(source_data):
                        writer.writerow([i, str(item)])
        else:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Source","Data"])
                writer.writerow([source_name, str(source_data)])
        csv_upload, csv_err = upload_file_to_google_drive(csv_path, 2, f"{order_id}_{source_name}_data.csv", "text/csv")
        csv_urls[f"{source_name}_csv"] = csv_upload or ""
    except Exception as e:
        print("CSV creation/upload failed for", source_name, e)
        csv_urls[f"{source_name}_csv"] = ""

# --- Update Notion row ---
print(f"[{datetime.now(UTC).isoformat()}] Updating Notion record")
files_text = []
if pdf_s3_url: files_text.append(f"📄 PDF Report (S3): {pdf_s3_url}")
if markdown_url: files_text.append(f"📝 Markdown Report: {markdown_url}")
if chart1_url: files_text.append(f"📊 Forecast Chart: {chart1_url}")
if chart2_url: files_text.append(f"📈 Keywords Chart: {chart2_url}")
for csv_name, csv_url in csv_urls.items():
    if csv_url:
        source_name = csv_name.replace("_csv","").title()
        files_text.append(f"📋 {source_name} Data: {csv_url}")
files_text_content = "\n".join(files_text) if files_text else "No files uploaded"

update_result, update_error = run_composio_tool("NOTION_UPDATE_ROW_DATABASE", {
    "row_id": notion_page_id,
    "properties": [
        {"name": "Status", "type": "select", "value": "🟡 Waiting client review"},
        {"name": "Date Delivered", "type": "date", "value": datetime.now(UTC).isoformat()},
        {"name": "Trend Rating", "type": "select", "value": analysis.get("trend_rating","RISING")},
        {"name": "Executive Summary", "type": "rich_text", "value": analysis.get("executive_summary","")[:2000]},
        {"name": "Files", "type": "rich_text", "value": files_text_content[:2000]},
        {"name": "Revenue", "type": "number", "value": "100"},
    ]
})
if update_error:
    print("Notion update warning:", update_error)
else:
    print("Notion updated successfully")

# --- Output object ---
output = {
    "order_id": order_id,
    "executive_summary": analysis.get("executive_summary"),
    "pdf_report_url": pdf_s3_url,
    "markdown_report_url": markdown_url,
    "chart_forecast_url": chart1_url,
    "chart_keywords_url": chart2_url,
    "notion_page_url": notion_page_url,
    "trend_rating": analysis.get("trend_rating"),
}
print(json.dumps(output, indent=2))
