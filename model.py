import pyomo.environ as pe
import pyomo.opt as po
import pandas as pd
from parameters import *

'''import and conversion of datas from excel to list'''

elec_load = pd.read_excel("GEP_consumption_aggregated.xlsx")
radiation = pd.read_excel("50.88_4.29_radiation.xlsx")
wind_speed = pd.read_excel("50.88_4.29_wind_speed_100m.xlsx")

Load = elec_load['Consumer_0'].tolist()
sun = radiation['Radiation (W/mÂ²)'].tolist()
wind = wind_speed['Wind speed (m/s)'].tolist()

'''Load = Load[3000:4000]
sun = sun[3000:4000]
wind = wind[3000:4000]'''

'''conversion of data about radiation in power'''

sun_power_kW = [rad*pv_efficiency*pv_area*pv_number/1000 for rad in sun]

'''conversion of data about wind speed in power (the adjustemet are made to better match the power profile of a Enercon E-82 E4 3.000'''

wind_power_kW = [(wt_number*(wt_rated_power*(wind_speed-wt_min_speed))/(wt_rated_speed-wt_min_speed)) for wind_speed in wind]
for y in range(0, len(wind_power_kW)):
    if wind_power_kW[y] < 0:
        wind_power_kW[y] = 0
for z in range(0, len(wind_power_kW)):
    if wind_power_kW[z] > wt_rated_power:
        wind_power_kW[z] = wt_rated_power

'''creating a list with load, production and the difference between the two'''

production = [s + w for s, w in zip(sun_power_kW, wind_power_kW)]
difference = [l - p for l, p in zip(Load, production)]

'''define lenght of the list'''

ti = 0
tf = len(Load) - 1

'''creation of model'''

model = pe.ConcreteModel()

model.time = pe.RangeSet(ti, tf)

'''variable related to batterie'''

model.state_of_energy_bat = pe.Var(model.time, domain=pe.NonNegativeReals)
model.bat_charge = pe.Var(model.time, domain=pe.NonNegativeReals)
model.bat_charge_state = pe.Var(model.time, domain=pe.Binary)
model.bat_discharge = pe.Var(model.time, domain=pe.NonNegativeReals)
model.bat_discharge_state = pe.Var(model.time, domain=pe.Binary)
model.bat_size = pe.Var(domain=pe.NonNegativeIntegers, initialize=300)
model.bat_cost = pe.Var(domain=pe.NonNegativeReals)
model.bat_replacement_cost = pe.Var(model.time, domain=pe.NonNegativeReals)
model.bat_total_replacement_cost = pe.Var(domain=pe.NonNegativeReals)
model.bat_total_cost = pe.Var(domain=pe.NonNegativeReals)

state_of_energy_initial_bat = bat_initial_state_of_energy * model.bat_size
kW_charged_and_discharged_in_battery_before_replacement = bat_number_of_cycle_in_life_time * 2 * (bat_max_state_of_energy - bat_min_state_of_energy)


'''variable related to fuel cell'''

model.fc_power = pe.Var(model.time, domain=pe.NonNegativeReals)
model.fc_cons = pe.Var(model.time, domain=pe.NonNegativeReals)
model.fc_on = pe.Var(model.time, domain=pe.Binary)
model.fc_SB = pe.Var(model.time, domain=pe.Binary)
model.fc_off = pe.Var(model.time, domain=pe.Binary)
model.fc_size = pe.Var(domain=pe.NonNegativeIntegers, initialize=150)
model.fc_SB_power = pe.Var(domain=pe.NonNegativeReals)
model.fc_off_power = pe.Var(domain=pe.NonNegativeReals)
model.fc_cost = pe.Var(domain=pe.NonNegativeReals)

'''variable related to water electrolyser'''

