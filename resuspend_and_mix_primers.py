#from opentrons import instruments, containers
from opentrons import protocol_api


# def make_ordered_list():
# 	l = []
# 	for col in range(12):
# 		for row in ["A", "B", "C", "D", "E", "F", "G", "H"]:
# 			l.append(row+str(col+1))
# 	return l

metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <opentrons@example.com>',
    'description': 'Simple protocol to get started using the OT-2',
    'apiLevel': '2.12'
}

# protocol run function
def run(ctx: protocol_api.ProtocolContext):
	# Load in everything
	tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', '5')]
	container = ctx.load_labware("opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", "3")
	plate = ctx.load_labware("thermoscientificnunc_96_wellplate_2000ul", "1")

	pip = ctx.load_instrument('p300_multi_gen2', 'right')

	num_channels_per_pickup = 1
	# (only pickup tips on front-most channel)

	per_tip_pickup_current = .1
	# (current required for picking up one tip, do not modify unless
	# you are using a GEN2 P20 8-Channel in which case change it to
	# 0.075)

	pick_up_current = num_channels_per_pickup * per_tip_pickup_current

	ctx._implementation._hw_manager.hardware._attached_instruments[
		pip._implementation.get_mount()
	].update_config_item('pick_up_current', pick_up_current)

	#tips_ordered = make_ordered_list()

	# For each, add 200 ul of water, then mix, then transfer to row F

	vol = 200

	tips_ordered = []
	for rack in tipracks:
		for row in rack.rows()[
		           len(rack.rows())
		           - num_channels_per_pickup::-1 * num_channels_per_pickup]:
			for tip in row:
				tips_ordered.append(tip)

	tip_count = 0
	mix_number = 50
	mix_volume = 100
	for row in ["A", "B"]:
		for col in range(11):
			col_str = str(col+1)

			# Pick up a tip
			pip.pick_up_tip(tips_ordered[tip_count])
			tip_count += 1

			# Aspirate from falcon
			pip.aspirate(200, container["A3"])

			# Add to plate then mix
			pip.mix(mix_number, mix_volume, plate[row+col_str])

			# Transfer to row F
			pip.aspirate(20, plate[row+col_str])
			pip.dispense(200, plate["F" + col_str])

			# Get rid of tip
			pip.drop_tip()





	#
	# tips_ordered = []
	# for rack in tipracks:
	# 	for row in rack.rows()[
	# 	           len(rack.rows())
	# 	           - num_channels_per_pickup::-1 * num_channels_per_pickup]:
	# 		for tip in row:
	# 			tips_ordered.append(tip)
	# tip_count = 0
	#
	# def pick_up(pip):
	# 	nonlocal tip_count
	# 	pip.pick_up_tip(tips_ordered[tip_count])
	# 	tip_count += 1
	#
	# for i in range(len(tips_ordered)):
	# 	pick_up(pip)
	# 	# perform some step
	# 	pip.drop_tip()
