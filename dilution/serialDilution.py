# Perform serial dilutions to get 100 uM (0.1 mM) of a reagent called MS.
# use 3 1.5 ml eppendorf tubes  for dilutions
# use 15mL Falcon Tubes for H2O
# use 15mL Falcon Tubes for reagent
# use 20ul pipette tips
# Starting reagent concentration is 2.66 g/mL.
# use 3 steps

from opentrons import robot, protocol, types

metadata = {
    'apiLevel': '2.13',
    'protocolName': ' Dilution lab 1',
    'description': ''' Dilution lab 1''',
    'author': 'Adrian'
    } 


def run(protocol: protocol_api.ProtocolContext):
    # Define labware
    tube_rack = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 1)
    falcon_rack = protocol.load_labware("opentrons_15_tuberack_falcon_4x50ml_6x15ml_conical", 2)
    tiprack = protocol.load_labware("opentrons_96_filtertiprack_20ul", 3)

    # Define pipette
    pipette = protocol.load_instrument("p20_single_gen2", mount="right", tip_racks=[tiprack])

    # Define reagents and locations
    reagent_tube = falcon_rack["A1"]
    water_tube = falcon_rack["B1"]
    dilution_tubes = [tube_rack.wells()[i] for i in [0, 1, 2]]

    # Calculate volumes for each step
    initial_volume = 4.54  # uL, adjusted for slight overage
    transfer_volume = 20.0  # uL

    # Perform serial dilutions
    for i in range(3):
        pipette.pick_up_tip()
        pipette.aspirate(transfer_volume, reagent_tube)
        pipette.dispense(transfer_volume, dilution_tubes[i])
        pipette.mix(5, 20, dilution_tubes[i])  # Ensure thorough mixing
        pipette.blow_out(dilution_tubes[i])
        pipette.aspirate(transfer_volume, water_tube)
        pipette.dispense(transfer_volume, dilution_tubes[i])
        pipette.mix(5, 20, dilution_tubes[i])  # Ensure thorough mixing
        pipette.blow_out(dilution_tubes[i])
        pipette.drop_tip()

    # Optional: Further mixing for final dilution
    pipette.pick_up_tip()
    pipette.mix(10, 40, dilution_tubes[2])  # More intensive mixing for final dilution
    pipette.blow_out(dilution_tubes[2])
    pipette.drop_tip()