model.we_power = pe.Var(model.time, domain=pe.NonNegativeReals)
model.we_cons = pe.Var(model.time, domain=pe.NonNegativeReals)
model.we_on = pe.Var(model.time, domain=pe.Binary)
model.we_SB = pe.Var(model.time, domain=pe.Binary)
model.we_off = pe.Var(model.time, domain=pe.Binary)
model.we_size = pe.Var(domain=pe.NonNegativeIntegers, initialize=150)
model.we_SB_power = pe.Var(domain=pe.NonNegativeReals)
model.we_off_power = pe.Var(domain=pe.NonNegativeReals)
model.we_cost = pe.Var(domain=pe.NonNegativeReals)

'''variable related to hydrogen tank'''

model.state_of_energy_ht = pe.Var(model.time, domain=pe.Reals)
model.ht_size = pe.Var(domain=pe.NonNegativeIntegers, initialize=80)
model.ht_cost = pe.Var(domain=pe.NonNegativeReals)

state_of_energy_initial_ht = ht_initial_state_of_energy * model.ht_size

'''other variable in the model'''

model.curtailment = pe.Var(model.time, domain=pe.NonNegativeReals)
model.cost = pe.Var(domain=pe.NonNegativeReals)

obj_expr = model.cost
model.obj = pe.Objective(expr=obj_expr, sense=pe.minimize)

'''energie'''

def energy_balance(model, t):
    if t == ti:
       return Load[t] == production[t] - (model.bat_charge_state[t] * model.bat_charge[t]) + (model.bat_discharge_state[t] * model.bat_discharge[t]) - model.we_cons[t] - model.fc_cons[t] + model.fc_power[t]*(1 - fc_TUP * fc_off_initial) - model.curtailment[t]
    else:
       return Load[t] == production[t] - (model.bat_charge_state[t] * model.bat_charge[t]) + (model.bat_discharge_state[t] * model.bat_discharge[t]) - model.we_cons[t] - model.fc_cons[t] + model.fc_power[t]*(1 - fc_TUP * model.fc_off[t-1]) - model.curtailment[t]
model.energy_balance = pe.Constraint(model.time, rule=energy_balance)

'''constrain linked to batterie'''

'''no charge and discharge in same time'''

def charge_discharge(model, t):
    return model.bat_charge_state[t] + model.bat_discharge_state[t] <= 1
model.charge_discharge = pe.Constraint(model.time, rule=charge_discharge)

'''limit energy in batterie'''

def minimum_state_of_energy_batterie(model, t):
    return model.state_of_energy_bat[t] >= bat_min_state_of_energy * model.bat_size
model.minimum_state_of_energy_batterie = pe.Constraint(model.time, rule=minimum_state_of_energy_batterie)

def maximum_state_of_energy_batterie(model, t):
    return model.state_of_energy_bat[t] <= bat_max_state_of_energy * model.bat_size
model.maximum_state_of_energy_batterie = pe.Constraint(model.time, rule=maximum_state_of_energy_batterie)

'''define the state of energy in batterie'''

def state_of_energy_batterie(model, t):
    if t == ti:
        return model.state_of_energy_bat[t] == state_of_energy_initial_bat + (model.bat_charge_state[t]*model.bat_charge[t]*bat_charge_efficiency) - (model.bat_discharge_state[t]*model.bat_discharge[t]/bat_discharge_efficiency)
    else:
        return model.state_of_energy_bat[t] == model.state_of_energy_bat[t-1] + (model.bat_charge_state[t]*model.bat_charge[t]*bat_charge_efficiency) - (model.bat_discharge_state[t]*model.bat_discharge[t]/bat_discharge_efficiency)
model.state_of_energy_batterie = pe.Constraint(model.time, rule=state_of_energy_batterie)

'''limite charge and discharge of the batterie'''

def min_bat_charge(model, t):
    return 0 <= model.bat_charge[t]
model.min_bat_charge = pe.Constraint(model.time, rule=min_bat_charge)

def max_bat_charge(model, t):
    return model.bat_charge[t] <= bat_max_charge * model.bat_size * model.bat_charge_state[t]
model.max_bat_charge = pe.Constraint(model.time, rule=max_bat_charge)

def min_bat_discharge(model, t):
    return 0 <= model.bat_discharge[t]
