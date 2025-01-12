import sys
import warnings

from widget.console import *

warnings.filterwarnings("ignore", category=DeprecationWarning)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    console = Console()
    console.show()

    sys.exit(app.exec())
