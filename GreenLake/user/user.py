import requests
import urllib3

# Disable SSL warnings (corporate SSL environments)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------------------------------
# 🔐 Paste your headers exactly like copied (with #)
# --------------------------------------------------
RAW_HEADERS = """
authorization
Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE2aTQ0dDNLTlVSRHUycTVKSU5NZVlvX2FtVV9SUzI1NiIsInBpLmF0bSI6IjFmN28ifQ.eyJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiY2xpZW50X2lkIjoiYXF1aWxhLXVzZXItYXV0aCIsImlzcyI6Imh0dHBzOi8vc3NvLmNvbW1vbi5jbG91ZC5ocGUuY29tIiwianRpIjoibjhRMWp1ZFV1WENQMzBaSTdnIiwibGFzdE5hbWUiOiJIdXNzYWluIiwic3ViIjoic3llZC1tYXNvb2QuaHVzc2FpbkBocGUuY29tIiwiYXVkIjoiYXVkIiwiYyI6IjUwOGNkOGM0LTUxYjUtNDUwMS04ZjA2LTU3YjIzZThlN2E3YSIsImF1dGhfc291cmNlIjoiaHBlIiwiZ2l2ZW5OYW1lIjoiU3llZCBNYXNvb2QiLCJpYXQiOjE3NzIxMDAyNjgsImV4cCI6MTc3MjEwNzQ2OH0.GN50oNRB01IKhFlb9wBs9rESWYRMdDMc7l1y9gbBvMHMdr62ShASe9dRFimVC_e4lTxZcPb_GidXVBC-ITC2lX-QQAv14p52wBA_JMf2NpMCI4-f6NLAaS7dcGNmLxge3Oep32-JcZ6wMN4WkwkpBiE-vpkGV2TYDceEoprb0GLUimA5yVFND-ivlAFFqsdnRM0W3R_JgJjj2SJbl8ncRns6qD5MYEaO_7gwKoZxgDCBosb-IrpC-PKk__q-uw3qzhson_fxg92bGnPJD4q3Dn9oUIE8GSPp-WDf7EHqqliNa55oqX-E2lZaoJvZMqKVpC24GK1U7GbbwvekmwNs8g
cookie
notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; optout_domains_pc=; drift_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; driftt_aid=b730365f-d809-4a2f-b7a5-2d9b091e1f86; _mkto_trk=id:117-SZC-407&token:_mch-hpe.com-bbe7b9487e76baae371e01ed53442ad; s_ecid=MCMID%7C27457408545680224153679487991052136343; _ga=GA1.1.37299827.1770224817; _gcl_au=1.1.188344893.1770316432; _ga_3YZ812RSQH=GS2.1.s1770830807$o1$g0$t1770830809$j58$l0$h0; coveo_visitorId=a0f5d633-ba2d-4547-a6dd-e128659503a1; mbox=session%2327457408545680224153679487991052136343%2DOQHVLz%231771437172; lang=en; cc=in; kndctr_56B5A25055667EED7F000101_AdobeOrg_identity=CiYyNzQ1NzQwODU0NTY4MDIyNDE1MzY3OTQ4Nzk5MTA1MjEzNjM0M1IRCOLoibXXMhgBKgRJTkQxMAHwAfievoXJMw%3D%3D; _uetvid=3d313a20420e11f099d051fbedc2727d|12vvtld|1763234352536|1|1|bat.bing.com/p/insights/c/l; AMCV_56B5A25055667EED7F000101%40AdobeOrg=179643557%7CMCMID%7C27457408545680224153679487991052136343%7CMCIDTS%7C20509%7CMCAID%7CNONE%7CMCOPTOUT-1772057688s%7CNONE%7CMCAAMLH-1772655288%7C12%7CMCAAMB-1772655288%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C5.5.0; RT="z=1&dm=hpe.com&si=e335455d-f500-438a-8332-c03aba1ca74f&ss=mm2ii8dg&sl=0&tt=0"; fs_uid=#11CH4F#20e48861-6183-4459-b871-1cd1a5b8885d:25f757a7-bf68-4aee-9424-57463a6774b7:1772052839457::1#d37775ce#/1803068815; isMfe=true; i18next=en-US; TAsessionID=70201da6-a109-4325-9eb9-1081c5ae8fb6|EXISTING; notice_behavior=implied,eu; ccs-pf-id=oYSS4bZLJMdb3cwzbN81dfZpNjM..oBc-.vcWVYmuMaj4GZ9qlVn456kQaE; ccs-old-style-pf-id=oYSS4bZLJMdb3cwzbN81dfZpNjM..oBc-.vcWVYmuMaj4GZ9qlVn456kQaE; _abck=4E0CF9E29DBE2E801FD5A79A3B1336E8~0~YAAQHAHARXTmj1KcAQAAIR1omQ9OTZBvPCovt7wScjm8Nes+gLB+hvtLYXgGp3K7z3doVaVT7SX4+t2LrDVsjmGoiBuIAiPqlvG9oA6+ckvOwEl0HnwANHT6zAtHs8tZcgCt7c1RS3pv7H6F/uVd2I1Gx80ThkwU3hFoScCFhjF/C4XQM2w/wRFbhYxLY+cA1+VswZSLmT4/tvQJ2mdrf1n+cBvG9DseGhn5G7ftt7T+C1fiN0u+6bxTesCjUz9KeOw4s7M5I7Nx1wbBRaK/tyvKN8xsIDThvRRxnE/Y9ip3XUweRH3usQleKxkzFByE86M4ltGigzcL0zJOV7aRCHviPaD73wsJZD2ylzkDKA+i93MczGkJP+dXJ5SNdT2KG1utYl/VH3nBbigE8POXBEy1Usso+uRO3CCcA+aw5aUbNaLLoP1AyZnWA75E8yi1dWahEDcoz/L5IMya80QE7Gtc2cWeMbw88fdz658WUZY7iSLzpViZfU8ImPHZu0zlQ2jFYskoCHngdJ7bfPGvscMY+DuFMg9Cxfp+4aFBoUooosT9FI+OTxZIOBNGd5js4W5bP/Mtvp500Ix3mdgjl+DkjyVVf+UIi43qC8OolOaJY5asfXG1X2FhQLUebNg0iCb3jlDj8WpmZgv1EQhlLVZokNru0sxQ~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f6DELM6jp%2fA1rVvGbQrC134%2f2jYwNvT7VoYPBSUOy1l4nVnpyZn3b7VK1sAqn7EszV2r5g5LeEhydl6XGPtqw3lYCcvRARKJ4rSLDkb%2f9W32aEEAM8sREnqcRWtYNACR046B5H3EJm6ulPuYJMeNC8xcKUUNj5+L9tSwScc6iw%3d%3d~-1; AMP_ca3a475ee4=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJlMWU2Yjk3OC01MWQ5LTRiMDYtOGY0Zi1kZThiNTE2N2M2MzIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI4MzI4NTlkNmEyMGM0MGYwNjQ0MTM4YTU2M2NhODhkOTAwYzQ2NmMwNjU0NTNiZjg2YmZiZGY4MjI1YWRmODMzJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc3MjA5OTQwMjA1NyUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NzIxMDAyNzYwNDIlMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTE0JTJDJTIycGFnZUNvdW50ZXIlMjIlM0EwJTdE; ccs-session=eyJzZXNzaW9uaWQiOiAiYjlhYzQ1YjcyNjczYzkwNGRiMjRlNmIzMWRkYmRhNjkiLCAiY2NzLWNzcmZ0b2tlbiI6ICI2N2JhNjhiNjhiN2Q2MjZlOGEyYTY1ZWI5YjAyZDVmOTBjMjc1ZWFjIn0=.aaAa0A.WmbAV6zIU79PJbtiL-XwHZUecpY"""

