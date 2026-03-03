import requests
import urllib3
import webbrowser
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RAW_HEADERS = """
authorization
Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE2aTQ0dDNLTlVSRHUycTVKSU5NZVlvX2FtVV9SUzI1NiIsInBpLmF0bSI6IjFmN28ifQ.eyJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiY2xpZW50X2lkIjoiYXF1aWxhLXVzZXItYXV0aCIsImlzcyI6Imh0dHBzOi8vc3NvLmNvbW1vbi5jbG91ZC5ocGUuY29tIiwianRpIjoiSzJrdGJBREMwOVBKWkN3Z2trIiwibGFzdE5hbWUiOiJIdXNzYWluIiwic3ViIjoic3llZC1tYXNvb2QuaHVzc2FpbkBocGUuY29tIiwiYXVkIjoiYXVkIiwiYyI6IjUwOGNkOGM0LTUxYjUtNDUwMS04ZjA2LTU3YjIzZThlN2E3YSIsImF1dGhfc291cmNlIjoiaHBlIiwiZ2l2ZW5OYW1lIjoiU3llZCBNYXNvb2QiLCJpYXQiOjE3NzIzMzQzNTAsImV4cCI6MTc3MjM0MTU1MH0.ITJThgaDFiocOkDCxqAHFaYK_wyH56UnW1wjLcpv7zYSnJLFgGFH7p9zBjnlNOpn3pzZmbP83cUQ4kcn6Tzae-lCkXS82Ld_lyMOsqRUR-23xielRp1dORN1xnadg_thcy6JWZ24oVJIeL-SB2LqjMMin3o4_oF40Uq6TwjdMPP5a-eNVbWvcQ92dS90D2syhTQtK4SJogerxod3y2hUS3TdzgrlmMkQoQSXY5YnD_XUY9LTa5pinMtr8ZGwnALPAeBCm8omv9cVzZHC6t8p2UoqhCSGg7DhyIdKhi4AYtTa6YBJsYT9kJMp3dnUiaLJQR3Rnw3TM5tDJ57dMBvWDg
cookie
notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; optout_domains_pc=; drift_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; driftt_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; _mkto_trk=id:117-SZC-407&token:_mch-hpe.com-bbe7b9487e76baae371e01ed53442ad; s_ecid=MCMID%7C27457408545680224153679487991052136343; _ga=GA1.1.37299827.1770224817; _gcl_au=1.1.188344893.1770316432; coveo_visitorId=a0f5d633-ba2d-4547-a6dd-e128659503a1; lang=en; cc=in; kndctr_56B5A25055667EED7F000101_AdobeOrg_identity=CiYyNzQ1NzQwODU0NTY4MDIyNDE1MzY3OTQ4Nzk5MTA1MjEzNjM0M1IRCOLoibXXMhgBKgRJTkQxMAHwAdzdk4TKMw%3D%3D; _uetvid=3d313a20420e11f099d051fbedc2727d|12vvtld|1763234352536|1|1|bat.bing.com/p/insights/c/l; RT="z=1&dm=hpe.com&si=e335455d-f500-438a-8332-c03aba1ca74f&ss=mm5brqai&sl=0&tt=0"; mbox=session%2327457408545680224153679487991052136343%2DtuRgOx%231772224790; _ga_3YZ812RSQH=GS2.1.s1772222939$o2$g0$t1772222943$j56$l0$h0; AMCV_56B5A25055667EED7F000101%40AdobeOrg=179643557%7CMCMID%7C27457408545680224153679487991052136343%7CMCIDTS%7C20511%7CMCAID%7CNONE%7CMCOPTOUT-1772230157s%7CNONE%7CMCAAMLH-1772827757%7C12%7CMCAAMB-1772827757%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C5.5.0; fs_uid=#11CH4F#b87427ea-2f2a-4342-9bb6-c735aae503d9:643f80f6-209a-4f79-86fe-03b595198e73:1772222956077::1#b3faeaaf#/1803664526; isMfe=true; i18next=en-US; notice_behavior=implied,eu; _abck=4E0CF9E29DBE2E801FD5A79A3B1336E8~0~YAAQZwHARcPVcmecAQAA9fbupg/Wmh8aIkXEIdLKXAB6DQqRsf8FXupRcVr00qrW09Va+PBHvb06/TWhatVlwRv3Cm3QXdfrMlmv3Vo9LlH8OxVjJ9u9eMhWd3xnj+4Dt/GqebQkWkczJkXHot8DFTkWjzHS9gR1FLNpkIDfTtGT71NmB9ElO2azNAERNArt1xJw9YfkQxR7UChuex/qum+ZMkNvl+Q+4j2KyhKQq2z0++hApDZHidWRSMWP866ctuQnbCgd0H7lJXgevp4RQJ3VoNDiuwBkZLN0VGdqfrobDOx1OkiHBJm45C0PKKbSCNr9ekc0Ex+78G6IEmAMx5slTD+Y1kbdcRF4yANA7awN/Hc6IMnbxXvBZEkq9S2OimmYCFcz6On5qjSwvYUioL44qISoW+Bkei3vxnQMrFZL/FP7CRT4yLKQ6nGc2WiImGcEOxKnB3TaIPYrf7YHwGBwY+hOfjacKNBEjP+ugcEP8n7DuJS2hdyXDQHIs+us2PJZ0J4JLBcvE2utbtPgSDQiPDDUC2SCYnJDJGn666cxqXEcLzKzLqmv8dTTfkBKVlXSnpw82KVJYl96SvfwO3IlCgC74wUN//LvXEG5jFglolf4nodIn/FSmMh20Q==~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f2JWnErG6WxSk2MIYxQalEUu3CEp3xHT7UuYKn1jGcf7O52zLb38r5BthyaR0ivBRTpljVL9psG+ee5N3C3LQuzH48KuNjJH3nLGjd79NaVQYxk+4725qMcOq%2faZ9%2fEULbcoV8k%3d~-1; ccs-pf-id=0DuC-d8mx8QgyxPjZLyqQkkqqbc..o5Ee.dRjdGXSZN1tXW660w4ZVnw3lw; ccs-old-style-pf-id=0DuC-d8mx8QgyxPjZLyqQkkqqbc..o5Ee.dRjdGXSZN1tXW660w4ZVnw3lw; AMP_ca3a475ee4=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3NDAzZjgzMS1hMzFiLTRkZGYtYWMxNS04YzhlNmY3MWE4MTUlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI4MzI4NTlkNmEyMGM0MGYwNjQ0MTM4YTU2M2NhODhkOTAwYzQ2NmMwNjU0NTNiZjg2YmZiZGY4MjI1YWRmODMzJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc3MjMyNzIwODU5NSUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NzIzMjcyMzAxMTklMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTYlMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; ccs-session=eyJzZXNzaW9uaWQiOiAiNmJhMzdlZWJkMGFjODE3YWM3MTI3ZGZjMTQxODE5OTciLCAiY2NzLWNzcmZ0b2tlbiI6ICIwNzJjNzJhODk3OTIxMGNiODNkNmFkNmUzNmJkOTBlMDI1OTBmMDkyIn0=.aaO9Sw.6s3DMYumnEme1eZyZjkAhBbFdQg
"""

