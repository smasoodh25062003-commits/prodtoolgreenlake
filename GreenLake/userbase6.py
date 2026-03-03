import requests
import urllib3
import webbrowser
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------------------------------
# 🔐 Paste your headers exactly like copied
# --------------------------------------------------
RAW_HEADERS = """
authorization
Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE2aTQ0dDNLTlVSRHUycTVKSU5NZVlvX2FtVV9SUzI1NiIsInBpLmF0bSI6IjFmN28ifQ.eyJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiY2xpZW50X2lkIjoiYXF1aWxhLXVzZXItYXV0aCIsImlzcyI6Imh0dHBzOi8vc3NvLmNvbW1vbi5jbG91ZC5ocGUuY29tIiwianRpIjoiSzJrdGJBREMwOVBKWkN3Z2trIiwibGFzdE5hbWUiOiJIdXNzYWluIiwic3ViIjoic3llZC1tYXNvb2QuaHVzc2FpbkBocGUuY29tIiwiYXVkIjoiYXVkIiwiYyI6IjUwOGNkOGM0LTUxYjUtNDUwMS04ZjA2LTU3YjIzZThlN2E3YSIsImF1dGhfc291cmNlIjoiaHBlIiwiZ2l2ZW5OYW1lIjoiU3llZCBNYXNvb2QiLCJpYXQiOjE3NzIzMzQzNTAsImV4cCI6MTc3MjM0MTU1MH0.ITJThgaDFiocOkDCxqAHFaYK_wyH56UnW1wjLcpv7zYSnJLFgGFH7p9zBjnlNOpn3pzZmbP83cUQ4kcn6Tzae-lCkXS82Ld_lyMOsqRUR-23xielRp1dORN1xnadg_thcy6JWZ24oVJIeL-SB2LqjMMin3o4_oF40Uq6TwjdMPP5a-eNVbWvcQ92dS90D2syhTQtK4SJogerxod3y2hUS3TdzgrlmMkQoQSXY5YnD_XUY9LTa5pinMtr8ZGwnALPAeBCm8omv9cVzZHC6t8p2UoqhCSGg7DhyIdKhi4AYtTa6YBJsYT9kJMp3dnUiaLJQR3Rnw3TM5tDJ57dMBvWDg
cookie
notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; optout_domains_pc=; drift_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; driftt_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; _mkto_trk=id:117-SZC-407&token:_mch-hpe.com-bbe7b9487e76baae371e01ed53442ad; s_ecid=MCMID%7C27457408545680224153679487991052136343; _ga=GA1.1.37299827.1770224817; _gcl_au=1.1.188344893.1770316432; coveo_visitorId=a0f5d633-ba2d-4547-a6dd-e128659503a1; lang=en; cc=in; kndctr_56B5A25055667EED7F000101_AdobeOrg_identity=CiYyNzQ1NzQwODU0NTY4MDIyNDE1MzY3OTQ4Nzk5MTA1MjEzNjM0M1IRCOLoibXXMhgBKgRJTkQxMAHwAdzdk4TKMw%3D%3D; _uetvid=3d313a20420e11f099d051fbedc2727d|12vvtld|1763234352536|1|1|bat.bing.com/p/insights/c/l; RT="z=1&dm=hpe.com&si=e335455d-f500-438a-8332-c03aba1ca74f&ss=mm5brqai&sl=0&tt=0"; mbox=session%2327457408545680224153679487991052136343%2DtuRgOx%231772224790; _ga_3YZ812RSQH=GS2.1.s1772222939$o2$g0$t1772222943$j56$l0$h0; AMCV_56B5A25055667EED7F000101%40AdobeOrg=179643557%7CMCMID%7C27457408545680224153679487991052136343%7CMCIDTS%7C20511%7CMCAID%7CNONE%7CMCOPTOUT-1772230157s%7CNONE%7CMCAAMLH-1772827757%7C12%7CMCAAMB-1772827757%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C5.5.0; fs_uid=#11CH4F#b87427ea-2f2a-4342-9bb6-c735aae503d9:643f80f6-209a-4f79-86fe-03b595198e73:1772222956077::1#b3faeaaf#/1803664526; isMfe=true; i18next=en-US; notice_behavior=implied,eu; _abck=4E0CF9E29DBE2E801FD5A79A3B1336E8~0~YAAQZwHARcPVcmecAQAA9fbupg/Wmh8aIkXEIdLKXAB6DQqRsf8FXupRcVr00qrW09Va+PBHvb06/TWhatVlwRv3Cm3QXdfrMlmv3Vo9LlH8OxVjJ9u9eMhWd3xnj+4Dt/GqebQkWkczJkXHot8DFTkWjzHS9gR1FLNpkIDfTtGT71NmB9ElO2azNAERNArt1xJw9YfkQxR7UChuex/qum+ZMkNvl+Q+4j2KyhKQq2z0++hApDZHidWRSMWP866ctuQnbCgd0H7lJXgevp4RQJ3VoNDiuwBkZLN0VGdqfrobDOx1OkiHBJm45C0PKKbSCNr9ekc0Ex+78G6IEmAMx5slTD+Y1kbdcRF4yANA7awN/Hc6IMnbxXvBZEkq9S2OimmYCFcz6On5qjSwvYUioL44qISoW+Bkei3vxnQMrFZL/FP7CRT4yLKQ6nGc2WiImGcEOxKnB3TaIPYrf7YHwGBwY+hOfjacKNBEjP+ugcEP8n7DuJS2hdyXDQHIs+us2PJZ0J4JLBcvE2utbtPgSDQiPDDUC2SCYnJDJGn666cxqXEcLzKzLqmv8dTTfkBKVlXSnpw82KVJYl96SvfwO3IlCgC74wUN//LvXEG5jFglolf4nodIn/FSmMh20Q==~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f2JWnErG6WxSk2MIYxQalEUu3CEp3xHT7UuYKn1jGcf7O52zLb38r5BthyaR0ivBRTpljVL9psG+ee5N3C3LQuzH48KuNjJH3nLGjd79NaVQYxk+4725qMcOq%2faZ9%2fEULbcoV8k%3d~-1; ccs-pf-id=0DuC-d8mx8QgyxPjZLyqQkkqqbc..o5Ee.dRjdGXSZN1tXW660w4ZVnw3lw; ccs-old-style-pf-id=0DuC-d8mx8QgyxPjZLyqQkkqqbc..o5Ee.dRjdGXSZN1tXW660w4ZVnw3lw; AMP_ca3a475ee4=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3NDAzZjgzMS1hMzFiLTRkZGYtYWMxNS04YzhlNmY3MWE4MTUlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI4MzI4NTlkNmEyMGM0MGYwNjQ0MTM4YTU2M2NhODhkOTAwYzQ2NmMwNjU0NTNiZjg2YmZiZGY4MjI1YWRmODMzJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc3MjMyNzIwODU5NSUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NzIzMjcyMzAxMTklMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTYlMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; ccs-session=eyJzZXNzaW9uaWQiOiAiNmJhMzdlZWJkMGFjODE3YWM3MTI3ZGZjMTQxODE5OTciLCAiY2NzLWNzcmZ0b2tlbiI6ICIwNzJjNzJhODk3OTIxMGNiODNkNmFkNmUzNmJkOTBlMDI1OTBmMDkyIn0=.aaPA-w.DhsNZrIl5ReQLILVKf2EAFOF19E
"""

