import matplotlib.pyplot as plt
import random


###########################
#### Начальные условия ####
###########################
# Номинальные массы окислителя и горючего
Mo_nom = 24814
Mg_nom = 9926
# Ошибка по массе для окислителя
wrong = random.uniform(-Mo_nom*0.005, Mo_nom*0.005)
# Задаем массивы для всех значений масс на всем времени полета. Нулевыми элементы задаем начальные значения
# массы окислителя и горючего. Задаем суммарную массу в начальный момент времени [кг]
Mo = [Mo_nom + wrong]
Mg = [Mg_nom]
M_0 = Mo[0] + Mg[0]

# Номинальное значение кф соотношения расходов
Km_nom = Mo_nom/Mg_nom
# Ошибка по кф соотношения расходов
wrong = random.uniform(Km_nom*0.02, Km_nom*0.02)
# Задаем массив для всех значений кф соотношения расходов на всем времени полета. Нулевым элементом задаем начальное
# значение кф соотношения расходов
Km = [Km_nom + wrong]

# Задаем суммарный расход (const на всем времени). Задаем массивы для всех значений секундного расхода окислителя и
# горючего на всем времени полета. Нулевыми элементы задаем начальные значения расходов [кг/сек]
R = 83.5655
Ro = [R * (Km[0]/(1 + Km[0]))]
Rg = [R * (1/(Km[0] + 1))]

# Начальный момент времени 0. Задаем конечный момент времени [с]
t = [0]
tk = M_0 / R


def predict(i):
    global tk, t, Mo, Mg, Ro, Rg

    Mo_predict = round(Mo[i] - Ro[i] * (time_k - time[i]), 5)
    Mg_predict = round(Mg[i] - Rg[i] * (time_k - time[i]), 5)

    return Mo_predict, Mg_predict


def start():
    global tk, t,  Mo, Mg, Ro, Rg, R, Km

    time_arr_predict = []
    Mo_predict = []
    Mg_predict = []
    dMo = []
    dMg = []
    dKm_arr = []
    i = 0  # Счетчик времени
    k = 0
    while i < int(time_k):
        dKm = 0
        if i % 10 == 0:
            a = predict(i)
            Mo_predict += [a[0]]
            Mg_predict += [a[1]]
            time_arr_predict += [i]
            dKm = Mo_predict[k-1] / (Ro[i] * (time_k - k)) - Mg_predict[k - 1] / (Rg[i] * (time_k - k))
            dKm_arr += [dKm]
            k += 1

        Mo += [Mo[i] - Ro[i]]
        Mg += [Mg[i] - Rg[i]]

        dMo += [Mo[i] - (Mo[i] + Mg[i]) * (Km[i] / (Km[i] + 1))]
        dMg += [Mg[i] - (Mo[i] + Mg[i]) * (1 / (Km[i] + 1))]

        Km += [Km[i] + dKm]

        Ro += [R * (Km[i + 1] / (Km[i + 1] + 1))]
        Rg += [R * (1 / (Km[i + 1] + 1))]

        i += 1
        time += [i]

    Mo += [Mo[i] - Ro[i] * (time_k - int(time_k))]
    Mg += [Mg[i] - Rg[i] * (time_k - int(time_k))]

    dMo += [Mo[i] - (Mo[i] + Mg[i]) * (Km[i] / (Km[i] + 1))]
    dMg += [Mg[i] - (Mo[i] + Mg[i]) * (1 / (Km[i] + 1))]

    i += time_k - int(time_k)
    time += [i]
    time_arr_predict += [i]
    Mo_predict += [0.0]
    Mg_predict += [0.0]

    # Прогноз остатков массы окислителя каждые 10 секунд
    plt.plot(time_arr_predict, Mo_predict)
    plt.xlabel('Время [с]')
    plt.ylabel('Масса [кг]')
    plt.title('Прогноз массы окислителя')
    plt.show()
    # Прогноз остатков массы горючего
    plt.plot(time_arr_predict, Mg_predict)
    plt.xlabel('Время [с]')
    plt.ylabel('Масса [кг]')
    plt.title('Прогноз массы горючего')
    plt.show()

    # Прогноз остатков массы окислителя в каждый момент времени
    plt.plot(time[:-1], dMo)
    plt.xlabel('Время [с]')
    plt.ylabel('Масса [кг]')
    plt.title('Прогноз массы окислителя')
    plt.show()
    # Прогноз остатков массы горючего в каждый момент времени
    plt.plot(time[:-1], dMg)
    plt.xlabel('Время [с]')
    plt.ylabel('Масса [кг]')
    plt.title('Прогноз массы горючего')
    plt.show()

    # Масса окислителя
    print('Масса окислителя')
    print('Начало: ' + str(Mo[0]) + ' кг', 'Конец: ' + str(Mo[-1]) + ' кг', 'Ожидаемый остаток: ' + str(Mo_predict[-1]))
    plt.plot(time, Mo, label='Текущая масса')
    plt.plot(time_arr_predict, Mo_predict, label='Прогноз остатков')
    plt.xlabel('Время [с]')
    plt.ylabel('Масса [кг]')
    plt.title('Изменение массы окислителя')
    plt.legend()
    plt.show()
    # Масса горючего
    print('Масса горючего')
    print('Начало: ' + str(Mg[0]) + ' кг', 'Конец: ' + str(Mg[-1]) + ' кг', 'Ожидаемый остаток: ' + str(Mg_predict[-1]))
    plt.plot(time, Mg, label='Текущая масса')
    plt.plot(time_arr_predict, Mg_predict, label='Прогноз остатков')
    plt.xlabel('Время [с]')
    plt.ylabel('Масса [кг]')
    plt.title('Изменение массы горючего')
    plt.legend()
    plt.show()

    # Кф соотношения расходов
    print('Кф соотношения расходов')
    print('Начало: ' + str(Km[0]), 'Конец: ' + str(Km[-1]))
    plt.plot(time[:-1], Km, label='Текущий кф')
    plt.xlabel('Время [с]')
    plt.ylabel('кф соотношения расходов')
    plt.title('Изменение кф соотношения расходов')
    plt.legend()
    plt.show()

    # Расход окислителя
    print('Расход окислителя')
    print('Начало: ' + str(Ro[0]) + ' кг/с', 'Конец: ' + str(Ro[-1]) + ' кг/с')
    plt.plot(time[:-1], Ro)
    plt.xlabel('Время [с]')
    plt.ylabel('Расход [кг/с]')
    plt.title('Изменение расхода окислителя')
    plt.show()
    # Расход горючего
    print('Расход горючего')
    print('Начало: ' + str(Rg[0]) + ' кг/с', 'Конец: ' + str(Rg[-1]) + ' кг/с')
    plt.plot(time[:-1], Rg)
    plt.xlabel('Время [с]')
    plt.ylabel('Расход [кг/с]')
    plt.title('Изменение расхода горючего')
    plt.show()


start()
