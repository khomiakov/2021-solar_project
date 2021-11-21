# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.
    Параметры:
    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    connection = False
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        if r == 0: connection = True  # Защита от бесконечной силы
        body.Fx += gravitational_constant * body.m * obj.m * (obj.x - body.x) / r**3
        body.Fy += gravitational_constant * body.m * obj.m * (obj.y - body.y) / r**3
    if connection: body.Fx = body.Fy = 0


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.
    Параметры:
    **body** — тело, которое нужно переместить.
    """
    # запоминаем начальные координаты тела
    x1 = body.x
    y1 = body.y

    # рассчитываем ускорение до перемещения
    if body.m != 0:
        ax1 = body.Fx/body.m
        ay1 = body.Fy/body.m
    else:
        ax1 = ay1 = 0

    # оценочно рассчитываем положение планеты через dt
    body.x += body.Vx*dt + ax1 * dt**2 / 2
    body.y += body.Vy*dt + ay1 * dt**2 / 2

    # рассчитываем ускорение после перемещения
    if body.m != 0:
        ax2 = body.Fx/body.m
        ay2 = body.Fy/body.m
    else:
        ax2 = ay2 = 0

    # берем среднее ускорение между начальным и оценочным конечным положениями
    ax = (ax1 + ax2) / 2
    ay = (ay1 + ay2) / 2

    # "точные" конечные координаты планеты (начальное положение + среднаяя скорость * dt + среднее ускорение * dt**2)
    body.x = x1 + dt * (body.Vx + (body.Vx + ax * dt)) / 2 + ax * dt**2 / 2
    body.y = y1 + dt * (body.Vy + (body.Vy + ay * dt)) / 2 + ay * dt**2 / 2

    body.Vx += ax*dt
    body.Vy += ay*dt


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объеspace_objectsктов.
    Параметры:
    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects)
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")