grid = open("input.txt").read().splitlines()

def solve(row, column, target, plot_positions, direction=(0, 0)):
    if not (0 <= row < len(grid) and 0 <= column < len(grid[0])):
        return frozenset(), [((row, column), direction)]

    if (row, column) in plot_positions:
        return frozenset(), []

    fences = []
    if grid[row][column] == target:
        plot_positions.add((row, column))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            fences += solve(row + dx, column + dy, target, plot_positions, (dx, dy))[1]
    else:
        fences.append(((row, column), direction))

    return plot_positions, fences

positions = set()
plots = dict()
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if (i, j) in positions:
            continue

        plot = solve(i, j, grid[i][j], set())
        for x in plot[0]:
            positions.add(x)

        plots.setdefault(grid[i][j], []).append(plot)

part1 = sum(len(value[0]) * len(value[1]) for plot in plots for value in plots[plot])
print("Part 1:", part1)

part2 = 0
for key in plots.keys():
    for value in plots[key]:
        area = len(value[0])
        fences = value[1]
        for fence in fences:
            for other_fence in fences:
                if fence == other_fence:
                    continue

                distance = (other_fence[0][0] - fence[0][0], other_fence[0][1] - fence[0][1])
                if distance in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    k = 1
                    while (u := ((k * distance[0] + fence[0][0], k * distance[1] + fence[0][1]), fence[1])) in fences:
                        fences.remove(u)
                        k += 1

                    k = -1
                    while (u := ((k * distance[0] + fence[0][0], k * distance[1] + fence[0][1]), fence[1])) in fences:
                        fences.remove(u)
                        k -= 1

        part2 += area * len(fences)

print("Part 2:", part2)
