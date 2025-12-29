G = 9.81 # m/s²

canvas_width = 800  # exemple, comme en JS
length = 0.2 * canvas_width  # longueur des bras
radius = 0.015 * canvas_width  # taille visuelle des masses
mass = 1

prefactor_t = 6 / (mass * length * length)
prefactor_p = mass * length * length / 2
constant = 9.81 / length
