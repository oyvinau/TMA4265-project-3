'''
Assume the price of a certain stock develops according to a Brownian motion
with 0 mean and noise standard error σ = 0.75 per day. On Jan 1st, the
price of the stock is $ 40. In this exercise the goal is to predict the future
stock price.
'''
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

plt.style.use('ggplot')

mean = 0
stand_err = 0.75
n=120

'''
1. What is the probability that the stock price is larger than $ 50 on May
1st (120 days ahead)? Find the solution by analytical calculations and
approximate the solution by generating and plotting 100 realizations
of the random process with a daily resolution until 1 May.
'''
def simulate_brownian(n_days, stand_err, x0):
	#time points 0-120
	time_points = np.arange(n_days+1)#121v120? 
	print (time_points)
	#initial value
	#1: Draw n independent standard normal variables (z1, . . . , zn).
	standard_normal_variables = [np.random.normal() for x in range(n_days) ]
	#2: return x(ti) = x(ti−1) + (ti − ti−1)σzi, i = 1, . . . , n.
	prices = [x0]
	for i in range(n_days):
		xi = prices[-1] + stand_err * standard_normal_variables[i]
		prices.append(xi)

	return(time_points, prices)

def plot_realizations(n_sim, n_days, x0):
	plt.figure()
	over_50 = 0
	for i in range(n_sim):
		realization = simulate_brownian(n_days, stand_err, x0)
		if realization[1][-1] > 50:
			over_50 += 1
		plt.plot(realization[0], realization[1])
	plt.title('100 realizations of the stocks price')
	plt.ylabel('Price in $')
	plt.xlabel('days')
	plt.show()
	print(over_50)
	print(over_50/100)

#plot_realizations(100, 120, 40)
print(5/(np.sqrt(60)*0.75))

'''
2. On March 2, the price of the stock is $ 45. What is now the probability
that the stock price is larger than $ 50 on May 1st (60 days ahead)?
Find again the solution by analytical calculations and approximate
the solution by generating and plotting 100 realizations of the random
process with a daily resolution until 1 May
'''
#plot_realizations(100, 60, 45)

'''
3. Assume that we know only the stock price of $ 40 on Jan 1st. There
is interest in the waiting time until the stock price has gone up 10
% (to $ 44). Find the distribution analytically and approximate this
distribution with sorted simulated hitting times over 100 realizations.
(You can truncate the simulations at some time (say t = 10000) to
avoid the tail in the hitting time distribution.)
'''
def hitting_times(n_sim, truncation_time):
	hitting_times = []
	#timesteps 1-1000
	time_steps = np.arange(truncation_time)
	for n in range(n_sim):
		for t in time_steps:
			#calculate prob of hit at time t
			prob = 1-stats.norm.pdf(4/(np.sqrt(t+1)*stand_err))
			#dice if hit or not with prob
			if np.random.uniform() > prob:
				hitting_times.append(t)
				#if hit end
				break
			
	hitting_times.sort()
	return hitting_times

def plot_hit(n_sim, truncation_time):
	hits = hitting_times(n_sim, truncation_time)
	plot_list = [0 for i in range(len(hits))]
	for hit in hits:
		plot_list[hit] += 1
	for i in range(len(plot_list)):
		plot_list[i] = plot_list[i] / len(plot_list)

	plot_list2 = []
	summ=0
	for i in plot_list:
		summ+=i
		plot_list2.append(summ)

	print(plot_list)
	print(hits[-1])
	analytical_list = [stats.norm.pdf(4/(np.sqrt(t+1)*stand_err)) for t in range(hits[-1])]
	analytical_list_points = [0 for i in range(len(analytical_list))]
	for i in range(len(analytical_list)):
		if i==0:
			analytical_list_points[i] = analytical_list[i]
		else:
			analytical_list_points[i] = analytical_list[i] - analytical_list[i-1]
	print(analytical_list)
	plt.figure()
	plt.plot(range(hits[-1]), analytical_list, 'bo')
	plt.bar(range(hits[-1]), plot_list[:hits[-1]])
	plt.show()

#plot_hit(100, 1000)

hits = hitting_times(10000, 1000)
hit_bar = [0 for _ in range(hits[-1]+1)]
for i in hits:
	hit_bar[i]+=1
print(hit_bar)
plt.figure()
plt.bar(range(hits[-1]+1), hit_bar)
plt.show()