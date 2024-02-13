from typing import (   Dict,    List,    NamedTuple,    Optional,    Type,    Union,    Mapping,    cast,)
from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
from opentrons.protocol_api._liquid import Liquid
import logging


INCUBATION_TIME=1 # TODO change it to the actul required time
#see https://docs.opentron s.com/v2/tutorial.html for introduction to Opentron proramming and 
#https://pypi.org/project/opentrons/ for installing latest opentron lib "pip install --upgrade opentrons" from VSS console

metadata = {    "apiLevel": "2.14",    "protocolName": "Cell-Free protocol for HTGAA 2024",    "description": """The 2024 version of the lab is at 
                   https://howtogrowalmostanything.notion.site/Class-6-Cell-Free-Systems-05bf5e89d25a48feb557b5a26900bcec""",    "author": "adrian for HTGAA 2024"}

# for OT2 the requirements block is optional so we will not include it for now. If included should remove API from metadata requirements = {"robotType": "OT-2", "apiLevel": "2.16"}
stockLiquids:Dict=dict()
logger = logging.getLogger(__name__)

def stockLiquid (well:Well, volume, liquid:Liquid) -> Liquid:
    stockLiquids[liquid.name]= well
    well.load_liquid(liquid, volume)
    return liquid

def total(stockLiquids:Dict):
    total=0
    for l in stockLiquids:
        total=total+2
    return 0  

def run(protocol: protocol_api.ProtocolContext):
    print("Starting Cell Free Protocol using https://howtogrowalmostanything.notion.site/Class-6-Cell-Free-Systems-05bf5e89d25a48feb557b5a26900bcec info ")
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 1)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 2)
    plate:Labware = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    left_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])
    # define liquids
    water=stockLiquid( reservoir["A9"], 50, protocol.define_liquid( name="water", description="water to total (at end)    # 9.60ul", display_color="#00FF00",))
    mgGlutamate: Liquid= stockLiquid( reservoir["A1"], 50, protocol.define_liquid( name="mgGlutamate", description="Mg-glutamate (mM) 7.2ul", display_color="#00FF00",))
    kGlutamate=stockLiquid( reservoir["A2"], 50, protocol.define_liquid( name="kGlutamate", description="K-glutamate (mM)    # 2.8ul", display_color="#FF0000",))
    ddt=stockLiquid( reservoir["A3"], 50, protocol.define_liquid( name="ddt", description="DTT (mM)    # 1.2ul", display_color="#00FF00",))
    energy10x=stockLiquid( reservoir["A4"], 50, protocol.define_liquid( name="energy", description="energy mix current energy mix 2/17/2017 10x stock    # 6ul", display_color="#0000FF",))
    aminoAcids20x=stockLiquid( reservoir["A5"], 50, protocol.define_liquid( name="aminoAcids20x", description="amino acids 20mM stock (10x) 3/15/2017    # 6ul", display_color="#00FF00",))
    template=stockLiquid( reservoir["A6"], 50, protocol.define_liquid( name="template", description="Template    # 3ul", display_color="#00FF00",))
    t7=stockLiquid( reservoir["A7"], 50, protocol.define_liquid( name="t7", description="T7 (12/16)    # 3ul", display_color="#00FF00",))
    cellFree=stockLiquid( reservoir["A8"], 50, protocol.define_liquid( name="cellFree", description="Cell Free Prep    # 20ul", display_color="#00FF00",))
    totalLiquids=9.6 #total(stockLiquids)

    # action
    #print(stockLiquids)
    onePot=plate.wells_by_name()['A1']
    left_pipette.transfer(9.6, stockLiquids.get(water.name), onePot )              #,  mix_after(3, 50))

    left_pipette.transfer(7.2, stockLiquids.get(mgGlutamate.name), onePot )   
    left_pipette.transfer(2.8, stockLiquids.get(kGlutamate.name), onePot )   
    left_pipette.transfer(1.2, stockLiquids.get(ddt.name), onePot )  

    # energy is 10x stock so we need to dilute to working concentration 
    energyWorking=stockLiquid( reservoir["A10"], 0, protocol.define_liquid( name="energyWorking", description="energy at working concentration", display_color="#00FF00",))
    left_pipette.transfer(27, stockLiquids.get(water.name), stockLiquids.get(energyWorking.name ))
    left_pipette.transfer(3, stockLiquids.get(energy10x.name), stockLiquids.get(energyWorking.name ))

    left_pipette.transfer(6, stockLiquids.get(energyWorking.name), onePot )   

    # amino acids are 20x stock so we need to dilute to working concentration
    aminoAcidsWorking=stockLiquid( reservoir["A10"], 0, protocol.define_liquid( name="aminoAcidsWorking", description="energy at working concentration", display_color="#00FF00",))
    left_pipette.transfer(57, stockLiquids.get(water.name), stockLiquids.get(aminoAcidsWorking.name ))
    left_pipette.transfer(3, stockLiquids.get(aminoAcids20x.name), stockLiquids.get(aminoAcidsWorking.name ))

    left_pipette.transfer(6, stockLiquids.get(aminoAcidsWorking.name), onePot )
    left_pipette.transfer(3, stockLiquids.get(template.name), onePot )
    left_pipette.transfer(3, stockLiquids.get(t7.name), onePot)
    left_pipette.transfer(20, stockLiquids.get(cellFree.name), onePot )

    protocol.delay(INCUBATION_TIME,0,"delay for "+str(INCUBATION_TIME))

    # opentrons_simulate cellfree.py
    # If you’re curious how long that will take, you can use an experimental feature to estimate the time:
    # opentrons_simulate dilution-tutorial.py -e -o nothing

    ################## initial prtocol used to develop the code
    # water to total (at end)    # 9.60ul
    # Mg-glutamate (mM)    # 7.2ul
    # K-glutamate (mM)    # 2.8ul
    # DTT (mM)    # 1.2ul
    # energy mix current energy mix 2/17/2017 10x stock    # 6ul
    # amino acids 20mM stock (10x) 3/15/2017    # 6ul
    # Template    # 3ul
    # T7 (12/16)    # 3ul
    # Cell Free Prep    # 20ul