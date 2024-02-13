import opentrons.simulate

#protocol_file = open('/C:/a/diy/pythonProjects/HTGAA/labprotocol/cellfreeLab/automation/cellfree.py')
protocol_file = open('./labprotocol/cellfreeLab/automation/cellfree.py')
opentrons.simulate.simulate(protocol_file)