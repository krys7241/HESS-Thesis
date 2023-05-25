'''paramaters related to renewable energy sources (pv for photovoltaic and wt for wind turbine)'''

pv_efficiency = 0.2
pv_area = 1.5
pv_number = 2700

wt_rated_power = 3000
wt_rated_speed = 16
wt_min_speed = 3
wt_number = 1

'''data related to batterie'''

'''economical (in euro per kWh)'''
bat_cost_kWh = 800/10

'''climat change for 2030 (in kgCO2eq per kWh)'''
'''bat_cost_kWh = 2.38/10'''

'''toxicity for 2030 (in kg1.4DCBeq per kWh)'''
'''bat_cost_kWh = 8.12/10'''

'''metal depletion (in kgFeeq per kWh)'''
'''bat_cost_kWh = 9.55/10'''

'''terrestrial acidification (in kgSO2eq per kWh)'''
'''bat_cost_kWh = 0.05/10'''

'''water depletion (in kgH2Oeq per kWh)'''
'''bat_cost_kWh = 0.05/10'''

bat_charge_efficiency = 0.95
bat_discharge_efficiency = 0.95
bat_max_charge = 0.5
bat_max_discharge = 0.5
bat_min_state_of_energy = 0.2
bat_max_state_of_energy = 0.95
bat_initial_state_of_energy = 0.5
bat_number_of_cycle_in_life_time = 4000

'''data related to water electrolizer'''

'''economical (in euro per kW per year)'''
we_cost_kW = 1500/14

'''climat change for 2030 (in kgCO2eq per kW per year)'''
'''we_cost_kW = 23.31/14'''

'''toxicity for 2030 (in kg1.4DCBeq per kW per year)'''
'''we_cost_kW = 5.08/14'''

'''metal depletion (in kgFeeq per kW per year)'''
'''we_cost_kW = 53.31/14'''

'''terrestrial acidification (in kgSO2eq per kW per year)'''
'''we_cost_kW = 5.78/14'''

'''water depletion (in kgH2Oeq per kW per year)'''
'''we_cost_kW = 0.29/14'''

we_SB_to_nominal_power = 0.02
we_off_to_nominal_power = 0.005
we_TUP = 0.5
we_MPL = 0.1
we_on_initial = 0
we_SB_initial = 0
we_off_initial = 1
we_efficiency = 52

'''data related to fuel cell'''

'''economical (in euro per kW per year)'''
fc_cost_kW = 1800/10

'''climat change for 2030 (in kgCO2eq per kW per year)'''
'''fc_cost_kW = 57.52/10'''

'''toxicity for 2030 (in kg1.4DCBeq per kW per year)'''
'''fc_cost_kW = 14.33/10'''

'''metal depletion (in kgFeeq per kW per year)'''
'''fc_cost_kW = 93.26/10'''

'''terrestrial acidification (in kgSO2eq per kW per year)'''
'''fc_cost_kW = 2.42/10'''

'''water depletion (in kgH2Oeq per kW per year)'''
'''fc_cost_kW = 0.41/10'''

fc_SB_to_nominal_power = 0.02
fc_off_to_nominal_power = 0.005
fc_TUP = 0.25
fc_MPL = 0.1
fc_on_initial = 0
fc_SB_initial = 0
fc_off_initial = 1
fc_efficiency = 20

'''data related to hydrogen tank'''

'''economical (in euro per kg per year)'''
ht_cost_kg = 450/25

'''climat change for 2030 (in kgCO2eq per kg per year)'''
'''ht_cost_kg = 727.7/25'''

'''toxicity for 2030 (in kg1.4DCBeq per kg per year)'''
'''ht_cost_kg = 70.48/25'''

'''metal depletion (in kgFeeq per kg per year)'''
'''ht_cost_kg = 25.88/25'''

'''terrestrial acidification (in kgSO2eq per kg per year)'''
'''ht_cost_kg = 3.3/25'''

'''water depletion (in kgH2Oeq per kg per year)'''
'''ht_cost_kg = 6.32/25'''

ht_min_state_of_energy = 0.2
ht_max_state_of_energy = 0.95
ht_initial_state_of_energy = 0.3
