from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well

metadata = {
    'protocolName': 'Dinosaur',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Draw a picture of a dinosaur',
    'apiLevel': '2.14'
}

# for OT  requirements block is optional so we will not include it for now. If included should remove API from metadata requirements = {"robotType": "OT-2", "apiLevel": "2.16"}
def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 1)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 2)
    plate:Labware = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)

    #water = protocol.define_liquid(    name="water",    description="Green colored water for testing",    display_color="#00FF00",)
    left_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])

    # action
    left_pipette.transfer(100, reservoir["A1"],   plate.wells_by_name()['A1'])              #,  mix_after(3, 50))

