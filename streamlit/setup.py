import os

with open(os.path.join('C:\\Data Science\\Geleia\\novo-covid-vix\\streamlit', 'Procfile'), "w") as file1:
    toFile = 'web: sh setup.sh && streamlit run Predicao_Covid.py'

    file1.write(toFile)