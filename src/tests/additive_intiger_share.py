a = 84148748585171335716677766872848
# 		 84148748585171335716677766872848
b = 100992853402524468941817214537763
# 		185141601987695804658494981410611
c = 7702193764531101523335850373289
# 		192843795752226906181830831783900
d = 140158104170659197267192914269086
# 		333001899922886103449023746052986
e = -17600913846915186130090700253545
# 		315400986075970917318933045799441
f = -71105368600340266644363436383268
# 		244295617475630650674569609416173
g = -120249473268136713205859832370582
# 		124046144207493937468709777045591
h = -84772507597356991229976740975640
# 		 39273636610136946238733036069951
i = 22937251769023113014656097263311
# 		 62210888379160059253389133333262
j = -5498495751308422654500507823434
# 		 56712392627851636598888625509828
k = 26777121642574605342771370024129
# 		  83489514270426241941659995533957
l = -101241490983181211736712472823503
# 		 -17751976712754969795052477289546
m = 105939648826364741308416500962063
##		  88187672113609771513364023672517
value = 4762638
sum = a + b + c + d + e + f + g + h + i + j + k + l + m
print(sum)
own_value = value - sum
print(own_value)

restored_value = own_value + sum
print(restored_value)
# own share value = -88187672113609771513364018909879 = 4762638 - 88187672113609771513364023672517

prim = 15285151248481
value_1 = 23859352468604561
value_2 = 122766707080827
value_3 = -5646845590679191
value_4 = 29168244437161418
value_5 = 24238160881147149
value_6 = -24713027120549590
value_7 = -3824105258277177
value_8 = 2217234732262210
value_9 = 1408181451797796
value_10 = -24547758110680338
value_11 = -4578424545693815
value_12 = -17998604826842792
value_13 = -10538082382095287

value_0 = 10832907161526867
print("==========")
sum = (
    value_1
    + value_2
    + value_3
    + value_4
    + value_5
    + value_6
    + value_7
    + value_8
    + value_9
    + value_10
    + value_11
    + value_12
    + value_13
)
print(sum)
print(sum + value_0)


value_1_m = value_1 % prim
value_2_m = value_2 % prim
value_3_m = value_3 % prim
value_4_m = value_4 % prim
value_5_m = value_5 % prim
value_6_m = value_6 % prim
value_7_m = value_7 % prim
value_8_m = value_8 % prim
value_9_m = value_9 % prim
value_10_m = value_10 % prim
value_11_m = value_11 % prim
value_12_m = value_12 % prim
value_13_m = value_13 % prim

value_0_m = value_0 % prim
print("==========")
sum_m = (
    value_1_m
    + value_2_m
    + value_3_m
    + value_4_m
    + value_5_m
    + value_6_m
    + value_7_m
    + value_8_m
    + value_9_m
    + value_10_m
    + value_11_m
    + value_12_m
    + value_13_m
)
print(sum_m)
print((sum_m + value_0_m) % prim)