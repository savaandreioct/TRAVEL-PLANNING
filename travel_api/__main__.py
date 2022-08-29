#!/usr/bin/env python3
import os
from travel_api.config import ApiConfig


def main():
    ApiConfig.i("travel_api").app.run(
        host=os.environ.get("FLASK_RUN_HOST", "0.0.0.0"),
        port=os.environ.get("FLASK_RUN_PORT", "7203"),
        debug=True,
    )


if __name__ == "__main__":
    main()
