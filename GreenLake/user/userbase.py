import requests
import urllib3
import webbrowser
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------------------------------
# 🔐 Paste your headers exactly like copied
# --------------------------------------------------
RAW_HEADERS = """
authorization
Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE2aTQ0dDNLTlVSRHUycTVKSU5NZVlvX2FtVV9SUzI1NiIsInBpLmF0bSI6IjFmN28ifQ.eyJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiY2xpZW50X2lkIjoiYXF1aWxhLXVzZXItYXV0aCIsImlzcyI6Imh0dHBzOi8vc3NvLmNvbW1vbi5jbG91ZC5ocGUuY29tIiwianRpIjoiQlFIQTRNdGFsb3JiazB6TGNiIiwibGFzdE5hbWUiOiJIdXNzYWluIiwic3ViIjoic3llZC1tYXNvb2QuaHVzc2FpbkBocGUuY29tIiwiYXVkIjoiYXVkIiwiYyI6IjUwOGNkOGM0LTUxYjUtNDUwMS04ZjA2LTU3YjIzZThlN2E3YSIsImF1dGhfc291cmNlIjoiaHBlIiwiZ2l2ZW5OYW1lIjoiU3llZCBNYXNvb2QiLCJpYXQiOjE3NzIzMjcyMDYsImV4cCI6MTc3MjMzNDQwNn0.pCklckE6XtIwUmEDNV951Ss8CSR8DflkmgZKdV-X7Sw1TOzLm0MZN5Qgl983eAjdAtXAqBxjHZD6JAn_pRuN3PSUwLnz6IT5FEhxfAznOdF6pTIRuPOWSnuDrFSWIl8WDsobVrY178ggi4XdmE77B0hOYFfYiaz2tv8NHCbuq_MuE4WEGt0rGWSDyhO1nq7zmu_n0Xn1krtgx91RTrauG3UAusll-1pD24Zt-BNS1L8f-txpdnZCZJRTOglI-IzNbIeFxBVlXxM1-ujKbI3owGmtBLwGahDJIpS7D01wOkYu9iKiLVKmtiMDnJ3U4sAmgDpE-Px7yb5i6-4NMGkeqA
cookie
notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; optout_domains_pc=; drift_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; driftt_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; _mkto_trk=id:117-SZC-407&token:_mch-hpe.com-bbe7b9487e76baae371e01ed53442ad; s_ecid=MCMID%7C27457408545680224153679487991052136343; _ga=GA1.1.37299827.1770224817; _gcl_au=1.1.188344893.1770316432; coveo_visitorId=a0f5d633-ba2d-4547-a6dd-e128659503a1; lang=en; cc=in; kndctr_56B5A25055667EED7F000101_AdobeOrg_identity=CiYyNzQ1NzQwODU0NTY4MDIyNDE1MzY3OTQ4Nzk5MTA1MjEzNjM0M1IRCOLoibXXMhgBKgRJTkQxMAHwAdzdk4TKMw%3D%3D; _uetvid=3d313a20420e11f099d051fbedc2727d|12vvtld|1763234352536|1|1|bat.bing.com/p/insights/c/l; RT="z=1&dm=hpe.com&si=e335455d-f500-438a-8332-c03aba1ca74f&ss=mm5brqai&sl=0&tt=0"; mbox=session%2327457408545680224153679487991052136343%2DtuRgOx%231772224790; _ga_3YZ812RSQH=GS2.1.s1772222939$o2$g0$t1772222943$j56$l0$h0; AMCV_56B5A25055667EED7F000101%40AdobeOrg=179643557%7CMCMID%7C27457408545680224153679487991052136343%7CMCIDTS%7C20511%7CMCAID%7CNONE%7CMCOPTOUT-1772230157s%7CNONE%7CMCAAMLH-1772827757%7C12%7CMCAAMB-1772827757%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C5.5.0; fs_uid=#11CH4F#b87427ea-2f2a-4342-9bb6-c735aae503d9:643f80f6-209a-4f79-86fe-03b595198e73:1772222956077::1#b3faeaaf#/1803664526; isMfe=true; i18next=en-US; TAsessionID=db4802ec-3396-431d-be0d-9d77e279b6fa|EXISTING; notice_behavior=implied,eu; _abck=4E0CF9E29DBE2E801FD5A79A3B1336E8~0~YAAQZwHARcPVcmecAQAA9fbupg/Wmh8aIkXEIdLKXAB6DQqRsf8FXupRcVr00qrW09Va+PBHvb06/TWhatVlwRv3Cm3QXdfrMlmv3Vo9LlH8OxVjJ9u9eMhWd3xnj+4Dt/GqebQkWkczJkXHot8DFTkWjzHS9gR1FLNpkIDfTtGT71NmB9ElO2azNAERNArt1xJw9YfkQxR7UChuex/qum+ZMkNvl+Q+4j2KyhKQq2z0++hApDZHidWRSMWP866ctuQnbCgd0H7lJXgevp4RQJ3VoNDiuwBkZLN0VGdqfrobDOx1OkiHBJm45C0PKKbSCNr9ekc0Ex+78G6IEmAMx5slTD+Y1kbdcRF4yANA7awN/Hc6IMnbxXvBZEkq9S2OimmYCFcz6On5qjSwvYUioL44qISoW+Bkei3vxnQMrFZL/FP7CRT4yLKQ6nGc2WiImGcEOxKnB3TaIPYrf7YHwGBwY+hOfjacKNBEjP+ugcEP8n7DuJS2hdyXDQHIs+us2PJZ0J4JLBcvE2utbtPgSDQiPDDUC2SCYnJDJGn666cxqXEcLzKzLqmv8dTTfkBKVlXSnpw82KVJYl96SvfwO3IlCgC74wUN//LvXEG5jFglolf4nodIn/FSmMh20Q==~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f2JWnErG6WxSk2MIYxQalEUu3CEp3xHT7UuYKn1jGcf7O52zLb38r5BthyaR0ivBRTpljVL9psG+ee5N3C3LQuzH48KuNjJH3nLGjd79NaVQYxk+4725qMcOq%2faZ9%2fEULbcoV8k%3d~-1; ccs-pf-id=0DuC-d8mx8QgyxPjZLyqQkkqqbc..o5Ee.dRjdGXSZN1tXW660w4ZVnw3lw; ccs-old-style-pf-id=0DuC-d8mx8QgyxPjZLyqQkkqqbc..o5Ee.dRjdGXSZN1tXW660w4ZVnw3lw; AMP_ca3a475ee4=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3NDAzZjgzMS1hMzFiLTRkZGYtYWMxNS04YzhlNmY3MWE4MTUlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI4MzI4NTlkNmEyMGM0MGYwNjQ0MTM4YTU2M2NhODhkOTAwYzQ2NmMwNjU0NTNiZjg2YmZiZGY4MjI1YWRmODMzJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc3MjMyNzIwODU5NSUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NzIzMjcyMzAxMTklMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTYlMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; ccs-session=eyJzZXNzaW9uaWQiOiAiNmJhMzdlZWJkMGFjODE3YWM3MTI3ZGZjMTQxODE5OTciLCAiY2NzLWNzcmZ0b2tlbiI6ICIwNzJjNzJhODk3OTIxMGNiODNkNmFkNmUzNmJkOTBlMDI1OTBmMDkyIn0=.aaORUg.gehDSuQYrvdoV6qcwk5v9EgOE2w
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


# --------------------------------------------------
# API DETAILS
# --------------------------------------------------
headers = build_headers(RAW_HEADERS)

url = "https://common.cloud.hpe.com/api/glp/support-assistant/v1alpha1/customers"
username = "syed-masood.hussain@hpe.com"

limit = 50
offset = 0
all_customers = []

print("\nFetching workspaces...\n")

# --------------------------------------------------
# Pagination Loop
# --------------------------------------------------
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

    if response.status_code == 401:
        print("Session expired.")
        break

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
        print("All records fetched successfully.")
        break


if not all_customers:
    print("No customers fetched. Exiting.")
    exit()

print(f"Total customers fetched: {len(all_customers)}")


# --------------------------------------------------
# GROUP DATA
# --------------------------------------------------
standalone = []
msp = []
tenant = []

for c in all_customers:
    name = c.get("contact", {}).get("company_name", "")
    cid = c.get("customer_id", "")
    acc_type = c.get("account_type", "")

    if not acc_type:
        continue

    acc_type_lower = acc_type.lower()

    if "standalone" in acc_type_lower:
        standalone.append((name, cid))

    elif "msp" in acc_type_lower:
        msp.append((name, cid))

    elif "tenant" in acc_type_lower:
        tenant.append((name, cid))


print("Standalone:", len(standalone))
print("MSP:", len(msp))
print("Tenant:", len(tenant))


# --------------------------------------------------
# BUILD HTML TABLE
# --------------------------------------------------
max_rows = max(len(standalone), len(msp), len(tenant))

html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Workspace Summary</title>
<style>
body {{ font-family: Arial; padding: 20px; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th {{ background-color: #0073e6; color: white; }}
tr:nth-child(even) {{ background-color: #f2f2f2; }}
</style>
</head>
<body>

<h2>Workspace Summary for: {username}</h2>

<table>
<tr>
    <th>User</th>
    <th>Standalone Name</th>
    <th>Standalone ID</th>
    <th>MSP Name</th>
    <th>MSP ID</th>
    <th>Tenant Name</th>
    <th>Tenant ID</th>
</tr>
"""

for i in range(max_rows):

    s_name = standalone[i][0] if i < len(standalone) else ""
    s_id = standalone[i][1] if i < len(standalone) else ""

    m_name = msp[i][0] if i < len(msp) else ""
    m_id = msp[i][1] if i < len(msp) else ""

    t_name = tenant[i][0] if i < len(tenant) else ""
    t_id = tenant[i][1] if i < len(tenant) else ""

    user_cell = username if i == 0 else ""

    html += f"""
<tr>
    <td>{user_cell}</td>
    <td>{s_name}</td>
    <td>{s_id}</td>
    <td>{m_name}</td>
    <td>{m_id}</td>
    <td>{t_name}</td>
    <td>{t_id}</td>
</tr>
"""

html += """
</table>
</body>
</html>
"""

file_path = "grouped_workspaces.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

webbrowser.open('file://' + os.path.realpath(file_path))

print("HTML file generated:", file_path)