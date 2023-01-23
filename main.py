import copy
import math


def get_points_from_file(path: str) -> list[list[int]]:
    """
    Считывает матрицу координат из файла.
    :param path: путь до файла.
    :return: матрица координат точек с параметром.
    """
    # считываем файл построчно: разбиваем строку по пробелам, переводим в целые числа, упаковываем в список
    with open(path, "r") as file:
        return [list(map(int, line.split())) for line in file.readlines()]


def write_points_to_file(path: str, points: list[list[int]], ind: int = None, value: int = None) -> None:
    """
    Записывает матрицу координат в файл, может добавить столбец параметра.
    :param path: путь до файла.
    :param points: матрица координат точек.
    :param ind: индекс столбца параметра.
    :param value: значение параметра.
    """
    points = copy.deepcopy(points)
    with open(path, "w") as file:
        for point in points:
            if ind and value:
                point.insert(ind, value)
            file.write(" ".join(str(c) for c in point) + "\n")


def get_max_dimensions(points: list[list[int]], param_ind: int = None) -> list[int]:
    """
    Возвращает размеры фигуры по всем измерениям.
    :param points: матрица координат точек.
    :param param_ind: индекс столбца параметра, если есть.
    :return: список размеров фигуры по всем измерениям, не учитывая столбец параметра.
    """
    max_d = copy.deepcopy(points[0])
    for p in points:
        for j, d in enumerate(zip(p, max_d)):
            max_d[j] = max(d)
    # увеличиваем на 1 (получаем кол-во возможных координат по каждому измерению), отбрасываем параметр точки
    max_d = [max_d[i] + 1 for i in range(len(max_d)) if i != param_ind]
    return max_d


def get_points_without_param(points: list[list[int]], param_v: int, param_ind: int) -> list[list[int]]:
    """
    Создаёт новую матрицу координат точек, удаляя точки не с переданным параметром и удаляя столбец параметра.
    :param points: матрица координат точек с параметром.
    :param param_v: значение параметра.
    :param param_ind: индекс столбца параметра.
    :return: новая матрица координат точек без параметров.
    """
    new_points = []
    for i, p in enumerate(points):
        if p[param_ind] == param_v:
            del p[param_ind]
            new_points.append(p)
    return new_points


def is_neighbors(p1: list[int], p2: list[int]) -> bool:
    """
    Определяет, являются ли точки соседями. Точки соседи, если лишь одна их координата отличается на единицу.
    :param p1: координаты точки.
    :param p2: координаты точки.
    :return: являются ли точки соседями.
    """
    # отличается ли какая-то координата точек на единицу
    by_step = False
    for i, c in enumerate(zip(p1, p2)):
        if c[0] != c[1]:
            if not by_step and abs(c[0] - c[1]) == 1:
                by_step = True
            else:
                return False
    return by_step


def count_neighbors(points: list[list[int]]) -> int:
    """
    Считает общее кол-во соседей.
    :param points: матрица координат точек.
    :return: кол-во соседей.
    """
    n = 0
    for p1 in points:
        for p2 in points:
            n += 1 if is_neighbors(p1, p2) else 0
    return n


def point_in_row(point: list[int], row: list[int], ind: int) -> bool:
    """
    Определяет, находится ли точка в данном ряду.
    :param point: координаты точки.
    :param row: координаты ряда (на 1 координату меньше чем в точке)
    :param ind: индекс измерения, в котором находится ряд.
    :return:
    """
    # удаляем координату по индексу, в котором находится ряд
    point = copy.deepcopy(point)
    del point[ind]
    return row == point


def shift_point(point: list[int], ind: int, max_d: list[int], step: int) -> None:
    """
    Сдвигает точку в одном измерении. Если точка выходит за фигуру, то зацикливает координату.
    :param point: координаты точки.
    :param ind: индекс координаты, по которой сдвигается точка.
    :param max_d: размеры фигуры.
    :param step: шаг сдвига.
    """
    new_c = point[ind] + step
    if new_c < 0:
        new_c = max_d[ind] - 1
    elif new_c == max_d[ind]:
        new_c = 0
    point[ind] = new_c


def shift_row(points: list[list[int]], row: list[int], ind: int, max_d: list[int], step: int) -> list[list[int]]:
    """
    Сдвигает ряд точек в одном измерении.
    :param points: матрица координат точек
    :param row: координаты ряда (на 1 координату меньше чем в точке)
    :param ind: индекс пропущенной в ряде координаты.
    :param max_d: размеры фигуры.
    :param step: шаг сдвига.
    :return:
    """
    points = copy.deepcopy(points)
    for i, p in enumerate(points):
        if point_in_row(p, row, ind):
            shift_point(p, ind, max_d, step)
    return points


