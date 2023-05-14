import math

time_step = 1 #hours
time_period = 8760 #hours
start_time = 0 #time_step
time_days = 365
end_time = time_days*24

pv_eff = 0.205
pv_area = 2.00743
pv_units = 205

wt_efficiency = 0.57
wt_rho_air = 1.2
wt_blade_lenght = 1
wt_surface = math.pi*(wt_blade_lenght**2)
wt_number = 3

wt_vcin = 3
wt_vcout = 34
wt_vrated = 12
wt_prated = 20

bat_capex = 800
bat_C_charge = 0.3
bat_C_discharge = 0.3
bat_charge_eff = 0.92
bat_discharge_eff = 0.95
bat_SOE_i = 0.2
bat_SOE_min = 0.2
bat_SOE_max = 1

ely_capex = 1500
ely_consumption_idle = 0.025
ely_consumption_SB = 0.05
ely_eff = 52
ely_STT = 0.5
ely_MPL = 0.1
ely_a_i = 0
ely_b_i = 0
ely_c_i = 1

fc_capex = 1800
fc_consumption_idle = 0.025
fc_consumption_SB = 0.05
fc_eff = 20.940
fc_STT = 0.25
fc_MPL = 0.1
fc_a_i = 0
fc_b_i = 0
fc_c_i = 1

hs_capex = 400
hs_capacity = 30
hs_SOE_i = 0.1
hs_SOE_min = 0.1
hs_SOE_max = 1