model.min_bat_discharge = pe.Constraint(model.time, rule=min_bat_discharge)

def max_bat_discharge(model, t):
    return model.bat_discharge[t] <= bat_max_discharge * model.bat_size * model.bat_discharge_state[t]
model.max_bat_discharge = pe.Constraint(model.time, rule=max_bat_discharge)

'''cost of the batterie'''

def battery_cost(model):
    return model.bat_cost == bat_cost_kWh * model.bat_size
model.battery_cost = pe.Constraint(rule=battery_cost)

'''taking into account that the battery will have to be replaced after a certain number of charge and ddischarge cycle'''

def battery_replacement_cost(model, t):
    return model.bat_replacement_cost[t] == (bat_cost_kWh / kW_charged_and_discharged_in_battery_before_replacement) * (model.bat_charge[t] + model.bat_charge[t])
model.battery_replacement_cost = pe.Constraint(model.time, rule=battery_replacement_cost)

def battery_total_replacement_cost(model):
    bat_final_replacement_cost = 0
    for t in range(ti, tf + 1):
       bat_final_replacement_cost = bat_final_replacement_cost + model.bat_replacement_cost[t]
    return model.bat_total_replacement_cost == bat_final_replacement_cost
model.battery_total_replacement_cost = pe.Constraint(rule=battery_total_replacement_cost)

''' final cost of the batterie'''

def battery_total_cost(model):
    return model.bat_total_cost == model.bat_cost + model.bat_total_replacement_cost
model.battery_total_cost = pe.Constraint(rule=battery_total_cost)

'''constraint linked to the fuel cell'''

'''power in stand-by'''

def fc_power_SB(model):
    return model.fc_SB_power == fc_SB_to_nominal_power * model.fc_size
model.fc_power_SB = pe.Constraint(rule=fc_power_SB)

'''power in off'''

def fc_power_off(model):
    return model.fc_off_power == fc_off_to_nominal_power * model.fc_size
model.fc_power_off = pe.Constraint(rule=fc_power_off)

'''power limitation for fuel cell'''

def fc_minimum_power(model, t):
    return model.fc_power[t] >= model.fc_size * fc_MPL * model.fc_on[t]
model.fc_minimum_power = pe.Constraint(model.time, rule=fc_minimum_power)

def fc_maximum_power(model, t):
    return model.fc_power[t] <= model.fc_size * model.fc_on[t]
model.fc_maximum_power = pe.Constraint(model.time, rule=fc_maximum_power)

'''fuel cell consumption'''

def fc_consumption(model, t):
    return model.fc_cons[t] == model.fc_SB_power*model.fc_SB[t] + model.fc_off[t]*model.fc_off_power
model.fc_consumption = pe.Constraint(model.time, rule=fc_consumption)

'''fuel cell can be on, off, or in stand-by but only one at time'''

def fc_state(model, t):
    return model.fc_on[t]+model.fc_SB[t]+model.fc_off[t] == 1
model.fc_state = pe.Constraint(model.time, rule=fc_state)

'''avoid passing directly from off to stand-by'''

def fc_off_to_SB(model, t):
    if t == ti:
        return model.fc_SB[t] + fc_off_initial <= 1
    else:
        return model.fc_SB[t] + model.fc_off[t-1] <= 1
model.fc_off_to_SB = pe.Constraint(model.time, rule=fc_off_to_SB)

'''avoid passing directly from stand-by to off'''

def fc_SB_to_off(model, t):
    if t == ti:
        return model.fc_off[t] + fc_SB_initial <= 1
    else:
        return model.fc_off[t] + model.fc_SB[t-1] <= 1
model.fc_SB_to_off = pe.Constraint(model.time, rule=fc_SB_to_off)

'''cost of fuel cell'''

def fc_final_cost(model):
    return model.fc_cost == fc_cost_kW * model.fc_size
model.fc_final_cost = pe.Constraint(rule=fc_final_cost)

'''constraint linked to water electrolyser'''

