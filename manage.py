# -*- coding: utf-8 -*-
"""Create an application instance."""
from src.app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
