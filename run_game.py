# run_game.py
"""
This script serves as the entry point for running the Battleship game.

It imports the `main` function from the `battleship_game.src.main` module and executes it when the script is run directly.

Usage:
    python run_game.py
"""

import asyncio
from battleship_game.src.main import main

if __name__ == "__main__":
    asyncio.run(main())