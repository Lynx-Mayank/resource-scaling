import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://127.0.0.1:5000/work"


def send_request():
    try:
        requests.get(URL, timeout=10)
    except requests.RequestException:
        pass


def generate_load(requests_per_second, duration):
    print(
        f"Load: {requests_per_second} requests/sec "
        f"for {duration} seconds"
    )

    end_time = time.time() + duration

    with ThreadPoolExecutor(max_workers=requests_per_second) as executor:
        while time.time() < end_time:
            start = time.time()

            for _ in range(requests_per_second):
                executor.submit(send_request)

            elapsed = time.time() - start

            if elapsed < 1:
                time.sleep(1 - elapsed)


def main():
    print("Dynamic Load Generator")
    print("======================")

    # Low load
    generate_load(5, 30)

    # Medium load
    generate_load(20, 30)

    # High load
    generate_load(50, 30)

    # Low load again
    generate_load(5, 30)

    print("Load test completed.")


if __name__ == "__main__":
    main()