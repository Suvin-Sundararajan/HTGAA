from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
import time


INCUBATION_TIME=10 # fake constant
#see https://docs.opentron s.com/v2/tutorial.html for introduction to Opentron proramming and 
#https://pypi.org/project/opentrons/ for installing latest opentron lib "pip install --upgrade opentrons" from VSS console


metadata = {    "apiLevel": "2.14",    "protocolName": "Cell-Free protocol for HTGAA 2024",    "description": """The 2024 version of the lab is at 
                   https://howtogrowalmostanything.notion.site/Class-6-Cell-Free-Systems-05bf5e89d25a48feb557b5a26900bcec""",    "author": "adrian for HTGAA 2024"
    }

# for OT  requirements block is optional so we will not include it for now. If included should remove API from metadata requirements = {"robotType": "OT-2", "apiLevel": "2.16"}
def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 1)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 2)
    plate:Labware = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)

    water = protocol.define_liquid(    name="water",    description="Green colored water for testing",    display_color="#00FF00",)
    left_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])

    # action
    left_pipette.transfer(100, reservoir["A1"],   plate.wells_by_name()['A1'])              #,  mix_after(3, 50))
    protocol.pause("wait for incubation of", INCUBATION_TIME)
    time.sleep(1)# seconds
    protocol.resume("Finished incubation of", INCUBATION_TIME)

    # opentrons_simulate cellfree.py
    # This should generate a lot of output! As written, the protocol has about 1000 steps. If you’re curious how long that will take, you can use an experimental feature to estimate the time:
    # opentrons_simulate dilution-tutorial.py -e -o nothing

    ################## initial prtocol used to develop a draft code
    # water to total (at end)    # 9.60ul
    # Mg-glutamate (mM)    # 7.2ul
    # K-glutamate (mM)    # 2.8ul
    # DTT (mM)    # 1.2ul
    # energy mix current energy mix 2/17/2017 10x stock    # 6ul
    # amino acids 20mM stock (10x) 3/15/2017    # 6ul
    # Template    # 3ul
    # T7 (12/16)    # 3ul
    # Cell Free Prep    # 20ul