# --------------------------------------------------
# BUILD HEADERS
# --------------------------------------------------

def build_headers(raw_text):
    lines = raw_text.strip().split("\n")
    headers = {}
    current_key = None
    current_value = []

    for line in lines:
        line = line.strip()

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


# --------------------------------------------------
# STATUS COLOR FUNCTION
# --------------------------------------------------

def status_sort_key(status):
    """Lower = first. BLOCKED first, then SUSPENDED, then ACTIVE, then others.

    Some APIs return variants like "BLOCKED_WORKSPACE" or "SUSPENDED_ACCOUNT",
    so we treat substring matches as well.
    """
    s = (status or "").strip().upper()
    if "BLOCK" in s:
        return 0
    if "SUSPEND" in s:
        return 1
    if "ACTIVE" in s:
        return 2
    return 3


def get_status_color(status):
    status = (status or "").upper()

    if status == "ACTIVE":
        return "#2e7d32"
    elif status == "SUSPENDED":
        return "#ef6c00"
    elif status == "BLOCKED":
        return "#c62828"
    else:
        return "#616161"


# --------------------------------------------------
# GET STATUS FROM CUSTOMER DETAIL API
# --------------------------------------------------

def get_customer_status(customer_id):
    detail_url = "https://common.cloud.hpe.com/api/glp/support-assistant/v1alpha1/customer-detail"

    params = {"platform_customer_id": customer_id}

    try:
        r = requests.get(
            detail_url,
            headers=headers,
            params=params,
            timeout=30,
            verify=False
        )

        if r.status_code == 200:
            data = r.json()
            return data.get("account", {}).get("status", "UNKNOWN")
        else:
            return "UNKNOWN"

    except:
        return "UNKNOWN"


