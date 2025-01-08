


ca_cert_path = "chain.crt"
# Keycloak token endpoint
url = "https://keycloak.dd.wwest.local/realms/dd-realm/protocol/openid-connect/token"

# Request payload
data = {
    "code": "80907af0-531a-4fef-be2f-9012da6c1905.08a479e4-5cc4-409d-847d-e9d464e8547c.7ae32108-eaf1-45ea-bd17-f2bd0266348e",  # Replace with actual code
    "grant_type": "authorization_code",
    "client_id": "testing_ddfe",
    "redirect_uri": "https://testing.dd.wwest.local/#iss=https://keycloak.dd.wwest.local/realms/dd-realm"
}

# Cookies extracted from the browser
cookies = {
    "AUTH_SESSION_ID": "47cfb5d5-e325-4609-9fad-871a6e8654e3.keycloak-0-22565",
    "AUTH_SESSION_ID_LEGACY": "47cfb5d5-e325-4609-9fad-871a6e8654e3.keycloak-0-22565",
    "KEYCLOAK_SESSION": "dd-realm/36f56d1b-dea1-4cb2-bdb1-13c2a0c9e5ed/47cfb5d5-e325-4609-9fad-871a6e8654e3",
    "KEYCLOAK_SESSION_LEGACY": "dd-realm/36f56d1b-dea1-4cb2-bdb1-13c2a0c9e5ed/47cfb5d5-e325-4609-9fad-871a6e8654e3",
    "KEYCLOAK_IDENTITY": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhZmYxZTc1ZS1kMzMzLTRhNjQtODcxZi0wNjZjMzM0YzFmY2MifQ.eyJleHAiOjE3MzYzODA0ODAsImlhdCI6MTczNjM0NDQ4MCwianRpIjoiYmRjY2Y4YzUtZjUzMi00Mzc3LWE4ZjktNjA0MDM3M2JkYmY0IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5kZC53d2VzdC5sb2NhbC9yZWFsbXMvZGQtcmVhbG0iLCJzdWIiOiIzNmY1NmQxYi1kZWExLTRjYjItYmRiMS0xM2MyYTBjOWU1ZWQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6IjQ3Y2ZiNWQ1LWUzMjUtNDYwOS05ZmFkLTg3MWE2ZTg2NTRlMyIsInNpZCI6IjQ3Y2ZiNWQ1LWUzMjUtNDYwOS05ZmFkLTg3MWE2ZTg2NTRlMyIsInN0YXRlX2NoZWNrZXIiOiI3TDlyT1VDcFF4QjFUZzBSNHM1eXNmS3lNZ0YtQVE1bGVBME11LVExMTVjIn0.ukLXAW05UjsXAkWDsIZtJaLJIpgcafzayostLENY6sA",
    "KEYCLOAK_IDENTITY_LEGACY": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhZmYxZTc1ZS1kMzMzLTRhNjQtODcxZi0wNjZjMzM0YzFmY2MifQ.eyJleHAiOjE3MzYzODA0ODAsImlhdCI6MTczNjM0NDQ4MCwianRpIjoiYmRjY2Y4YzUtZjUzMi00Mzc3LWE4ZjktNjA0MDM3M2JkYmY0IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5kZC53d2VzdC5sb2NhbC9yZWFsbXMvZGQtcmVhbG0iLCJzdWIiOiIzNmY1NmQxYi1kZWExLTRjYjItYmRiMS0xM2MyYTBjOWU1ZWQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6IjQ3Y2ZiNWQ1LWUzMjUtNDYwOS05ZmFkLTg3MWE2ZTg2NTRlMyIsInNpZCI6IjQ3Y2ZiNWQ1LWUzMjUtNDYwOS05ZmFkLTg3MWE2ZTg2NTRlMyIsInN0YXRlX2NoZWNrZXIiOiI3TDlyT1VDcFF4QjFUZzBSNHM1eXNmS3lNZ0YtQVE1bGVBME11LVExMTVjIn0.ukLXAW05UjsXAkWDsIZtJaLJIpgcafzayostLENY6sA"
}

# Additional headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Origin": "https://testing.dd.wwest.local",
    "Referer": "https://testing.dd.wwest.local/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

# Send the POST request
response = requests.post(url, data=data, cookies=cookies, headers=headers, verify=ca_cert_path)

# Check the response
if response.status_code == 200:
    token_data = response.json()
    print("Access token:", token_data.get("access_token"))
else:
    print("Failed to get token:", response.status_code, response.text)
