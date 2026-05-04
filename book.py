import requests
import os

BASE_URL = "https://uwe.leisurecloud.net/AWS/api"
TOKEN_URL = f"{BASE_URL}/token?locale=en_GB"
BOOK_URL = f"{BASE_URL}/Book"

USERNAME = os.environ.get("UWE_USERNAME")
PASSWORD = os.environ.get("UWE_PASSWORD")

BASE_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "authenticationkey": "M0bi1eProB00king$",
    "User-Agent": "iPhone",
}


def get_jwt():
    """Login and get a fresh JWT in one call."""
    headers = {
        **BASE_HEADERS,
        "user": USERNAME,
        "pw": PASSWORD,
    }
    response = requests.get(TOKEN_URL, headers=headers, timeout=10)
    data = response.json()

    if "jwtToken" not in data:
        raise Exception(f"Login failed: {data}")

    print(f"✅ Got JWT for member {data.get('memberId')}")
    return data["jwtToken"]


def book(session_id):
    """Login → get JWT → book."""
    jwt = get_jwt()

    headers = {
        **BASE_HEADERS,
        "authorisation": f"Bearer {jwt}",
    }
    payload = {
        "items": [
            {
                "sessionId": str(session_id),
                "includeKeyBookee": "true",
                "type": "class",
            }
        ],
        "locale": "en_GB",
    }

    response = requests.post(BOOK_URL, json=payload, headers=headers, timeout=10)
    data = response.json()

    if data.get("status") == "Booked":
        print(f"✅ BOOKED! Reference: {data.get('bookingRef')}")
        return True
    else:
        print(f"⚠️ Failed: {data}")
        return False


if __name__ == "__main__":
    book("655589")
