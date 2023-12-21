import datetime

######### DATA #########
# Pega a data atual
dia = datetime.date.today().day
ano = datetime.date.today().year
mês = datetime.date.today().month
sem = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
ds = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta")

# Verifica que dia é hoje de acordo com o padrão de data em inglês ex:(2021/05/10)
num = datetime.date(ano, mês, dia).weekday()
p = (sem[num])

# De acordo com o número que 'p' tiver, é setado um dia da semana conforme o correspondente na lista 'ds'
# 'ds' é abreviação de Dias da Semana

# Verifica se o dia atual é dia útil, se não for é considerado 'fim de semana'
if p in ds:
    h = 'dia de semana'
else:
    h = 'fim de semana'

# Termina o código mostrando que dia é hoje
if h == 'dia de semana':
    print(f"Tenha uma boa {sem[num]} =D")
else:
    print(f"Tenha um bom {sem[num]} =D")

#####################################
    
    