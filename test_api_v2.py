import requests
import json
import datetime
import base64

BASE_URL = "https://dziennik.polandcentral.cloudapp.azure.com/api"
USERNAME = "wojciech_dzwonnik"
PASSWORD = "password123"


def get_token():
    url = f"{BASE_URL}/auth/login/"
    response = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
    if response.status_code == 200:
        return response.json()["access"]
    else:
        print(f"Login failed: {response.status_code} {response.text}")
        return None


def fetch_data(endpoint, token):
    url = f"{BASE_URL}{endpoint}"
    # Use both styles of Authorization to match frontend behavior
    headers = {
        "Authorization": f"Bearer {token}",
        # Add X-Authorization header as well
        "X-Authorization": f"Bearer {token}",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {endpoint}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def main():
    token = get_token()
    if not token:
        return

    # decode jwt payload simple way
    try:
        # Split token (header.payload.signature)
        parts = token.split(".")
        if len(parts) > 1:
            payload_part = parts[1]
            padding = "=" * (4 - len(payload_part) % 4)
            payload_part += padding

            # Decode
            payload_bytes = base64.urlsafe_b64decode(payload_part)
            payload_str = payload_bytes.decode("utf-8")
            decoded = json.loads(payload_str)

            print("--- Token Payload ---")
            print(json.dumps(decoded, indent=2))

            klasa_id = decoded.get("klasa_id")
            if not klasa_id:
                print("CRITICAL: 'klasa_id' is MISSING in the token!")
            else:
                print(f"DEBUG: 'klasa_id' found: {klasa_id}")

            uczen_id = decoded.get("uczen_id")

            print("\n--- API Test ---")
            if klasa_id:
                print(f"Fetching /plany-zajec/?klasa_id={klasa_id}")
                plans = fetch_data(f"/plany-zajec/?klasa_id={klasa_id}", token)
                if plans:
                    current_plan = sorted(plans, key=lambda x: x["id"], reverse=True)[0]
                    print(f"Found plan ID: {current_plan['id']}")

                    entries = fetch_data(
                        f"/plan-wpisy/?plan_id={current_plan['id']}", token
                    )
                    if entries:
                        print(f"Accessing /plan-wpisy/ worked. Count: {len(entries)}")
                        today = datetime.datetime.today().weekday() + 1
                        today_entries = [
                            e for e in entries if e.get("dzien_tygodnia") == today
                        ]
                        print(f"Entries for today (day {today}): {len(today_entries)}")
                        for e in today_entries:
                            # Print entry types
                            print(
                                f"  Entry: {e} dt_type:{type(e.get('dzien_tygodnia'))} gl_type:{type(e.get('godzina_lekcyjna'))} z_type:{type(e.get('zajecia'))}"
                            )
                    else:
                        print("Failed to get entries (or empty)")
                else:
                    print("Failed to get plans (or empty)")
            else:
                print("Cannot fetch plans without class ID")

    except Exception as e:
        print(f"Error decoding token: {e}")


if __name__ == "__main__":
    main()
