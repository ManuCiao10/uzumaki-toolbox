from nike.nikeTypes import Thread
from nike.backendlink import BackendLinkFlow
from nike.threads import RunningThreads


def Start():
    PIDS = [
        "CU1726-100",
        "408452-140",
        "AQ9129-103",
        "CW1590-100",
        "DD1391-103",
        "DR9654-001",
    ]

    PIDS = ["DD1391-103"]  # for testing purposes
    PIDS_RO = ["DH9765-001", "DO6485-600"]
    while True:
        for pid in PIDS_RO:
            if pid not in RunningThreads:
                RunningThreads[pid] = Thread(BackendLinkFlow, pid)
                RunningThreads[pid].start()
