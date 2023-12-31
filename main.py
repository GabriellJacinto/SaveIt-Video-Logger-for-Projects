from src.application import Application
from codecarbon import EmissionsTracker

#tracker = EmissionsTracker()
#tracker.start()

if __name__ == "__main__":
    app = Application()
    app()

#tracker.stop()