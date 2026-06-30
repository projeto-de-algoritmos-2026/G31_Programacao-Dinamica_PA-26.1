def knapsack_iterativo(capacidade, pesos, valores):
    """
    Knapsack 0/1 iterativo (tabulation).
    capacidade e pesos em unidades inteiras (ex: ×10 para 0.1 kg de precisão).
    Retorna (valor_max, indices_selecionados, tabela_dp).
    """
    n = len(pesos)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, v = pesos[i - 1], valores[i - 1]
        for j in range(capacidade + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= w:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w] + v)

    selecionados = []
    j = capacidade
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selecionados.append(i - 1)
            j -= pesos[i - 1]

    return dp[n][capacidade], list(reversed(selecionados)), dp


def knapsack_recursivo(capacidade, pesos, valores):
    """
    Knapsack 0/1 recursivo com memoization (top-down).
    Retorna (valor_max, indices_selecionados).
    """
    n = len(pesos)
    memo = {}

    def resolver(i, restante):
        if i == 0 or restante == 0:
            return 0
        if (i, restante) in memo:
            return memo[(i, restante)]
        resultado = resolver(i - 1, restante)
        if pesos[i - 1] <= restante:
            resultado = max(resultado, resolver(i - 1, restante - pesos[i - 1]) + valores[i - 1])
        memo[(i, restante)] = resultado
        return resultado

    valor_max = resolver(n, capacidade)

    selecionados = []
    restante = capacidade
    for i in range(n, 0, -1):
        if resolver(i, restante) != resolver(i - 1, restante):
            selecionados.append(i - 1)
            restante -= pesos[i - 1]

    return valor_max, list(reversed(selecionados))