# --------------------------------------------------
# Header Builder (Your Logic – Fixed & Stable)
# --------------------------------------------------
def build_headers(raw_text):
    lines = raw_text.strip().split("\n")

    headers = {}
    current_key = None
    current_value = []

    for line in lines:
        line = line.strip()

        # Remove leading '#'
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


# Build headers
headers = build_headers(RAW_HEADERS)

# --------------------------------------------------
# API DETAILS
# --------------------------------------------------
url = "https://common.cloud.hpe.com/api/glp/support-assistant/v1alpha1/customers"
username = "vishal.kumar-ext@hpe.com"

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

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,      # Prevent hanging
            verify=False     # Helps in corporate SSL networks
        )
    except requests.exceptions.RequestException as e:
        print("Request Failed:", e)
        break

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        break

    data = response.json()

    customers = data.get("customers", [])
    pagination = data.get("pagination", {})

    all_customers.extend(customers)

    total_count = pagination.get("total_count", 0)
    count_per_page = pagination.get("count_per_page", 0)

    offset += count_per_page

    if offset >= total_count:
        break


# --------------------------------------------------
# Print Results
# --------------------------------------------------
# --------------------------------------------------
# Transform Data Per User (Store IDs instead of count)
# --------------------------------------------------

user_summary = {}

for c in all_customers:
    user_email = username  # API already filtered by username

    workspace_id = c.get("customer_id", "")
    acc_type = c.get("account_type", "").lower()
    status = c.get("account", {}).get("status", "")

    if user_email not in user_summary:
        user_summary[user_email] = {
            "standalone_ids": [],
            "msp_ids": [],
            "tenant_ids": [],
            "status": set()
        }

    if acc_type == "standalone":
        user_summary[user_email]["standalone_ids"].append(workspace_id)

    elif acc_type == "msp":
        user_summary[user_email]["msp_ids"].append(workspace_id)

        # Collect tenant IDs under MSP
        tenants = c.get("children", [])   # Adjust if API uses different key
        for t in tenants:
            tenant_id = t.get("customer_id", "")
            if tenant_id:
                user_summary[user_email]["tenant_ids"].append(tenant_id)

    if status:
        user_summary[user_email]["status"].add(status)


# --------------------------------------------------
# Print Table With IDs
# --------------------------------------------------

print("\nUser Workspace Summary:\n")

print(f"{'User Email':<35} {'Standalone IDs':<40} {'MSP IDs':<30} {'Tenant IDs':<40} {'Status':<15}")
print("-" * 170)

for user, data in user_summary.items():

    standalone_str = ", ".join(data["standalone_ids"])
    msp_str = ", ".join(data["msp_ids"])
    tenant_str = ", ".join(data["tenant_ids"])
    status_str = ", ".join(data["status"])

    print(f"{user:<35} "
          f"{standalone_str:<40} "
          f"{msp_str:<30} "
          f"{tenant_str:<40} "
          f"{status_str:<15}")

print("-" * 170)