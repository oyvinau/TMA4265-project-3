library("ggplot2")
colors = c("#89C5DA", "#DA5724", "#74D944", "#CE50CA", "#3F4921", "#C0717C", "#CBD588", "#5F7FC7", 
           "#673770", "#D3D93E")
sigma = 1
phi = 3 / 10

data = c(0.58, -1.34, 0.61)
points = c(11.2, 51.8, 81.4)

t = 1:100
# for task 2
t = c(t, points)

size = length(t)
H = abs( matrix(1, size, 1) %*% t - t %*% matrix(1, 1, size) )
S = sigma * sigma * exp( -phi * H )

# the new expectation and variance based on the data
S_a = S[1:(size - 3), 1:(size - 3)]
S_ab = S[1:(size - 3),(size - 2):size]
S_ba = S[(size - 2):size, 1:(size - 3)]
S_b = S[(size - 2):size,(size - 2):size]

my = S_ab %*% solve(S_b, data)
var = S_a - S_ab %*% solve(S_b) %*% S_ba

simulate_independent = function() {
  p = ggplot()
  Lt = chol(S)
  L = t(Lt)
  for (i in 1:10) {
    z = rnorm(100)
    x = L %*% z
    df = data.frame(t, x)
    p = p + geom_line(data = df, aes(t, x), color = colors[i], size = 1)
  }
  p = p + theme(text = element_text(size = 20))
  p = p + labs(title = expression("10 realizations of x(t), with exponential correlation,"~phi[E]~"="~1 / 10), x = "t", y = "x", size = 10)
  print(p)
}
simulate_dependent = function() {
  p = ggplot()
  t = t[1:100]
  Lt = chol(var)
  L = t(Lt)
  for (i in 1:10) {
    z = rnorm(100)
    x = my + L %*% z
    df = data.frame(t, x)
    p = p + geom_line(data = df, aes(t, x), color = colors[i], size = 1)
  }
  df = data.frame(points, data)
  p = p + geom_point(data = df, aes(points, data), size = 3, color = "black")
  p = p + theme(text = element_text(size = 20))
  p = p + labs(title = expression("10 realizations of x(t), given initial data,"~phi[E]~"="~3 / 10), x = "t", y = "x", size = 10)
  print(p)
}

main = function() {
  # task 1
  #simulate_independent()
  
  # task 2
  simulate_dependent()
}

main()


