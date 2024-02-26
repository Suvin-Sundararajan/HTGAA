import opentrons.simulate
from typing import (
    TYPE_CHECKING,
    Generator,
    Any,
    Dict,
    List,
    Mapping,
    TextIO,
    Tuple,
    BinaryIO,
    Optional,
    Union,
)

#protocol_file = open('/C:/a/diy/pythonProjects/HTGAA/labprotocol/cellfreeLab/automation/cellfree.py')
protocol_file = open('/a/diy/pythonProjects/HTGAA/labprotocol/cellfreeLab/automation/cellfree.py')
#protocol_file = open('./labprotocol/cellfreeLab/automation/cellfree.py')
print("adrian print in sim 0")
messages=list()
messages=(opentrons.simulate.simulate(protocol_file, propagate_logs=True)[0])
m:Mapping
for m in messages:
    print(m) #.get(1))

    # exit
    # print(" nothing")
    # for key in m.items() :
    #     #print (key, " and " , m[key])
    #     print ( m[key])



