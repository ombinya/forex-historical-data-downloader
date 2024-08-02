"""
This script serves as the entry point for running the main functionality of the program.
"""

from guimanager import GUIManager

if __name__ == "__main__":
    guimanager = GUIManager()
    guimanager.set_defaults()
    guimanager.show_gui()
    guimanager.close_gui()


