from opentrons import protocol_api, types
from opentrons.protocol_api import PARTIAL_COLUMN, SINGLE, ALL
from opentrons.types import Point
import math
import urllib.request
import json
import ssl

metadata = {
    'protocolName': 'Nanopore Library Preparation',
    'author': 'Cradle',
    'description': 'Custom Protocol For Nanopore Library Preparation',
    'apiLevel': '2.20'
}

def run(ctx: protocol_api.ProtocolContext):
    # DNA sample input from 1 to 8 (do not exceed!)
    dna_samples = 8 
    assert 1 <= dna_samples <= 8, "Error: DNA samples must be between 1 and 8"

    mag_engage_height = 5 # Maximum magnet height depending on the plate
    pos = {1: 'H', 2: 'G', 3: 'F', 4: 'E', 5: 'D', 6: 'C', 7: 'B', 8: 'A'} # Input sample to well mapping for nozzle configuration
    pos_flipped = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'A'} # Input sample to well mapping for defining liquids
    west = Point(-1, 0, 0) # Well position left
    east = Point(1, 0, 0)  # Well position right

    # Load an additional 300uL tip rack if dna_samples is between 5 and 8
    tips300 = ctx.load_labware('opentrons_96_tiprack_300ul', '2')
    tips301 = None
    if 5 <= dna_samples <= 8:
        tips301 = ctx.load_labware('opentrons_96_tiprack_300ul', '5')
    # List of tip racks
    tip_racks = [tips300]
    if tips301:
        tip_racks.append(tips301)

    # Load 300ul 8-channel pipette & nozzle configuration
    m300 = ctx.load_instrument('p300_multi_gen2', mount='left', tip_racks=tip_racks)
    if dna_samples == 1: 
        m300.configure_nozzle_layout(style=SINGLE, start='H1', tip_racks=tip_racks)
    elif 2 <= dna_samples <= 7:
        m300.configure_nozzle_layout(style=PARTIAL_COLUMN, start='H1', end=f'{pos[dna_samples]}1', tip_racks=tip_racks) 

    # Load 20ul 8-channel pipette & nozzle configuration
    tips20 = ctx.load_labware('opentrons_96_tiprack_20ul', '3')
    m20 = ctx.load_instrument('p20_multi_gen2', mount='right', tip_racks=[tips20]) 
    if dna_samples == 1: 
        m20.configure_nozzle_layout(style=SINGLE, start='H1', tip_racks=[tips20])
    elif 2 <= dna_samples <= 7:
        m20.configure_nozzle_layout(style=PARTIAL_COLUMN, start='H1', end=f'{pos[dna_samples]}1', tip_racks=[tips20]) 
    
    # SINGLE configuration only operates when input = 1 sample
    # PARTIAL COLUMN configuration only operates when input = between 2 and 7
    # No action is needed if input = 8 samples

    # Load magnetic module
    magdeck = ctx.load_module('magnetic module gen2', '1')
    magplate = magdeck.load_labware('thermofisher_96_midi_storage_plate_800ul')
    
    # Depending on the input samples, different source locations are used.
    # - 1 sample = 1 tip attached = aspirate from A = transfer['A'] with SINGLE configuration.
    # - 2 samples = 2 tips attached = aspirate from A-B = transfer['B'] with PARTIAL_COLUMN configuration.
    # - 4 samples = 4 tips attached = aspirate from A-D = transfer['D'] with PARTIAL_COLUMN configuration.
    # - 8 samples = 8 tips attached = aspirate from A-H = transfer['A'] with no configuration.
    # The input dna_samples will be color-coded accordingly in the Opentrons app.

    # Reagents & Sample Wells (Row 2 is not in use)
    ampure_beads = magplate[f'{pos_flipped[dna_samples]}4']
    for i in range (24, 24+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("AMpure", "", "#8B4513"), 100) 
    ethanol = magplate[f'{pos_flipped[dna_samples]}5']
    for i in range (32, 32+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Ethanol", "", "#808080"), 400)
    nuclease_free_water = magplate[f'{pos_flipped[dna_samples]}6']
    for i in range (40, 40+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Nuclease Free Water", "", "#ADD8E6"), 61)
    ligation_buffer = magplate[f'{pos_flipped[dna_samples]}7']
    for i in range (48, 48+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Ligation Buffer", "", "#FFD700"), 25)
    ligase = magplate[f'{pos_flipped[dna_samples]}8']
    for i in range (56, 56+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Ligase", "", "#FF4500"), 10)
    ligation_adapter = magplate[f'{pos_flipped[dna_samples]}9']
    for i in range (64, 64+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Ligation Adapter", "", "#800080"), 5)
    fragment_buffer = magplate[f'{pos_flipped[dna_samples]}10']
    for i in range (72, 72+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Fragment Buffer", "", "#228B22"), 500)
    elution_buffer = magplate[f'{pos_flipped[dna_samples]}11']
    for i in range (80, 80+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Elution Buffer", "", "#00CED1"), 15)
    initial_sample = magplate[f'{pos_flipped[dna_samples]}1']
    for i in range (0, dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Initial Sample", "", "#1E90FF"), 60) 
    inter_sample = magplate[f'{pos_flipped[dna_samples]}3']
    for i in range (16, 16+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Intermediate Sample", "", "#FF8C00"), 0)
    final_sample = magplate[f'{pos_flipped[dna_samples]}12']
    for i in range (88, 88+dna_samples): magplate.wells()[i].load_liquid(ctx.define_liquid("Final Sample", "", "#32CD32"), 0)

    # Setting up starting_tip is not possible with partial pipetting

    ############################################################################################################################################################

    # Defining functions for modular approach  

    # Engages and disengages magnets
    def magnet(delay_sec):
        magdeck.engage(height_from_base=mag_engage_height)
        ctx.delay(seconds=delay_sec, msg='Allowing beads to pellet')
    def magnetoff():
        magdeck.engage(height_from_base=-2.5)

    # Resuspends liquids in a well (ideal for beads)    
    def resuspend(srcs, volume, mix_reps, mix_rate, liquid_top):
        for _ in range(mix_reps):
            m300.aspirate(volume, srcs.bottom(), rate=mix_rate)
            m300.dispense(volume, srcs.bottom(liquid_top), rate=mix_rate)
        m300.blow_out(srcs.bottom(liquid_top))

    # Transfers reagents with 300 ul pipette
    def transferreagent300(volume, air_gap, srcs, dest, liquid_top, mix_after=None): 
        m300.aspirate(volume, srcs.bottom(), rate=0.2)
        m300.move_to(srcs.top(), speed=50)
        m300.air_gap(air_gap)
        m300.move_to(dest.top(), speed=50)
        m300.dispense(volume+air_gap, dest.bottom(liquid_top), rate=0.2)
        m300.blow_out(dest.bottom(liquid_top))
        # Ensures reagent is mixed
        if mix_after:
            resuspend(dest, volume=mix_after)

    # Transfers reagents with 20 ul pipette
    def transferreagent20(volume, srcs, dest, liquid_top, mix_after=None): 
        m20.aspirate(volume, srcs.bottom(), rate=0.25)
        m20.move_to(srcs.top(), speed=50)
        m20.move_to(dest.top(), speed=50)
        m20.dispense(volume, dest.bottom(liquid_top), rate=0.25)
        m20.blow_out(dest.bottom(liquid_top))
        # Ensures reagent is mixed
        if mix_after:
            resuspend(dest, volume=mix_after)

    # Hula mix (resuspension duration is calculated based on the mixing volume)
    def hula_mix(srcs, volume, duration, liquid_top):
        repeats=math.ceil(duration/((volume*4)/(92.86*0.15)))
        m300.aspirate(5, srcs.bottom(), rate=0.2)
        for _ in range(repeats): 
            m300.aspirate(volume, srcs.bottom().move(east), rate=0.15)
            m300.dispense(volume, srcs.bottom(z=3).move(west), rate=0.15)
            m300.aspirate(volume, srcs.bottom().move(west), rate=0.15)
            m300.dispense(volume, srcs.bottom(z=3).move(east), rate=0.15)
        m300.dispense(5, srcs.bottom(liquid_top), rate=0.2)
        m300.blow_out(srcs.bottom(liquid_top))

    # Removes supernatant of a well with the 300 ul pipette
    def remove_supernatant300(srcs):
        m300.pick_up_tip()
        m300.aspirate(75, srcs.bottom(z=4).move(west), rate=0.15)
        m300.aspirate(75, srcs.bottom(z=2).move(west), rate=0.15)
        m300.aspirate(150, srcs.bottom().move(west), rate=0.15)
        m300.drop_tip()
    
    # Removes supernatant of a well with the 20 ul pipette
    def remove_supernatant20(srcs):
        m20.pick_up_tip()
        m20.aspirate(10, srcs.bottom(z=0.5))
        m20.aspirate(10, srcs.bottom())
        m20.drop_tip()

    # Collects eluate of a well with the 20 ul pipette
    def collect_eluate(pipette, volume, srcs, dest):
        pipette.pick_up_tip()
        pipette.aspirate(volume, srcs, rate=0.15)
        pipette.dispense(volume, dest, rate=0.15)
        pipette.drop_tip()    

    ############################################################################################################################################################
    # 60 // - // - // 60+40 // 500 // 61 // 25 // 10 // 5 // 450 // 15 // -     +5% volume or +2uL
    # S1 // - // S2 // AP // ETOH // NF // LNB // LG // LA // SFB // EB // S3
    # End repair: 7x 300uL tips, 3x 20uL tips -> 26 min run time
    # Adapter ligation: 
    #"""""""""""
    ###################### Bind DNA to AMPure XP beads ######################
    # Disengage Magnet
    magnetoff()
    # Transferring AMPure beads
    m300.pick_up_tip()
    resuspend(ampure_beads, volume=50, mix_reps=10, mix_rate=0.3, liquid_top=3)
    transferreagent300(60, 60, ampure_beads, initial_sample, liquid_top=4)
    ctx.delay(2)
    # Hula Mixing (300 seconds)
    hula_mix(initial_sample, 50, 300, liquid_top=5)
    m300.drop_tip()
    # Engage Magnet
    magnet(180)
    # Remove Supernatant    
    remove_supernatant300(initial_sample)
    remove_supernatant20(initial_sample)

    ###################### Washing beads with ethanol ######################
    for _ in range(2):
        # Aspirate Ethanol
        m300.pick_up_tip()
        m300.aspirate(200, ethanol, rate=0.25)
        m300.move_to(ethanol.top())
        m300.air_gap(50)
        # Dispense Ethanol
        m300.dispense(250, initial_sample.center().move(west), rate=0.25)
        m300.move_to(initial_sample.top())
        ctx.delay(15)
        # Remove Ethanol
        m300.aspirate(50, initial_sample.bottom(z=4).move(west), rate=0.15)
        m300.aspirate(75, initial_sample.bottom(z=2).move(west), rate=0.15)
        m300.aspirate(150, initial_sample.bottom().move(west), rate=0.15)
        m300.move_to(initial_sample.top(), speed=50)
        m300.air_gap(25)
        m300.drop_tip()

    ###################### Drying pellet after washing ######################
    remove_supernatant20(initial_sample)
    ctx.delay(180)
    remove_supernatant20(initial_sample)
    ctx.delay(60)
    # Disengage Magnet
    magnetoff()

    ###################### Elute DNA from beads ######################
    # Transfer Nuclease free water
    m300.pick_up_tip()
    m300.transfer(61, nuclease_free_water, initial_sample.bottom(z=4).move(east), new_tip='never')
    for _ in range(10):
        m300.aspirate(65, initial_sample.bottom(), rate=0.3)
        m300.dispense(65, initial_sample.bottom(z=3).move(east), rate=0.3)
    m300.blow_out(initial_sample.bottom(z=3))
    m300.drop_tip()
    ctx.delay(120)
    # Engage Magnet
    magnet(120)
    # Collect Eluate
    collect_eluate(m300, 60, initial_sample.bottom().move(west), inter_sample)

    #"""""""""""
    ###################### Add adapter ligation components ######################
    # Transfer Ligation Buffer (Viscous)
    # Move Pipette Tip
    m300.pick_up_tip()
    m300.move_to(ligation_buffer.top())
    m300.move_to(ligation_buffer.bottom(), speed=10)
    ctx.delay(5)
    # Aspirate
    m300.aspirate(25, ligation_buffer.bottom(), rate=0.05)
    ctx.delay(5)
    m300.move_to(ligation_buffer.top(), speed=10)
    m300.air_gap(15)
    # Dispense
    m300.move_to(inter_sample.bottom(z=3), speed=10)
    m300.dispense(40, inter_sample.bottom(z=3), rate=0.1)
    for _ in range(3):
        m300.aspirate(30, inter_sample.bottom(), rate=0.25)
        m300.dispense(30, inter_sample.bottom(z=3), rate=0.25)
    m300.blow_out(inter_sample.bottom(z=3))
    m300.drop_tip()

    # Transfer Ligase
    m20.pick_up_tip()
    transferreagent20(10, ligase, inter_sample, liquid_top=2)
    m20.drop_tip()
    # Transfer Ligation Adapter
    m20.pick_up_tip()
    transferreagent20(5, ligation_adapter, inter_sample, liquid_top=2)
    m20.drop_tip()
    # Resuspend
    m300.pick_up_tip()
    resuspend(inter_sample, volume=50, mix_reps=2, mix_rate=0.15, liquid_top=3)
    m300.drop_tip()
    # Incubate 10 minutes
    ctx.delay(600)

    ###################### Bind DNA to ampure beads ######################
    # Transferring AMPure beads
    m300.pick_up_tip()
    resuspend(ampure_beads, volume=50, mix_reps=10, mix_rate=0.3, liquid_top=3)
    transferreagent300(40, 60, ampure_beads, inter_sample, liquid_top=5)
    ctx.delay(2)
    # Hula mixing for 5 minutes
    hula_mix(inter_sample, 60, 300, liquid_top=5)
    m300.drop_tip()
    # Pellet on magnet
    magnet(180)
    # Remove supernatant
    remove_supernatant300(inter_sample)
    remove_supernatant20(inter_sample)

    ###################### Washing beads with fragment buffer ######################
    for _ in range(2):
        # Transfer fragment buffer
        magnetoff()
        m300.pick_up_tip()
        transferreagent300(225, 50, fragment_buffer, inter_sample, liquid_top=11)
        # Resuspend beads
        for _ in range(5):
            m300.aspirate(100, inter_sample.bottom().move(east), rate=0.3)
            m300.dispense(100, inter_sample.bottom(z=5).move(west), rate=0.3)
            m300.aspirate(100, inter_sample.bottom().move(west), rate=0.3)
            m300.dispense(100, inter_sample.bottom(z=5).move(east), rate=0.3)
            m300.aspirate(200, inter_sample.bottom(), rate=0.3)
            m300.dispense(200, inter_sample.bottom(z=5), rate=0.3)
        m300.blow_out(inter_sample.bottom(11))
        m300.drop_tip()
        # Pellet on magnet
        magnet(180)
        # Remove supernatant
        remove_supernatant300(inter_sample)
    
    # Drying pellet
    remove_supernatant20(inter_sample)
    ctx.delay(240)
    remove_supernatant20(inter_sample)
    ctx.delay(240)
    # Disengage magnet
    magnetoff()

    ###################### Elute DNA from beads ######################
    # Transfer elution buffer
    m20.pick_up_tip()
    transferreagent20(15, elution_buffer, inter_sample, liquid_top=1)
    m20.drop_tip()
    # Resupend beads
    m300.pick_up_tip()
    for _ in range(10):
        m300.aspirate(20, inter_sample.bottom().move(west), rate=0.15)
        m300.dispense(20, inter_sample.bottom(z=2).move(east), rate=0.15)
    m300.drop_tip()
    # Incubate 10 minutes
    ctx.delay(600)
    # Engage magnet
    magnet(180)
    # Collect eluate 
    collect_eluate(m20, 15, inter_sample.bottom().move(west), final_sample.bottom())
    
    
