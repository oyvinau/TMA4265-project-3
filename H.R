library("ggplot2")

days = 60
sigma = 0.75
x_0 = 45

t = 0:days
simulate = function(times) {
  p = ggplot()
  above_50 = 0
  for (i in 1:times) {
    x = t * 0
    x[1] = x_0
    for (j in 2:(days + 1)) {
      x[j] = rnorm(1, x[j - 1], sigma)
    }
    if (x[days] > 50) {
      above_50 = above_50 + 1
    }
    df = data.frame(t, x)
    p = p + geom_line(data = df, aes(t, x), size = 1)
  }
  print("By running 100 simulations: ")
  print(p)
  print(above_50 / times)
}

simulate_wait = function(times) {
  timecap = 10000
  hitting_times = matrix(0, 10, 1)
  for (i in 1:times) {
    x = 40
    t = 0
    while (TRUE) {
      x = x + sigma * rnorm(1)
      t = t + 1
      if (x >= 44 || t >= timecap) {
        break
      }
    }
    if (t < timecap) {
      t_ = round(t / 1000)
      hitting_times[t_] = hitting_times[t_] + 1
    }
  }
  print("It took on average: ")
  print(sum(hitting_times) / times)
  print("days to increase by 10%")
  
  t = 1:10 * 1000
  hitting_times = hitting_times / times
  df = data.frame(t, hitting_times)
  p = ggplot() + geom_line(data = df, aes(t, hitting_times))
  print(p)
  
}

main = function() {
  # task 1
  # set x_0 = 40 and days = 120
  
  # task 2
  # by the markovian property we have p(x_2 | (x_1 and x_0) ) = p(x_2 | x_1)
  # set x_0 = 45 and days = 60
  
  #simulate(100)
  #print("The analytical probabiltity is: ")
  #z = (50 - x_0) / (sigma * sqrt(days))
  #print(1 - pnorm(z))
  
  # task 3
  simulate_wait(1000)
  # the analytical distribution is given by d/dt [ 2 * (1 - phi(4 / (sqrt(t) * sigma)) ]
  
}
main()




