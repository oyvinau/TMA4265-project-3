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
    
    #Simulate n_sim iterations
    for n in range(n_sim):
        #Initialize stock value to 40 and time to 0
        x = 40
        t = 0
        #While we haven't hit 10% increase nor reached truncation
        while (x < 44 and t < truncation_time):
            #Do gaussian motion
            x += stand_err*np.random.normal()
            #Increment time (1 day)
            t += 1
        if (t < truncation_time):
            #If we reached truncation time we throw the time away
            hitting_times.append(t)
        
    #Sort the hitting times
    hitting_times.sort()
    return hitting_times

#print(hitting_times(100, 1000))


def analytical_hitting_times(t):
    z = 4/(0.75*np.sqrt(t+1))
    p = stats.norm.cdf(z)
    return 2*(1-p)


def plot_hitting_times(n_sim):    
    H = hitting_times(n_sim, 10000)
    X = np.arange(0, H[-1]+2, 1)
    Y = np.zeros(len(X))
    for h in H:
        Y[h] += 1
    Y /= n_sim
    Y = np.cumsum(Y)
    
        
    Ya = [analytical_hitting_times(x) for x in X]
    
    plt.plot(X, Y)
    plt.plot(X, Ya)

    
plot_hitting_times(1000)
