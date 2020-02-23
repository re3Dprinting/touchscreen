#!/usr/bin/env python

#################################################################

import logging

from octoprint.settings import settings
from octoprint import printer
from octoprint import plugin

from octoprint.printer.standard import Printer
from octoprint.printer import profile

from octoprint.filemanager import analysis, storage, FileDestinations, FileManager

from octoprint.events import GenericEventListener

from octoprint import filemanager
from octoprint import events

from profiles.gigabot import gigabot_profile
from profiles.anet_a8 import anet_a8_profile


#################################################################
# Octoprint classes

def setup_octoprint(persona):

    # Get the EventManager singleton
    event_manager = events.eventManager()

    #################################################################
    # This is the octoprint section

    # Initialize settings
    p_settings = settings(True)

    # Initialize plugin manager
    plugin.plugin_manager(True)

    # Initialize profile manager
    profile_manager = profile.PrinterProfileManager()
    profile_manager.save(gigabot_profile, allow_overwrite = True, make_default = True)

    # Create an analysis queue
    analysis_queue = analysis.AnalysisQueue({})

    # Set up the storage managers. The file manager will need a
    # storage manager, which is a dictionary.
    storage_managers = dict()

    # Create our local storage manager and add it to the dictionary.
    local_storage_manager = storage.LocalFileStorage(persona.localpath)
    storage_managers[FileDestinations.LOCAL] = local_storage_manager

    # Now we can create the file manager...
    file_manager = FileManager(analysis_queue, None, None, initial_storage_managers=storage_managers)

    # And now we can create the printer.
    printer = Printer(file_manager, analysis_queue, profile_manager)

    # This has to happen to start the event dispatching. Prior to
    # dispatching a STARTUP event, events will be queued but not
    # sent.
    event_manager.fire(events.Events.STARTUP)

    # Caller needs the printer and storage manager objects.
    return (printer, local_storage_manager)
