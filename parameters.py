'''paramaters related to renewable energy sources (pv for photovoltaic and wt for wind turbine)'''

pv_efficiency = 0.2
pv_area = 1.5
pv_number = 2700

wt_rated_power = 3000
wt_rated_speed = 16
wt_min_speed = 3
wt_number = 3

'''data related to batterie'''

'''economical (in euro per kWh)'''
bat_cost_kWh = 800

'''environmental (in kgCO2eq per kWh)'''
'''bat_cost_kWh = 3.58'''

'''environmental for 2030 (in kgCO2eq per kWh)'''
'''bat_cost_kWh = 2.22'''

bat_charge_efficiency = 0.95
bat_discharge_efficiency = 0.95
bat_max_charge = 0.5
bat_max_discharge = 0.5
bat_min_state_of_energy = 0.2
bat_max_state_of_energy = 0.95
bat_initial_state_of_energy = 0.5
bat_number_of_cycle_in_life_time = 4000

'''data related to water electrolizer'''

'''economical (in euro per kW)'''
we_cost_kW = 1500

'''environmental (in kgCO2eq per kW)'''
'''we_cost_kW = 38.02'''

'''environmental for 2030 (in kgCO2eq per kW)'''
'''we_cost_kW = 21.26'''

we_SB_to_nominal_power = 0.02
we_off_to_nominal_power = 0.005
we_TUP = 0.5
we_MPL = 0.1
we_on_init = 0
we_SB_init = 0
we_off_init = 1
we_efficiency = 52

'''data related to fuel cell'''

'''economical (in euro per kW)'''
fc_cost_kW = 1800

'''environmental (in kgCO2eq per kW)'''
'''fc_cost_kW = 95.37'''

'''environmental for 2030 (in kgCO2eq per kW)'''
'''fc_cost_kW = 52.85'''

fc_SB_to_nominal_power = 0.02
fc_off_to_nominal_power = 0.005
fc_TUP = 0.25
fc_MPL = 0.1
fc_on_init = 0
fc_SB_init = 0
fc_off_init = 1
fc_efficiency = 20

'''data related to hydrogen tank'''

'''economical (in euro per kg)'''
ht_cost_kg = 450

'''environmental (in kgCO2eq per kg)'''
ht_cost_kg = 1118.32

'''environmental for 2030 (in kgCO2eq per kg)'''
ht_cost_kg = 671.9

ht_min_state_of_energy = 0.2
ht_max_state_of_energy = 0.95
ht_initial_state_of_energy = 0.3
