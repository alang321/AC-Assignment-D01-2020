from math import sqrt, acos, pi, cos, e

# get wto from c

M_cruise = 0.77
S = 534.904 #m^2
M_cr = 0.8
qhat = 0.7 * 28737 * M_cr**2
W_TO = 2.97  * 10**6

C_Lhat = W_TO / (qhat * S)

sweepquarter = (180/pi) * acos(0.75 * 0.935/(0.03 + M_cruise)) # deg, sweep angle at quarter of cord from leading edge
taperratio = 0.2 * (2 - sweepquarter * pi/180)
AR = 17.7 * (2- taperratio) * e**(-0.043 * sweepquarter) # source: gudmundson (??)

b = sqrt(AR * S)
c = 2 * S / (b * (1 + taperratio))

sweephalf = 26 * pi/180 # deg, through drawing

toverc = ((cos(sweephalf))*3 * (0.935 - (M_cruise + 0.03) * cos(sweephalf)) - 0.115 * C_Lhat1.5)/((cos(sweephalf))*2)

print(sweepquarter, taperratio, b, c, toverc, AR)