# --------------------------------------------------
# FETCH CUSTOMERS (PAGINATION)
# --------------------------------------------------

headers = build_headers(RAW_HEADERS)

url = "https://common.cloud.hpe.com/api/glp/support-assistant/v1alpha1/customers"
username = "syed-masood.hussain@hpe.com"

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

print(f"\nTotal customers fetched: {len(all_customers)}")


# --------------------------------------------------
# FETCH STATUS IN PARALLEL (FAST 🚀)
# --------------------------------------------------

print("\nFetching status for each workspace (Parallel Mode)...\n")

total_workspaces = len(all_customers)
processed = 0
status_map = {}

MAX_WORKERS = 15  # You can increase to 20 if network allows

def fetch_status(customer):
    customer_id = customer.get("customer_id", "")
    status = get_customer_status(customer_id)
    return customer_id, status

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = [executor.submit(fetch_status, c) for c in all_customers]

    for future in as_completed(futures):
        customer_id, status = future.result()
        status_map[customer_id] = status

        processed += 1
        percent = (processed / total_workspaces) * 100

        print(
            f"\rProcessed {processed}/{total_workspaces} "
            f"({percent:.1f}%)",
            end=""
        )

print("\n\nStatus fetching completed ✔")


# --------------------------------------------------
# BUILD HIERARCHY
# --------------------------------------------------

standalone = []
msp_dict = {}
tenant_map = {}

for c in all_customers:

    name = c.get("contact", {}).get("company_name", "")
    customer_id = c.get("customer_id", "")

    status = status_map.get(customer_id, "UNKNOWN")
    color = get_status_color(status)

    msp_parent_id = c.get("msp_id", "") or c.get("parent_customer_id", "")
    acc_type = c.get("account_type", "")

    if not acc_type:
        continue

    acc_type_lower = acc_type.lower()

    if "standalone" in acc_type_lower:
        standalone.append((name, customer_id, status, color))

    elif "msp" in acc_type_lower:
        msp_dict[customer_id] = {
            "name": name,
            "customer_id": customer_id,
            "status": status,
            "color": color
        }

    elif "tenant" in acc_type_lower:
        if msp_parent_id:
            tenant_map.setdefault(msp_parent_id, []).append({
                "name": name,
                "customer_id": customer_id,
                "status": status,
                "color": color
            })

# Sort: blocked first, then suspended, then active
standalone.sort(key=lambda x: (status_sort_key(x[2]), x[0]))
for k in tenant_map:
    tenant_map[k].sort(key=lambda t: (status_sort_key(t["status"]), t["name"]))
msp_sorted = sorted(msp_dict.items(), key=lambda item: (status_sort_key(item[1]["status"]), item[1]["name"]))

