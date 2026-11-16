# Executive Sales Dashboard

Interactive executive dashboard built in Streamlit, reading a star-schema
analytics mart produced by my
[retail-sales-data-pipeline](https://github.com/peaceogobor-engr/retail-sales-data-pipeline)
repo. Designed around three questions an executive actually asks:
**How are we doing? Where are we winning or losing? What needs attention?**

**What this demonstrates:** KPI design, executive-first layout (KPIs → trend
→ breakdowns → exceptions), and the same dashboard discipline I apply in
production Power BI / Vital Signs board reporting. In my day job I build
these in Power BI on Azure Synapse; this public version uses Streamlit so
anyone can open it in a browser.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
