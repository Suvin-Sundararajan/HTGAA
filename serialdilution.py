from opentrons import protocol_api
from datetime import datetime, timedelta

metadata = {
    'protocolName': 'Serial Dilution and Sampling for OD600 Experiment',
    'author': 'Suvin',
    'description': 'Incubate samples in 2 mL vials on the temperature module, take 60 µL from each vial, combine into PCR wells in the thermocycler, and prepare for OD600 measurements',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):

    # Load modules and labware
    temp_module = protocol.load_module('temperature module', '1')
    thermocycler = protocol.load_module('thermocycler')
    vial_rack = temp_module.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap', 'temp_module_vials')
    sample_plate = thermocycler.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 'thermocycler_sample_plate')
    tip_rack = protocol.load_labware('opentrons_96_tiprack_300ul', '4')
    
    # Pipettes
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tip_rack])

    # Set temperature module to 4°C for sample storage
    temp_module.set_temperature(4)

    # Set thermocycler to 37°C for bacterial growth
    thermocycler.set_block_temperature(37)
    thermocycler.open_lid()

    # Time intervals
    interval_minutes = 15
    total_duration_hours = 24
    number_of_intervals = (total_duration_hours * 60) // interval_minutes

    # Track the current well in the sample plate
    sample_well_index = 0

    # Function to take a sample
    def take_sample(source_vial_1, source_vial_2, dest_well):
        p300.pick_up_tip()
        p300.transfer(60, source_vial_1, dest_well, new_tip='never')
        p300.transfer(60, source_vial_2, dest_well, new_tip='never')
        p300.mix(3, 120, dest_well)  # Mix with the combined volume of 120 µL
        p300.drop_tip()

    # Start experiment
    start_time = datetime.now()
    for i in range(number_of_intervals):
        protocol.delay(minutes=interval_minutes)
        source_vial_1 = vial_rack.wells()[i % 24]
        source_vial_2 = vial_rack.wells()[(i + 1) % 24]
        dest_well = sample_plate.wells()[sample_well_index]
        take_sample(source_vial_1, source_vial_2, dest_well)
        sample_well_index += 1
        if sample_well_index >= len(sample_plate.wells()):
            break  # Stop if we run out of wells in the sample plate

    # End of experiment
    protocol.comment("Experiment complete. Samples are ready for OD600 measurements.")