# --------------------------------------------------
# BUILD HTML OUTPUT — VIEW SWITCHER (UI vs SHEETS)
# --------------------------------------------------

# Flat rows for Sheets view: Type | Name | ID | Status | color | Parent ID
sheets_rows = []
for sa in standalone:
    sheets_rows.append(("Standalone", sa[0], sa[1], sa[2], sa[3], ""))
for msp_id, msp_info in msp_sorted:
    sheets_rows.append(("MSP", msp_info["name"], msp_id, msp_info["status"], msp_info["color"], ""))
    for t in tenant_map.get(msp_id, []):
        sheets_rows.append(("Tenant", t["name"], t["customer_id"], t["status"], t["color"], msp_id))

html = """
<!DOCTYPE html>
<html>
<head>
<title>Workspace Hierarchy</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: 'Segoe UI', sans-serif; background: #f4f6f9; padding: 20px 24px; margin: 0; box-sizing: border-box; }
*, *::before, *::after { box-sizing: border-box; }
.container { max-width: 100%; margin: auto; padding: 0 8px; }

.view-switcher {
    display: flex;
    gap: 0;
    margin-bottom: 24px;
    background: white;
    padding: 6px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    width: fit-content;
}
.view-switcher button {
    padding: 12px 28px;
    border: none;
    background: transparent;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    border-radius: 8px;
    color: #5f6368;
    transition: all 0.2s;
}
.view-switcher button:hover {
    background: #f0f2f5;
    color: #1a1a1a;
}
.view-switcher button.active {
    background: #1a73e8;
    color: white;
}

.view-panel { display: none; }
.view-panel.active { display: block; }

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.08);
    margin-bottom: 24px;
    overflow: hidden;
}

h2 { margin-top: 0; margin-bottom: 12px; font-size: 1.15rem; }

/* UI view: scrollable table containers — no overflow */
#view-ui .table-wrap {
    overflow-x: auto;
    overflow-y: auto;
    max-height: min(65vh, 480px);
    margin-top: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    -webkit-overflow-scrolling: touch;
}
#view-ui table {
    width: 100%;
    min-width: 320px;
    border-collapse: collapse;
    margin: 0;
}
#view-ui th, #view-ui td {
    border: 1px solid #e8eaed;
    padding: 10px 12px;
    vertical-align: middle;
    word-break: break-word;
    max-width: 280px;
}
#view-ui th {
    background: #f0f2f5;
    text-align: left;
    position: sticky;
    top: 0;
    z-index: 1;
    white-space: nowrap;
}
#view-ui tbody tr:nth-child(even) { background: #fafafa; }
#view-ui tbody tr:hover { background: #e8f0fe; }

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

th, td {
    border: 1px solid #ddd;
    padding: 10px;
    vertical-align: top;
}

th {
    background: #f0f2f5;
    text-align: left;
}

.badge {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
    color: white;
    display: inline-block;
    white-space: nowrap;
}

.toggle-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-weight: bold;
    font-size: 14px;
}

.tenant-wrapper {
    display: none;
    margin-top: 8px;
}
#view-ui .tenant-wrapper .table-wrap {
    max-height: min(40vh, 320px);
    margin-top: 8px;
}

#view-sheets .sheets-table { font-size: 13px; }
#view-sheets .sheets-table th {
    background: #1a73e8;
    color: white;
    position: sticky;
    top: 0;
    z-index: 1;
}
#view-sheets .sheets-table tbody tr:nth-child(even) { background: #f8f9fa; }
#view-sheets .sheets-table tbody tr:hover { background: #e8f0fe; }
#view-sheets .sheets-wrap {
    overflow-x: auto;
    max-height: 75vh;
    overflow-y: auto;
}
</style>

<script>
function setView(viewId) {
    document.querySelectorAll('.view-panel').forEach(function(el) { el.classList.remove('active'); });
    document.querySelectorAll('.view-switcher button').forEach(function(btn) { btn.classList.remove('active'); });
    document.getElementById(viewId).classList.add('active');
    var btn = document.querySelector('.view-switcher button[data-view="' + viewId + '"]');
    if (btn) btn.classList.add('active');
}
function toggleTenants(id) {
    var element = document.getElementById(id);
    var arrow = document.getElementById("arrow-" + id);
    if (element.style.display === "none") {
        element.style.display = "block";
        arrow.innerHTML = "▼";
    } else {
        element.style.display = "none";
        arrow.innerHTML = "▶";
    }
}
</script>
</head>
<body>
<div class="container">
<div class="view-switcher">
    <button type="button" class="active" data-view="view-ui" onclick="setView('view-ui')">View as UI</button>
    <button type="button" data-view="view-sheets" onclick="setView('view-sheets')">View as Sheets</button>
</div>

<div id="view-ui" class="view-panel active">
"""

