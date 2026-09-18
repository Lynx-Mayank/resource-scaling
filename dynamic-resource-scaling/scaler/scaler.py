import subprocess
import time

DEPLOYMENT = "scaling-demo"

MIN_REPLICAS = 1
MAX_REPLICAS = 5

SCALE_UP_THRESHOLD = 70
SCALE_DOWN_THRESHOLD = 30

CHECK_INTERVAL = 15


def get_replicas():
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "deployment",
            DEPLOYMENT,
            "-o",
            "jsonpath={.spec.replicas}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return int(result.stdout)


def get_cpu_usage():
    result = subprocess.run(
        [
            "kubectl",
            "top",
            "pods",
            "-l",
            "app=scaling-demo",
            "--no-headers",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    lines = result.stdout.strip().splitlines()

    if not lines:
        return 0

    total_cpu = 0
    pod_count = 0

    for line in lines:
        parts = line.split()

        if len(parts) >= 2:
            cpu = parts[1]

            if cpu.endswith("m"):
                cpu_value = int(cpu[:-1])
            else:
                cpu_value = int(cpu) * 1000

            total_cpu += cpu_value
            pod_count += 1

    if pod_count == 0:
        return 0

    # Convert total CPU usage to percentage
    # based on 500m CPU container limit.
    average_cpu = total_cpu / pod_count
    percentage = (average_cpu / 500) * 100

    return percentage


def scale(replicas):
    print(f"Scaling deployment to {replicas} replicas...")

    subprocess.run(
        [
            "kubectl",
            "scale",
            "deployment",
            DEPLOYMENT,
            f"--replicas={replicas}",
        ],
        check=True,
    )


def main():
    print("Dynamic Resource Scaling Controller Started")
    print("------------------------------------------")

    while True:

        try:
            replicas = get_replicas()
            cpu = get_cpu_usage()

            print(
                f"CPU Usage: {cpu:.2f}% | "
                f"Replicas: {replicas}"
            )

            if cpu > SCALE_UP_THRESHOLD and replicas < MAX_REPLICAS:

                print("High CPU detected → SCALE UP")

                scale(replicas + 1)

            elif cpu < SCALE_DOWN_THRESHOLD and replicas > MIN_REPLICAS:

                print("Low CPU detected → SCALE DOWN")

                scale(replicas - 1)

            else:

                print("No scaling required")

        except Exception as e:

            print(f"Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()