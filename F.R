library("ggplot2")

TIMES = 100
size = TIMES + 3
sigma = 1
phi = 3 / 10

data = c(0.58, -1.34, 0.61)
points = c(11.2, 51.8, 81.4)

t = 1:TIMES
t = c(t, points)

H = abs( matrix(1, size, 1) %*% t - t %*% matrix(1, 1, size) )
S = sigma * sigma * exp( -phi * H )

Lt = chol(S)
L = t(Lt)

# the new expectation and variance based on the data
S_a = S[1:(size - 3), 1:(size - 3)]
S_ab = S[1:(size - 3),(size - 2):size]
S_ba = S[(size - 2):size, 1:(size - 3)]
S_b = S[(size - 2):size,(size - 2):size]

my = S_ab %*% solve(S_b, data)
var = S_a - S_ab %*% solve(S_b) %*% S_ba


main = function() {
  
  # drawing 100 simulations
  
  z = rnorm(TIMES, 0, 1)
  x = my + var %*% z
  t = t[1:TIMES]
  df = data.frame(t, x)
  p = ggplot() + geom_point(data = df, aes(t, x), color = "blue")
  print(p + labs(title = "title", x = "x", y = "y"))
}

main()


