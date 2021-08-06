import opentrons.simulate
protocol_file = open('protocol.py')
runlog, _bundle = opentrons.simulate.simulate(protocol_file)
# print the runlog
print(opentrons.simulate.format_runlog(runlog))