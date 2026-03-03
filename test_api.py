import requests
import json
import datetime

BASE_URL = "https://dziennik.polandcentral.cloudapp.azure.com/api"
USERNAME = "sebastian_cierpka"
PASSWORD = "password123"


def get_token():
    url = f"{BASE_URL}/auth/login/"
    print(f"DEBUG: Logging in to {url}")
    response = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
    print(f"DEBUG: Login status {response.status_code}")
    if response.status_code == 200:
        token = response.json().get("access")
        print(f"DEBUG: Token prefix: {token[:10]}...")
        return token
    else:
        print(f"Login failed: {response.status_code} {response.text}")
        return None


def fetch_data(endpoint, token):
    url = f"{BASE_URL}{endpoint}"
    # Add X-Authorization header as well
    headers = {"Authorization": f"Bearer {token}", "X-Authorization": f"Bearer {token}"}
    # print(f"DEBUG: Fetching {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to fetch {endpoint}: {response.status_code} Body: {response.text}"
        )
        return None


def main():
    token = get_token()
    if not token:
        return

    print("\n--- 0. Test Basic Auth (Przedmioty) ---")
    przedmioty = fetch_data("/przedmioty/", token)
    if przedmioty:
        print(f"Przedmioty count: {len(przedmioty)}")

    print("\n--- 1. Get User Context ---")
    # Assuming we know class ID or can find it. Let's list classes or just get plans directly if possible.
    # In the app, it does: getTimetablePlan(currentUser.classId)
    # We need to find the student's class ID first.
    users = fetch_data("/uczniowie/?user__username=" + USERNAME, token)
    if not users or len(users) == 0:
        print("Student not found")
        return

    student = users[0]
    class_id = student["klasa"]
    print(f"Student: {USERNAME}, Class ID: {class_id}")

    print("\n--- 2. Get Timetable Plan ---")
    plans = fetch_data(f"/plany-zajec/?klasa_id={class_id}", token)
    if not plans:
        print("No plans found")
        return

    # Sort by ID desc as in the app
    plans.sort(key=lambda x: x["id"], reverse=True)
    current_plan = plans[0]
    print(
        f"Current Plan ID: {current_plan['id']}, Valid From: {current_plan['ObowiazujeOdDnia']}"
    )

    print("\n--- 3. Get Plan Entries (Plan Wpisy) ---")
    entries = fetch_data(f"/plan-wpisy/?plan_id={current_plan['id']}", token)
    print(f"Entries count: {len(entries)}")
    today_dow = datetime.datetime.today().weekday() + 1
    # today_dow = 1 # Force Monday for testing if needed

    today_entries = [e for e in entries if e.get("dzien_tygodnia") == today_dow]
    print(f"Entries for today ({today_dow}): {len(today_entries)}")
    if len(today_entries) > 0:
        print("Sample Today Entry:", json.dumps(today_entries[0], indent=2))
        # Print all today entries
        for e in today_entries:
            print(
                f"ID: {e['id']}, HourID: {e['godzina_lekcyjna']}, Dzien: {e['dzien_tygodnia']}, ZajeciaID: {e['zajecia']}"
            )

    print("\n--- 4. Get Days of Week ---")
    days = fetch_data("/dni-tygodnia/", token)
    if days:
        print("Days:", json.dumps(days, indent=2))

    today_dow = (
        datetime.datetime.today().weekday() + 1
    )  # Monday is 0 in Python, 1 in DB??
    print(f"Today Python Weekday+1: {today_dow}")

    print("\n--- 5. Get Lesson Hours ---")
    hours = fetch_data("/godziny-lekcyjne/", token)
    if hours:
        print("Sample Hour:", json.dumps(hours[0], indent=2))

    print("\n--- 6. Get Zajecia ---")
    # In app: getZajecia()
    # Logic in app: subjects.forEach(s => subjectMap.set(s.id, s.nazwa || s.Nazwa));
    # zajecia.forEach(z => zajeciaMap.set(z.id, subjectMap.get(z.przedmiot) || 'Unknown'));
    zajecia = fetch_data("/zajecia/", token)
    if zajecia and len(zajecia) > 0:
        print("Sample Zajecia:", json.dumps(zajecia[0], indent=2))


if __name__ == "__main__":
    main()
