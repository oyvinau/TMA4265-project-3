library("ggplot2")

sigma = 4
phi = 0.2

data = c(50.1, 39.1, 54.7, 42.1, 40.9)
points = c(19.4, 29.7, 36.1, 50.7, 71.9)
# for task 3
data = c(data, 49.7)
points = c(points, 40.7)
# new data point
# try at t = 10, because only here our model has the target quality contained in the 
# 90% prediction interval (i. e. testing other points would most likeley be a waste 
# according to our model)

t = (0:140) * 0.5 + 10
t = c(t, points)

# calculate the expected values and the variances of x(t) given the data
size = length(t)
H = abs( matrix(1, size, 1) %*% t - t %*% matrix(1, 1, size) )
S = sigma * sigma * (1 + phi * H) * exp( -phi * H )

my_a = matrix(50, 141, 1)
my_b = matrix(50, size - 141, 1)
S_a = S[1:141,1:141]
S_ab = S[1:141,142:size]
S_ba = S[142:size,1:141]
S_b = S[142:size,142:size]

my = my_a + S_ab %*% solve(S_b, data - my_b)
var = S_a - S_ab %*% solve(S_b) %*% S_ba
var = diag(var)

main = function() {
  
  #task 1
  t = t[1:141]
  # lower and upper values for 90% prediction interval
  x_lower = my - sqrt(var) * 1.645
  x_upper = my + sqrt(var) * 1.645
  df1 = data.frame(t, my)
  df2 = data.frame(t, x_lower)
  df3 = data.frame(t, x_upper)
  p = ggplot() + geom_line(data = df1, aes(t, my), color = "black", size = 1) +
    geom_line(data = df2, aes(t, x_lower), color = "blue", size = 0.5) +
    geom_line(data = df3, aes(t, x_upper), color = "blue", size = 0.5)
  print(p + labs(title = expression("title," ~ phi[E] ~ "=" ~ 3 / 10), x = "x", y = "y"))
  
  # task 2, 3
  # the probabilities that x(t) > 57,
  # are gaussian distributed with mean 'my' and variance 'var'
  z = (57 - my) / sqrt(var)
  p_quality = 1 - pnorm(z)
  df4 = data.frame(t, p_quality)
  q = ggplot() + geom_line(data = df4, aes(t, p_quality), color = "black", size = 1)
  #print(q + labs(title = "title", x = "x", y = "y"))
  
}

main()