def add_state_to_queue(points: list[list[int]], states: list[list[list[int]]], queue: list[list[list[int]]]) -> None:
    """
    Добавляет матрицу координат точек в очередь, если это состояние ещё не в очереди или ещё не было рассмотрено.
    :param points: матрица координат точек.
    :param states: список состояний, которые были рассмотрены.
    :param queue: список состояний, которые будут рассмотрены.
    """
    # сортируем точки, чтоб избавиться от перестановок
    points.sort()
    if points not in states and points not in queue:
        queue.append(copy.deepcopy(points))


def next_row(prev_row: list[int], max_d: list[int], ind: int) -> list[int]:
    """
    Возвращает следующий ряд.
    :param prev_row: предыдущий ряд.
    :param max_d: размеры фигуры.
    :param ind: индекс измерения, в котором находится ряд
    :return: новый ряд.
    """
    # удаляем размер по индексу, в котором находится ряд
    max_d = copy.deepcopy(max_d)
    del max_d[ind]
    # проходим по оставшимся измерениям, увеличивая координату на 1, если можем, иначе обнуляем и увеличиваем следующую
    for i in range(len(max_d)):
        if prev_row[i] + 1 == max_d[i]:
            prev_row[i] = 0
        else:
            prev_row[i] += 1
            break
    return prev_row


def get_new_states(points: list[list[int]], max_d: list[int], states: list[list[list[int]]],
                   queue: list[list[list[int]]]) -> None:
    """
    Находит и добавляет в очередь новые состояния, которые можно получить из переданного.
    :param points: матрица координат точек.
    :param max_d: размеры фигуры.
    :param states: список состояний, которые были рассмотрены.
    :param queue: список состояний, которые будут рассмотрены.
    :return: кол-во соседей в переданном состоянии.
    """
    states.append(copy.deepcopy(points))
    # координаты ряда (на 1 координату меньше чем в точке)
    row = [0 for _ in range(len(max_d) - 1)]
    # проходим по всем измерениям
    for i in range(len(max_d)):
        # проходим по кол-ву перестановок, исключая текущее измерение (в котором находится ряд)
        for j in range(math.prod([val for ind, val in enumerate(max_d) if ind != i])):
            # добавляем в очередь состояния со сдвигом на +1 и -1 в данном ряду
            add_state_to_queue(shift_row(points, row, i, max_d, +1), states, queue)
            add_state_to_queue(shift_row(points, row, i, max_d, -1), states, queue)
            row = next_row(row, max_d, i)


def get_max_neighbors_recursive(points: list[list[int]], max_d: list[int]) -> (int, list[list[int]]):
    """
    Находит положение с максимальным кол-ом соседей.
    :param points: матрица координат точек.
    :param max_d: размеры фигуры.
    :return: кортеж из максимального кол-ва соседей и состояния, в котором оно было получено.
    """
    states = []
    queue = []
    get_new_states(points, max_d, states, queue)
    max_n = count_neighbors(points)
    max_s = []
    while queue:
        state = queue.pop(0)
        get_new_states(state, max_d, states, queue)
        temp_n = count_neighbors(state)
        if temp_n > max_n:
            max_s = copy.deepcopy(state)
            max_n = temp_n
    return max_n, max_s


if __name__ == '__main__':
    # пути до файлов
    input_file = "E:\Abot\zero.txt"
    output_file = "E:\Abot\one.txt"
    # параметр искомых точек
    param_value = 1
    # индекс столбца параметров в исходных данных (поменять на нужное)
    param_index = 0

    # считываем данные из файла
    points_matrix = get_points_from_file(input_file)
    # определяем размер фигуры
    max_dimensions = get_max_dimensions(points_matrix, param_index)
    # убираем все точки не с искомым параметром, убираем столбец параметра
    points_matrix = get_points_without_param(points_matrix, param_value, param_index)
    # находим максимальное значение соседей
    max_neighbors, max_state = get_max_neighbors_recursive(points_matrix, max_dimensions)
    # находим кол-во точек с искомым параметром
    ones = len(points_matrix)
    # считаем среднее кол-во соседей
    neighbors_average = max_neighbors / ones
    # записываем в файл
    write_points_to_file(output_file, max_state, param_index, param_value)

    print(
        f"координаты точек с параметром {param_value}", *points_matrix,
        "размеры фигуры", max_dimensions,
        "лучший вариант перестановки", *max_state,
        "среднее кол-во соседей", neighbors_average,
        sep="\n"
    ) s
