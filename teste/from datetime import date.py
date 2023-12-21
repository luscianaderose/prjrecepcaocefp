from datetime import date

dia_semana = date.today().weekday()
nomes = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")

if dia_semana in {5, 6}:
    print(f"Tenha um bom {nomes[dia_semana]} =D")
else:
    print(f"Tenha uma boa {nomes[dia_semana]} =D")