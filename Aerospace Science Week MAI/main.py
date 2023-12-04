import matplotlib.pyplot as plt
import random


###########################
#### Начальные условия ####
###########################
# Номинальные массы окислителя и горючего
Mo_nom = 24814
Mg_nom = 9926
# Ошибка по массе для окислителя
wrong = random.uniform(-Mo_nom*0.005, -Mo_nom*0.005)
# Задаем массивы для всех значений масс на всем времени полета. Нулевыми элементы задаем начальные значения
# массы окислителя и горючего. Задаем суммарную массу в начальный момент времени [кг]
Mo = [Mo_nom + wrong]
Mg = [Mg_nom]
M_0 = Mo[0] + Mg[0]

# Номинальное значение кф соотношения расходов. Задаем ограничение по кф соотношения 10%
Km_nom = Mo_nom/Mg_nom
alpha = 0.1
Km_min = Km_nom - Km_nom * alpha
Km_max = Km_nom + Km_nom * alpha
# Ошибка по кф соотношения расходов
wrong = random.uniform(-Km_nom*0.02, -Km_nom*0.02)
# Задаем массив для всех значений кф соотношения расходов на всем времени полета. Нулевым элементом задаем начальное
# значение кф соотношения расходов
Km = [Km_nom + wrong]

# Задаем суммарный расход (const на всем времени). Задаем массивы для всех значений секундного расхода окислителя и
# горючего на всем времени полета. Нулевыми элементы задаем начальные значения расходов [кг/сек]
R = 83.5655
Ro = [R * (Km_nom/(1 + Km_nom))]
Rg = [R * (1/(Km_nom + 1))]
Ro_nom = R * (Km_nom/(1 + Km_nom))  #
Rg_nom = R * (1/(Km_nom + 1))  #

# Начальный момент времени 0. Задаем конечный момент времени [с]
t = [0]
tk = M_0 / R


def start():
    global t, tk,  Mo, Mg, Ro, Rg, R, Km

    t_predict = []               # Моменты времени, когда делается прогноз
    Mo_predict = []              # Прогнозы остатков окислителя каждые 10 секунд
    Mg_predict = []              # Прогнозы остатков горючего каждые 10 секунд
    i = 0                        # Счетчик времени
    k = 0                        # Счетчик кол-ва предсказаний
    while i < int(tk):
        dKm = 0                  # Управляющее Km (Изменение Km)
        if i % 10 == 0 and i > 0:
            tau = i + 0.5 * (tk - i)  # Массив моментов времени на интервале времени, которые считаем конечными (для установления кф соотношения
            Mo_predict += [round(Mo[i] - Ro[i] * (tau - i) - Ro_nom * (tk - tau), 5)]
            Mg_predict += [round(Mg[i] - Rg[i] * (tau - i) - Rg_nom * (tk - tau), 5)]
            t_predict += [i]
            dKm = round((Mo_predict[k] / (Ro[i] * (tau - i)) - Mg_predict[k] / (Rg[i] * (tk - i))), 5) # Вот тут надо формулу поменять
            k += 1

        Mo += [Mo[i] - Ro[i]]
        Mg += [Mg[i] - Rg[i]]

        Km += [Km[i] + dKm]
        Ro += [R * (Km[i + 1] / (Km[i + 1] + 1))]
        Rg += [R * (1 / (Km[i + 1] + 1))]

        i += 1
        t += [i]

    Mo += [Mo[i] - Ro[i] * (tk - int(tk))]
    Mg += [Mg[i] - Rg[i] * (tk - int(tk))]

    Km += [Km[i] + dKm]

    i += tk - int(tk)
    t += [i]
    t_predict += [i]
    Mo_predict += [0.0]
    Mg_predict += [0.0]


    # Прогноз остатков массы окислителя (каждые 10 секунд)
    # plt.plot(t_predict, Mo_predict, label='Прогноз Zo')
    # plt.plot(t_predict, [0] * len(Mo_predict))
    # plt.xlabel('Время [с]')
    # plt.ylabel('Масса [кг]')
    # plt.title('Прогноз остатков массы окислителя')
    # plt.show()
    # # Прогноз остатков массы горючего (каждые 10 секунд)
    # plt.plot(t_predict, Mg_predict, label='Прогноз Zg')
    # plt.plot(t_predict, [0] * len(Mg_predict))
    # plt.xlabel('Время [с]')
    # plt.ylabel('Масса [кг]')
    # plt.title('Прогноз остатков массы горючего')
    # plt.show()

    # Кф соотношения расходов
    print('Кф соотношения расходов')
    print('Начало: ' + str(Km[0]), 'Конец: ' + str(Km[-1]))
    plt.plot(t, Km, label='Km')
    plt.plot(t, [Km_nom] * len(Km), label='Номинальный Km')
    plt.xlabel('Время [с]')
    plt.ylabel('Km')
    plt.title('Изменение Km')
    plt.legend()
    plt.show()

    # Расход окислителя
    # print('Расход окислителя')
    # print('Начало: ' + str(Ro[0]) + ' кг/с', 'Конец: ' + str(Ro[-1]) + ' кг/с')
    # plt.plot(t[:-1], Ro)
    # plt.plot(t[:-1], [Ro_nom] * len(Ro), label='Номинальный Km')
    # plt.xlabel('Время [с]')
    # plt.ylabel('Расход [кг/с]')
    # plt.title('Изменение расхода окислителя')
    # plt.show()
    # # Расход горючего
    # print('Расход горючего')
    # print('Начало: ' + str(Rg[0]) + ' кг/с', 'Конец: ' + str(Rg[-1]) + ' кг/с')
    # plt.plot(t[:-1], Rg)
    # plt.xlabel('Время [с]')
    # plt.ylabel('Расход [кг/с]')
    # plt.title('Изменение расхода горючего')
    # plt.show()


start()
