import os
import pandas as pd

# Simulating the path logic from gerar_mock.py
pasta_destino = os.path.join("Mock", "mock", "staging", "Tiflux")
print(f"Target path: {pasta_destino}")

if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)
    print(f"Directory created: {pasta_destino}")
else:
    print(f"Directory already exists: {pasta_destino}")

# Create a small dummy CSV to verify
df = pd.DataFrame({"test": [1, 2, 3]})
df.to_csv(os.path.join(pasta_destino, "Tiflux_tb_Clientes_MOCK.csv"), index=False)
print("Dummy CSV created.")
print(f"Absolute path: {os.path.abspath(pasta_destino)}")