'''power in stand-by'''

def we_power_SB(model):
    return model.we_SB_power == we_SB_to_nominal_power * model.we_size
model.we_power_SB = pe.Constraint(rule=we_power_SB)

'''power in off'''

def we_power_off(model):
    return model.we_off_power == we_off_to_nominal_power * model.we_size
model.we_power_off = pe.Constraint(rule=we_power_off)

'''power limitation for water electrolyzer'''

def we_minimum_power(model, t):
    return model.we_power[t] >= model.we_size * we_MPL * model.we_on[t]
model.we_minimum_power = pe.Constraint(model.time, rule=we_minimum_power)

def we_maximum_power(model, t):
    return model.we_power[t] <= model.we_size * model.we_on[t]
model.we_maximum_power = pe.Constraint(model.time, rule=we_maximum_power)

'''power consumed by the electrolizer'''

def we_consumption(model, t):
    return model.we_cons[t] == (model.we_power[t]*model.we_on[t]) + (model.we_SB_power*model.we_SB[t]) + (model.we_off[t]*model.we_off_power)
model.we_consumption = pe.Constraint(model.time, rule=we_consumption)

'''elecrolizer can be on, off, or in stand-by but only one at time'''

def we_state(model, t):
    return model.we_on[t]+model.we_SB[t]+model.we_off[t] == 1
model.we_state = pe.Constraint(model.time, rule=we_state)

'''avoid passing directly from off to stand-by'''

def we_off_to_SB(model, t):
    if t == ti:
        return model.we_SB[t] + we_off_initial <= 1
    else:
        return model.we_SB[t] + model.we_off[t-1] <= 1
model.we_off_to_SB = pe.Constraint(model.time, rule=we_off_to_SB)

'''avoid passing directly from stand-by to off'''

def we_SB_to_off(model, t):
    if t == ti:
        return model.we_off[t] + we_SB_initial <= 1
    else:
        return model.we_off[t] + model.we_SB[t-1] <= 1
model.we_SB_to_off = pe.Constraint(model.time, rule=we_SB_to_off)

'''cost of elecrolyzer'''

def we_final_cost(model):
    return model.we_cost == we_cost_kW * model.we_size
model.we_final_cost = pe.Constraint(rule=we_final_cost)


'''hydrogen tank'''

'''define the state of energy in hydrogen tank'''
'''here even if its called energy the value is calculed in kg'''

def state_of_energy_hydrogen_tank(model, t):
    if t == ti:
        return model.state_of_energy_ht[t] == state_of_energy_initial_ht + (model.we_power[t]*(1 - we_TUP * we_off_initial)/we_efficiency) - (model.fc_power[t]/fc_efficiency)
    else:
        return model.state_of_energy_ht[t] == model.state_of_energy_ht[t-1] + (model.we_power[t]*(1 - we_TUP * model.we_off[t-1])/we_efficiency) - (model.fc_power[t]/fc_efficiency)
model.state_of_energy_hydrogen_tank = pe.Constraint(model.time, rule=state_of_energy_hydrogen_tank)

'''limit the hydrogen inside hydrogene tank'''


def minimum_state_of_energy_hydrogen_tank(model, t):
    return ht_min_state_of_energy * model.ht_size <= model.state_of_energy_ht[t]
model.minimum_state_of_energy_hydrogen_tank = pe.Constraint(model.time, rule=minimum_state_of_energy_hydrogen_tank)


def maximum_state_of_energy_hydrogen_tank(model, t):
    return model.state_of_energy_ht[t] <= ht_max_state_of_energy * model.ht_size
model.maximum_state_of_energy_hydrogen_tank = pe.Constraint(model.time, rule=maximum_state_of_energy_hydrogen_tank)

'''cost of hydrogen tank'''

def ht_final_cost(model):
    return model.ht_cost == ht_cost_kg * model.ht_size
model.ht_final_cost = pe.Constraint(rule=ht_final_cost)

'''objective'''

def final_cost(model):
    return model.cost == model.bat_cost + model.ht_cost + model.fc_cost + model.we_cost