# --------------------------------------------------
# STANDALONE TABLE
# --------------------------------------------------

html += """
<div class="card">
<h2>Stand Alone Workspaces</h2>
<div class="table-wrap">
<table>
<tr>
<th>Name</th>
<th>ID</th>
<th>Status</th>
</tr>
"""

for sa in standalone:
    html += f"""
    <tr>
        <td>{sa[0]}</td>
        <td>{sa[1]}</td>
        <td><span class="badge" style="background:{sa[3]}">{sa[2]}</span></td>
    </tr>
    """

html += "</table></div></div>"

# --------------------------------------------------
# MSP TABLE
# --------------------------------------------------

html += """
<div class="card">
<h2>MSP Workspaces</h2>
<div class="table-wrap">
<table>
<tr>
<th>MSP Name</th>
<th>MSP ID</th>
<th>Status</th>
<th>Tenants</th>
</tr>
"""

for msp_id, msp_info in msp_sorted:

    tenants = tenant_map.get(msp_id, [])
    unique_id = f"tenant_{msp_id}"

    tenant_html = ""

    if tenants:
        tenant_html += f'<div id="{unique_id}" class="tenant-wrapper"><div class="table-wrap"><table>'
        tenant_html += "<tr><th>Tenant Name</th><th>ID</th><th>Status</th></tr>"

        for t in tenants:
            tenant_html += f"""
            <tr>
                <td>{t['name']}</td>
                <td>{t['customer_id']}</td>
                <td><span class="badge" style="background:{t['color']}">{t['status']}</span></td>
            </tr>
            """

        tenant_html += "</table></div></div>"

        tenant_button = f"""
        <button class="toggle-btn" onclick="toggleTenants('{unique_id}')">
            <span id="arrow-{unique_id}">▶</span> View Tenants ({len(tenants)})
        </button>
        {tenant_html}
        """
    else:
        tenant_button = "No Tenants"

    html += f"""
    <tr>
        <td>{msp_info['name']}</td>
        <td>{msp_id}</td>
        <td><span class="badge" style="background:{msp_info['color']}">{msp_info['status']}</span></td>
        <td>{tenant_button}</td>
    </tr>
    """

html += "</table></div></div>"
# --------------------------------------------------

html += """
</div>

<div id="view-sheets" class="view-panel">
<div class="card">
<h2>All Workspaces (Sheets View)</h2>
<div class="sheets-wrap">
<table class="sheets-table">
<thead>
<tr>
<th>Type</th>
<th>Name</th>
<th>ID</th>
<th>Status</th>
<th>Parent ID</th>
</tr>
</thead>
<tbody>
"""

for row in sheets_rows:
    type_, name, id_, status, color, parent_id = row
    html += f"""
    <tr>
        <td>{type_}</td>
        <td>{name}</td>
        <td>{id_}</td>
        <td><span class="badge" style="background:{color}">{status}</span></td>
        <td>{parent_id}</td>
    </tr>
    """

html += """
</tbody>
</table>
</div>
</div>
</div>
</div>
</body>
</html>
"""

output_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(output_dir, "workspace_hierarchy_table.html")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

os.startfile(file_path)