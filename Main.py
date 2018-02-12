from Tools import *
from Scenario import *
from NSGA import *
from Evolution import *
import matplotlib.pyplot as plt


tool_box = Tools()
flow_data = tool_box.read_flow_data_from_txt()
loc_data = tool_box.read_loc_data_from_txt()
time_data = tool_box.read_slot_data_from_txt()
scenario = Scenario(flow_data, loc_data, time_data)
# scenario.generate_initial_solution()
print 'scenario generated'
problem = NSGA_problem(scenario)
evolve = Evolution(problem, 50, 100)
selected_individuals = evolve.evolve()
f = open('gene.txt', 'w')
for i in selected_individuals:
    s = ''
    for g in i.features:
        s = s+','+str(g)
    f.write(s+'\n')
f.close()
x = [problem.f1(i) for i in selected_individuals]
y = [problem.f2(i) for i in selected_individuals]
print x, y
plt.plot(x, y, 'ro')
plt.show()
