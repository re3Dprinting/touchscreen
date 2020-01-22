from octoprint.printer.profile import BedFormFactor
from octoprint.printer.profile import BedOrigin

gigabot_profile = dict(
		id = "_gigabot",
		name = "Gigabot",
		model = "re:3D Gigabot",
		color = "default",
		volume=dict(
			width = 600,
			depth = 600,
			height = 600,
			formFactor = BedFormFactor.RECTANGULAR,
			origin = BedOrigin.LOWERLEFT,
			custom_box = False
		),
		heatedBed = True,
		heatedChamber = False,
		extruder=dict(
			count = 2,
			offsets = [
			    (0, 0),
                            (0, 0)
			],
			nozzleDiameter = 0.4,
			sharedNozzle = False
		),
		axes=dict(
			x = dict(speed=6000, inverted=False),
			y = dict(speed=6000, inverted=False),
			z = dict(speed=200, inverted=False),
			e = dict(speed=300, inverted=False)
		)
	)

if __name__ == "__main__":

    from octoprint import settings

    from octoprint.printer.profile import PrinterProfileManager

    settings = settings.settings(True)

    profile_manager = PrinterProfileManager()
    print("Testing printer profile (no output means it's valid):")
    profile_manager._ensure_valid_profile(gigabot_profile)
