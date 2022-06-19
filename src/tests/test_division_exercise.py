# num = 626169369296  # 23455
num = 156542342324  # 75438
den = 656179362217  # 23455
data_id_numerator = "num"
data_id_denominator = "den"
data_id_result = "my_result"

self.data[data_id_numerator] = num
self.data[data_id_denominator] = den

self.add_exercise_manager_inser_in_share(data_id_numerator)
self.add_exercise_manager_inser_in_share(data_id_denominator)

self.add_exercise_division(data_id_numerator, data_id_denominator, data_id_result)
self.add_exercise_reveal_number(data_id_result)
