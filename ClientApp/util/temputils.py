def break_up_temperature_struct(data):

        ### Heated bed
        try:
            # Get the dictionary of bed temperatures and from it
            # extract the target and actual temperatures.

            # We have to do this inside an exception handler because
            # sometimes the data dictionary doesn't have bed
            # temperatures inside it (have seen this at startup
            # sometimes).
            bed_temp_dict = data["bed"]
            bed_target_temp = bed_temp_dict["target"]
            bed_actual_temp = bed_temp_dict["actual"]

            # Gather the bed temperatuse into a tuple
            bed_tuple = (bed_target_temp, bed_actual_temp)
            
        except:
            # Don't do anything (but also don't crash)
            bed_tuple = (None, None)

        ### Extruder 0

        try:
            # Get the dictionary of extruder-0 temperatures and from it
            # extract the target and actual temperatures.
            tool0_temp_dict = data["tool0"]
            tool0_target_temp = tool0_temp_dict["target"]
            tool0_actual_temp = tool0_temp_dict["actual"]

            # Gather the tool0 temperatuse into a tuple
            tool0_tuple = (tool0_target_temp, tool0_actual_temp)
        except:
            tool0_tuple = (None, None)

        ### Extruder 1

        try:
            # Get the dictionary of extruder-1 temperatures and from it
            # extract the target and actual temperatures.
            tool1_temp_dict = data["tool1"]
            tool1_target_temp = tool1_temp_dict["target"]
            tool1_actual_temp = tool1_temp_dict["actual"]

            # Gather the tool1 temperatuse into a tuple
            tool1_tuple = (tool1_target_temp, tool1_actual_temp)
        except:
            tool1_tuple = (None, None)

        # Return the broken-apart temperatures as a 3-tuple of 2-tuples
        return (bed_tuple, tool0_tuple, tool1_tuple)