def build_headers(raw_text):
    lines = raw_text.strip().split("\n")
    headers = {}
    current_key = None
    current_value = []

    for line in lines:
        line = line.strip()

        if line.startswith("#"):
            line = line[1:].strip()

        if not line:
            continue

        if line.lower() == "authorization":
            current_key = "Authorization"
            current_value = []
            continue

        if line.lower() == "cookie":
            current_key = "Cookie"
            current_value = []
            continue

        if current_key:
            current_value.append(line)
            headers[current_key] = " ".join(current_value)

    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    return headers


headers = build_headers(RAW_HEADERS)

url = "https://common.cloud.hpe.com/api/glp/support-assistant/v1alpha1/customers"
username = "vishal.kumar-ext@hpe.com"

limit = 50
offset = 0
all_customers = []

print("\nFetching workspaces...\n")

while True:
    params = {
        "limit": limit,
        "offset": offset,
        "username": username
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
        verify=False
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        break

    data = response.json()
    customers = data.get("customers", [])
    pagination = data.get("pagination", {})

    if not customers:
        break

    all_customers.extend(customers)

    total_count = pagination.get("total_count", 0)
    count_per_page = pagination.get("count_per_page", limit)

    offset += count_per_page

    print(f"Fetched {min(offset, total_count)} of {total_count}")

    if offset >= total_count:
        break

if not all_customers:
    print("No customers fetched.")
    exit()

print(f"\nTotal customers fetched: {len(all_customers)}")

# --------------------------------------------------
# BUILD HIERARCHY WITH STATUS
# --------------------------------------------------
standalone = []
msp_dict = {}
tenant_map = {}

for c in all_customers:
    name = c.get("contact", {}).get("company_name", "")
    customer_id = c.get("customer_id", "")
    parent_id = c.get("msp_id") or c.get("parent_customer_id")
    acc_type = c.get("account_type", "")
    status = c.get("account", {}).get("status", "UNKNOWN")

    if not acc_type:
        continue

    acc_type_lower = acc_type.lower()

    if "standalone" in acc_type_lower:
        standalone.append((name, customer_id, status))

    elif "msp" in acc_type_lower:
        msp_dict[customer_id] = {
            "name": name,
            "customer_id": customer_id,
            "status": status
        }

    elif "tenant" in acc_type_lower:
        if parent_id:
            tenant_map.setdefault(parent_id, []).append({
                "name": name,
                "customer_id": customer_id,
                "status": status
            })

# --------------------------------------------------
# HTML
# --------------------------------------------------
html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Workspace Hierarchy</title>
<style>
body {{
    font-family: 'Segoe UI', sans-serif;
    background: #f4f6f9;
    padding: 40px;
}}

.container {{
    max-width: 1500px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.08);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}

th {{
    background: #e0e0e0;
}}

.status-ACTIVE {{ color: green; font-weight: bold; }}
.status-BLOCKED {{ color: red; font-weight: bold; }}
.status-SUSPENDED {{ color: orange; font-weight: bold; }}

.toggle-btn {{
    background: none;
    border: none;
    cursor: pointer;
    font-weight: bold;
}}

.tenant-wrapper {{
    display: none;
    margin-top: 6px;
}}
</style>

<script>
function toggleTenants(id) {{
    var element = document.getElementById(id);
    element.style.display = element.style.display === "none" ? "block" : "none";
}}
</script>

</head>
<body>

<div class="container">
<h2>Workspace Hierarchy for: {username}</h2>

<table>
<tr>
    <th>MAIL</th>
    <th colspan="3">Stand Alone</th>
    <th colspan="3">MSP WORKSPACE</th>
</tr>

<tr>
    <td>{username}</td>
    <th>Name</th>
    <th>Customer ID</th>
    <th>Status</th>
    <th>Name</th>
    <th>Customer ID</th>
    <th>Status</th>
</tr>
"""

msp_rows = []
counter = 0

for msp_id, msp_info in msp_dict.items():

    tenants = tenant_map.get(msp_id, [])
    unique_id = f"tenant{counter}"
    counter += 1

    tenant_html = ""

    if tenants:
        tenant_html += f"<div id='{unique_id}' class='tenant-wrapper'><table>"
        tenant_html += "<tr><th>Tenant Name</th><th>Customer ID</th><th>Status</th></tr>"

        for t in tenants:
            tenant_html += f"""
            <tr>
                <td>{t['name']}</td>
                <td>{t['customer_id']}</td>
                <td class="status-{t['status']}">{t['status']}</td>
            </tr>
            """

        tenant_html += "</table></div>"

    msp_block = f"""
    <button class="toggle-btn" onclick="toggleTenants('{unique_id}')">
        {msp_info['name']}
    </button>
    {tenant_html}
    """

    msp_rows.append((msp_block, msp_info["customer_id"], msp_info["status"]))

max_rows = max(len(standalone), len(msp_rows))

for i in range(max_rows):

    sa_name, sa_id, sa_status = standalone[i] if i < len(standalone) else ("", "", "")
    msp_name, msp_id, msp_status = msp_rows[i] if i < len(msp_rows) else ("", "", "")

    html += f"""
    <tr>
        <td></td>
        <td>{sa_name}</td>
        <td>{sa_id}</td>
        <td class="status-{sa_status}">{sa_status}</td>
        <td>{msp_name}</td>
        <td>{msp_id}</td>
        <td class="status-{msp_status}">{msp_status}</td>
    </tr>
    """

html += "</table></div></body></html>"

file_path = "workspace_hierarchy_status.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

webbrowser.open(os.path.abspath(file_path))

print("HTML file generated:", file_path)