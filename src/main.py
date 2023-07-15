from tasks import usom, phishtank

if __name__ == "__main__":
    # Start the phishtank() task
    phishtank.delay()

    # Start the usom() task
    usom.delay()

    