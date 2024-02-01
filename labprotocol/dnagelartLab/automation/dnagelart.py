# use 12 PCR tubes
# create a Python code for OT2 where
# n=5
# mix
# N15-n uL of nuclease-free water
# with
# 3ul of Lambda DNA at 1.5 ul concentration
# and
# NEB CutSmart Buffer at 1x concentration
# and
# n Enzymes each 1 ul at  uL (per enzyme) at 15 units (10 units/ug DNA)

# Place tubes in the 37ºC incubator. If enzymes show a “time saving icon,” incubate for 30 minutes otherwise 60 minutes

from opentrons import robot, protocol, types

# Define the number of PCR tubes
n_tubes = 12

# Define the number of enzymes
n_enzymes = 5

# Define the volumes
nuclease_free_water_vol = 15 - n_enzymes
lambda_dna_vol = 3
buffer_vol = 1

# Define the enzyme concentration
enzyme_concentration = 15  # units/uL
enzyme_volume = 1  # uL

# Define the incubation time based on enzyme time saving icon
time_saving_icon = False  # Replace with the actual logic to check for the icon
incubation_time = 60 if time_saving_icon else 30  # minutes

# Get the robot and pipette instances
robot = robot.Robot()
pipette = robot.instruments['ot2_robot'].pipettes['single']

# Labware setup
tiprack = robot.containers['tiprack_1']
tubes = robot.containers['tube_rack']

# Tip pickup
pipette.pick_up_tip(tiprack.wells('A1'))

# Dispense nuclease-free water
for tube in tubes.rows('A1'):
    pipette.transfer(
        nuclease_free_water_vol, tiprack.wells('A1'), tube, mix_after=True
    )

# Dispense Lambda DNA
pipette.transfer(
    lambda_dna_vol, tiprack.wells('A2'), tubes.columns()[:1], mix_after=True
)

# Dispense NEB CutSmart Buffer
pipette.transfer(
    buffer_vol, tiprack.wells('A3'), tubes.columns()[:1], mix_after=True
)

# Dispense enzymes
for i, enzyme in enumerate(tubes.columns()[1:]):
    pipette.transfer(
        enzyme_volume, tiprack.wells(f'A{i+4}'), enzyme, mix_after=True
    )

# Tip disposal
pipette.drop_tip(tiprack.wells('A9'))

# Incubation
robot.incubate(temperature=37, duration=incubation_time * minutes)

# Protocol complete
print(f"Protocol completed for {n_tubes} PCR tubes.")