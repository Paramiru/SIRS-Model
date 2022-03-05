
def infectednn(arr, row, col):
    return arr[(row+1) % len(arr[0]), col] == 1 or \
        arr[row, (col+1) % len(arr[0])] == 1 or \
        arr[row-1, col] == 1 or \
        arr[row, col-1] == 1
        