import pandas as pd

try:
    def load_positions_and_salaries():
        df = pd.read_csv("data/cargos-e-salarios-atualizados.csv")
        return df
except OSError as error:
    print("Erro ao importar a base de daddos!".upper())
    print(f"Detalhes do erro: {error}".upper())