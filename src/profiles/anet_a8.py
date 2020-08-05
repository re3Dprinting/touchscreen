from octoprint.printer.profile import BedFormFactor
from octoprint.printer.profile import BedOrigin

anet_a8_profile = dict(
		id = "_anet_a8",
		name = "A8",
		model = "Anet A8",
		color = "default",
		volume=dict(
			width = 220,
			depth = 220,
			height = 240,
			formFactor = BedFormFactor.RECTANGULAR,
			origin = BedOrigin.LOWERLEFT,
			custom_box = False
		),
		heatedBed = True,
		heatedChamber = False,
		extruder=dict(
			count = 1,
			offsets = [
                            (0, 0)
			],
			nozzleDiameter = 0.4,
			sharedNozzle = False
		),
		axes=dict(
			x = dict(speed=6000, inverted=False),
			y = dict(speed=6000, inverted=True),
			z = dict(speed=200, inverted=False),
			e = dict(speed=300, inverted=False)
		)
	)
