import json

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'COVID-19 Ag unit dose repackaging protocol',
    'author': 'Riley Ramirez rramirez6821@gmail.com',
    'description': 'A protocol to repackage COVID-19 Antigens into individual PCR tubes for distribution with tests',
    'apiLevel': '2.10'
}


# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    if protocol.is_simulating:
        with open("FlowHealth_COVID19_96_unit_dose_plate.json") as file:
            labware_json = json.loads(file.read())
            labware_name = labware_json.get('metadata').get('displayName'
                                                        )
    # load our custom labware
    positions = [10, 11, 7, 8, 5, 4, 3, 2, 1]
    plates = []

    for platePos in positions:
        if protocol.is_simulating:
            plates.append(protocol.load_labware_from_definition(labware_json, platePos, labware_name))
        else:
            plates.append(protocol.load_labware('FlowHealth_COVID19_96_unit_dose_plate'), platePos)

    tip_rack = protocol.load_labware('opentrons_96_tiprack_300ul', '9')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', '6')

    # get 8n channel pipette
    left_pipette = protocol.load_instrument(
        'p300_multi_gen2', 'left', tip_racks=[tip_rack])

    tip_row = 0
    protocol.pause("place PCR tube trays into bed positions 10, 11, 7, 8, 5, 4, 3, 2, and 1, ensure the tips tray "
                   "in bed 11 is full, and antigen reservoir has at least 11200ul or 11.2ml of COVID-19 Antigen per "
                   "reservoir")
    while True:
        if tip_row == 12:
            protocol.pause("out of tips! resume when tips are added")
            tip_row = 0
        left_pipette.pick_up_tip(tip_rack.columns()[tip_row][0])
        tip_row += 1

        for index, plate in enumerate(plates):
            for col in plate.columns():
                left_pipette.transfer(200, reservoir.columns()[index], col[0], new_tip="never", trash=False)
        protocol.pause("Finished dispensing into units, replace with empty trays and replace COVID-19 Antigen")
        left_pipette.drop_tip()
        protocol.home()
