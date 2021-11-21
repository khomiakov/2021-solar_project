# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
from matplotlib import pyplot as plt

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов
    Параметры:
    **input_filename** — имя входного файла
    """

    objects = []
    if input_filename != '':
        with open(input_filename) as input_file:
            for line in input_file:
                if len(line.strip()) == 0 or line[0] == '#':
                    continue  # пустые строки и строки-комментарии пропускаем
                object_type = line.split()[0].lower()
                if object_type == "star":
                    star = Star()
                    parse_star_parameters(line, star)
                    objects.append(star)
                elif object_type == "planet":
                    planet = Planet()
                    parse_planet_parameters(line, planet)
                    objects.append(planet)
                else:
                    print("Unknown space object")
    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4
    Параметры:
    **line** — строка с описание звезды.
    **star** — объект звезды.
    """

    tokens = line.split()
    star.R = int(tokens[1])
    star.color = tokens[2]
    star.m = float(tokens[3])
    star.x = float(tokens[4])
    star.y = float(tokens[5])
    star.Vx = float(tokens[6])
    star.Vy = float(tokens[7])


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4
    Параметры:
    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """

    tokens = line.split()
    planet.R = int(tokens[1])
    planet.color = tokens[2]
    planet.m = float(tokens[3])
    planet.x = float(tokens[4])
    planet.y = float(tokens[5])
    planet.Vx = float(tokens[6])
    planet.Vy = float(tokens[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Параметры:
    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    if output_filename != '':
        with open(output_filename + '.txt', 'w') as file:
            for obj in space_objects:
                string = str(obj.type) + ' ' + str(obj.R) + ' ' + str(obj.color) + ' ' + str(obj.m) + \
                ' ' + str(obj.x) + ' ' + str(obj.y) + ' ' + str(obj.Vx) + ' ' + str(obj.Vy) + '\n'
                file.write(string)

def clear_stats(space_objects):
    """
    Очищает файл stats.txt
    Сохраняет информацию о типах существующих тел в формате:
        Star  <радиус в пикселах> <цвет>
        <...>
        Planet <радиус в пикселах> <цвет>
        #End of the header
        
    Параметры:
        **space_objects** — список объектов планет и звёзд
        **physical_time** — время с начала симуляции
    """
    with open('stats.txt', 'w') as file:
            for obj in space_objects:
                string = str(obj.type) + ' ' + str(obj.R) + ' ' + str(obj.color) + '\n'
                file.write(string)
            file.write('#End of the header\n\n')

def save_space_objects_positions(space_objects, time):
    """
    Сохраняет данные о положении тел в файл stats.txt в формате
        <Физическое время с начала симуляции в секундах>
        <x> <y> <Vx> <Vy>
        <...>
        <x> <y> <Vx> <Vy>
        
    Параметры:
        **space_objects** — список объектов планет и звёзд
        **physical_time** — время с начала симуляции
    """
    with open('stats.txt', 'a') as file:
            file.write(str(time) + '\n')
            for obj in space_objects:
                string = str(obj.x) + ' ' + str(obj.y) + ' ' + str(obj.Vx) + ' ' + str(obj.Vy) + '\n'
                file.write(string)
            file.write('\n')

def get_data_for_plots():
    """
    Cчитывает данные о движении космических объектов из файла stats.txt
    Входной формат:
        Star  <радиус в пикселах> <цвет>
        <...>
        Planet <радиус в пикселах> <цвет>
        #End of the header
        <Физическое время с начала симуляции в секундах>
        <x> <y> <Vx> <Vy>
        <...>
        <x> <y> <Vx> <Vy>
        <...>
    Returns:
        **legend** — список объектов в формате:
            [<тип>,  <радиус в пикселах>, <цвет>]
        **t** — время с начала симуляции (список)
        **r** — расстояние между двумя первыми объектами (список)
        **v** — модуль скорости первого объекта относительно второго (список)
    """
    t = []
    r = []
    v = []
    legend = []
    k = 1 # Параметр, отвечающий за то, в заголовке мы или нет 1 -- да, 0 -- нет
    num = 5 # Начальный номер объекта. Можно указать любой, больше 2
    with open("stats.txt") as input_file:
            for line in input_file:
                if k == 1:
                    if line == '#End of the header\n':
                        k = 0  # Конец заголовка
                    else:
                        legend_i = line.split()
                        legend.append(legend_i)
                else: #Вне заголовка
                    if len(line.strip()) == 0 or line[0] == '#':
                        continue  # пустые строки и строки-комментарии пропускаем
                    data_i = line.split()
                    if len(data_i) == 1:
                        t.append(float(data_i[0]))
                        num = 0
                    elif num == 1:
                        data_first_obj = data_i
                    elif num == 2:
                        r_i = ((float(data_i[0]) - float(data_first_obj[0]))**2 +
                               (float(data_i[1]) - float(data_first_obj[1]))**2)**0.5
                        r.append(r_i)

                        v_i = ((float(data_i[2]) - float(data_first_obj[2]))**2 +
                               (float(data_i[3]) - float(data_first_obj[3]))**2)**0.5
                        v.append(v_i)
                    num += 1
    return legend, t, r, v

def draw_plots(legend, t, r, v):
    """
    Рисует графики движения космических объектов
    Args:
        **legend** — список объектов в формате:
            [<тип>,  <радиус в пикселах>, <цвет>]
        **t** — время с начала симуляции (список)
        **r** — расстояние между двумя первыми объектами (список)
        **v** — модуль скорости первого объекта относительно второго (список)
    """
    plt.plot(t, v)
    plt.title(r'$V(t)$')
    plt.grid(True)
    plt.show()

    plt.plot(t, r)
    plt.title(r'$r(t)$')
    plt.grid(True)
    plt.show()
    
    plt.plot(r, v)
    plt.title(r'$V(r)$')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("This module is not for direct call!")