def linear_regression(data):
    if data is None or len(data) <= 1:
        return 0

    X = range(1, 1 + len(data))
    Y = data
    Xsum = 0.0
    X2sum = 0.0
    Ysum = 0.0
    XY = 0.0
    n = len(X)
    for i in range(n):
        Xsum += X[i]
        Ysum += Y[i]
        XY += X[i] * Y[i]
        X2sum += X[i] ** 2
    k = (Xsum * Ysum / n - XY) / (Xsum ** 2 / n - X2sum)
    # b = (Ysum - k * Xsum) / n
    return k
