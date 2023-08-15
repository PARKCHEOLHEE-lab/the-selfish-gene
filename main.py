def move(body, interval, direction):
    return moved_boddy


body = [[0, 3],[0, 2],[0, 1],[0, 0],[1, 0],[2, 0],[3, 0]]

move(body=body, interval=2, direction="right")
>>> [[0, 1],[0, 0],[1, 0],[2, 0],[3, 0],[4, 0],[5, 0]]  # expected moved_body for right

move(body=body, interval=2, direction="up")
>>> [[0, 1],[0, 0],[1, 0],[2, 0],[3, 0],[3, 1],[3, 2]]  # expected moved_body for up

move(body=body, interval=2, direction="down")
>>> [[0, 1],[0, 0],[1, 0],[2, 0],[3, 0],[3, -1],[3, -2]]  # expected moved_body for down


