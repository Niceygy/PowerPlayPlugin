"""
PowerPlay Assistant EDMC Plugin
"""
from __future__ import annotations

import logging
import tkinter as tk

import myNotebook as nb  # noqa: N813
from config import appname, config
from ttkHyperlinkLabel import HyperlinkLabel  # Add this import near the top

# This **MUST** match the name of the folder the plugin is in.
PLUGIN_NAME = "PPA_EDMC"

logger = logging.getLogger(f"{appname}.{PLUGIN_NAME}")


class PowerPlayPlugin:
    """

    """
    

    def __init__(self) -> None:
        # Be sure to use names that wont collide in our config variables
        logger.info("PPA EDMC Plugin instantiated")
        self.user_current_system = ""
        self.system_var = tk.StringVar(value="")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.

        It is the first point EDMC interacts with our code after loading our module.

        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        return PLUGIN_NAME

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.

        It is the last thing called before EDMC shuts down. Note that blocking code here will hold the shutdown process.
        """
        self.on_preferences_closed("", False)  # Save our prefs

    def setup_preferences(self, parent: nb.Notebook, cmdr: str, is_beta: bool) -> nb.Frame | None:
        """
        setup_preferences is called by plugin_prefs below.

        It is where we can setup our own settings page in EDMC's settings window. Our tab is defined for us.

        :param parent: the tkinter parent that our returned Frame will want to inherit from
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        :return: The frame to add to the settings window
        """
        current_row = 0
        frame = nb.Frame(parent)

        # setup our config in a "Click Count: number"
        nb.Label(frame, text='PowerPlay Assistant').grid(row=current_row)
        nb.EntryMenu(frame, textvariable="PPA_BTN").grid(row=current_row, column=1)
        current_row += 1  # Always increment our row counter, makes for far easier tkinter design.
        return frame

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        """
        on_preferences_closed is called by prefs_changed below.

        It is called when the preferences dialog is dismissed by the user.

        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        """
        # You need to cast to `int` here to store *as* an `int`, so that

    def journal_entry(
        self, cmdr: str, is_beta: bool, system: str, station: str, entry: dict[str, any], state: dict[str, any]
    ) -> str | None:
        # Update current system from journal events
        if entry.get("event") in ("Location", "FSDJump"):
            new_system = entry.get("StarSystem") or system
            if new_system:
                self.user_current_system = new_system
                self.system_var.set(new_system)
        return None

    def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
        """
        Create our entry on the main EDMC UI.

        This is called by plugin_app below.

        :param parent: EDMC main window Tk
        :return: Our frame
        """
        current_row = 0
        frame = tk.Frame(parent)
        HyperlinkLabel(
            frame,
            text="Find PowerPlay Resources",
            url=f"https://elite.niceygy.net/?system_name={self.user_current_system}",
            underline=True
        ).grid(row=current_row)
        current_row += 1
        # tk.Label(frame, text="Current System:").grid(row=current_row, sticky=tk.W)
        # tk.Label(frame, textvariable=self.system_var).grid(row=current_row, column=1)
        return frame
    
    #PPA CODE
    
    def create_link(link: str):
        link = "https://elite.niceygy.net/"
        


cc = PowerPlayPlugin()


# Note that all of these could be simply replaced with something like:
# plugin_start3 = cc.on_load
def plugin_start3(plugin_dir: str) -> str:
    """
    Handle start up of the plugin.

    See PLUGINS.md#startup
    """
    return cc.on_load()


def plugin_stop() -> None:
    """
    Handle shutdown of the plugin.

    See PLUGINS.md#shutdown
    """
    return cc.on_unload()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> nb.Frame | None:
    """
    Handle preferences tab for the plugin.

    See PLUGINS.md#configuration
    """
    return cc.setup_preferences(parent, cmdr, is_beta)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """
    Handle any changed preferences for the plugin.

    See PLUGINS.md#configuration
    """
    return cc.on_preferences_closed(cmdr, is_beta)


def plugin_app(parent: tk.Frame) -> tk.Frame | None:
    """
    Set up the UI of the plugin.

    See PLUGINS.md#display
    """
    return cc.setup_main_ui(parent)