model.final_cost = pe.Constraint(rule=final_cost)

'''solving'''

solver = po.SolverFactory('gurobi')
solver.options['NonConvex'] = 2
solver.options['Method'] = 0
solver.options['MIPFocus'] = 3
solver.options['Presolve'] = 2
solver.options['MIPGap'] = 0.05
status = solver.solve(model)

'''data export'''

state_of_energy_bat_data = []
for t in range(ti, tf+1):
    state_of_energy_bat_data.append(pe.value(model.state_of_energy_bat[t]))

bat_charge_data = []
for t in range(ti, tf+1):
    bat_charge_data.append(pe.value(model.bat_charge[t]))

bat_discharge_data = []
for t in range(ti, tf+1):
    bat_discharge_data.append(pe.value(model.bat_discharge[t]))

bat_charge_state_data = []
for t in range(ti, tf+1):
    bat_charge_state_data.append(pe.value(model.bat_charge_state[t]))

bat_discharge_state_data = []
for t in range(ti, tf+1):
    bat_discharge_state_data.append(pe.value(model.bat_discharge_state[t]))

we_cons_data = []
for t in range(ti, tf+1):
    we_cons_data.append(pe.value(model.we_cons[t]))

we_power_data = []
for t in range(ti, tf+1):
    we_power_data.append(pe.value(model.we_power[t]))

we_on_data = []
for t in range(ti, tf+1):
    we_on_data.append(pe.value(model.we_on[t]))

we_off_data = []
for t in range(ti, tf+1):
    we_off_data.append(pe.value(model.we_off[t]))

we_SB_data = []
for t in range(ti, tf + 1):
    we_SB_data.append(pe.value(model.we_SB[t]))

fc_cons_data = []
for t in range(ti, tf+1):
    fc_cons_data.append(pe.value(model.fc_cons[t]))

fc_power_data = []
for t in range(ti, tf+1):
    fc_power_data.append(pe.value(model.fc_power[t]))

fc_on_data = []
for t in range(ti, tf+1):
    fc_on_data.append(pe.value(model.fc_on[t]))

fc_off_data = []
for t in range(ti, tf+1):
    fc_off_data.append(pe.value(model.fc_off[t]))

fc_SB_data = []
for t in range(ti, tf + 1):
    fc_SB_data.append(pe.value(model.fc_SB[t]))

curtailments_data = []
for t in range(ti, tf+1):
    curtailments_data.append(pe.value(model.curtailment[t]))

state_of_energy_ht_data = []
for t in range(ti, tf+1):
    state_of_energy_ht_data.append(pe.value(model.state_of_energy_ht[t]))

df = pd.DataFrame(list(zip(Load, sun, wind, sun_power_kW, wind_power_kW, production, difference, state_of_energy_bat_data, bat_charge_data, bat_discharge_data, bat_charge_state_data, bat_discharge_state_data, we_cons_data, we_power_data, we_on_data, we_off_data, we_SB_data, fc_cons_data, fc_power_data, fc_on_data, fc_off_data, fc_SB_data, curtailments_data, state_of_energy_ht_data)), columns=['Load (kW)', 'Radiation (Wh/m2)', 'Wind speed (m/s)', 'PV Power (kW)', 'WT Power (kW)', 'energy production (W)', 'diff (W)', 'energy in bat (W)', 'battery charging (W)', 'battery discharging (W)', 'battery charge state', 'battery discharge state', 'we consumption (W)', 'we production (W)', 'we on', 'we off', 'we SB', 'fc consumption (W)', 'fc production (W)',  'fc on', 'fc off', 'fc SB', 'curtailments (W)', 'hydrogene in ht (kg)'])
df.to_excel('Results.xlsx', sheet_name='Results')

'''printing some value'''

print(pe.value(model.bat_size))
print(pe.value(model.ht_size))
print(pe.value(model.fc_size))
print(pe.value(model.we_size))
print("solved")
print(pe.value(model.cost))
