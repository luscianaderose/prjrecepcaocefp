class Pessoa:
    riscado = 'riscado'
    atendendo = 'atendendo'
    aguardando = 'aguardando'
    
    def __init__(self, numero, nome, estado='aguardando', camara=None, dupla=-1, asterisco=0, observacao=''):
        self.nome = nome
        self.numero = numero
        self.estado = estado
        self.camara = camara
        self.dupla = dupla
        self.asterisco = asterisco
        self.observacao = observacao

    def __str__(self):
        return self.nome
     
    def csv(self):
        return f'{self.numero},{self.nome},{self.estado},{self.camara},{self.dupla},{self.asterisco},{self.observacao}'
    
    def nome_exibicao(self):
        if self.estado == self.riscado:
            return f'<s>{self.nome}</s> - {self.camara}'
        elif self.estado == self.atendendo:
            return f'<b>{self.nome}</b> - {self.camara}'
        else:
            return f'{self.nome}'
        
    def __repr__(self):
        return self.nome
    
    
class Fila():
    def __init__(self, atividade, nome_arquivo, nome_display):
        self.atividade = atividade
        self.nome_display = nome_display
        self.nome_arquivo = nome_arquivo
        self.fila = {}
        self.proximo_numero = 1
    
    def __contains__(self, numero):
        return numero in self.fila
    
    def adicionar_pessoa(self, pessoa, numero):
        for p in self.fila.values():
            if p.nome == pessoa.nome:
                raise Exception('Não foi possível registrar porque o nome já existe.')
        if numero in self.fila:
            raise Exception('Não foi possível registrar porque o número já existe.')
        self.fila[numero] = pessoa
        self.proximo_numero += 1
        self.salvar_fila()

    def remover_pessoa(self, numero):
        if numero not in self.fila:
            raise Exception('Não foi possível remover porque a pessoa não existe.')
        pessoa = self.fila[numero]
        if pessoa.dupla != - 1:
            self.fila[pessoa.dupla].dupla = -1
        del self.fila[numero]
        self.salvar_fila()

    def editar_pessoa(self, numero, nome):
        for p in self.fila.values():
            if p.nome == nome:
                return #Exception('Não foi possível registrar porque o nome já existe.')
        if numero not in self.fila:
            raise Exception('Não foi possível registrar porque o número não existe.')
        self.fila[numero].nome = nome
        self.salvar_fila()

    def values(self):
        return sorted(self.fila.values(), key=lambda p: p.numero)
    
    def clear(self):
        self.fila.clear()

    def get(self, numero):
        if numero in self.fila:
            return self.fila[numero]
        return None
    
    def trocar_posicao(self, n1, n2, ignorar_duplas=False):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível mover!')
        if n2 < n1:
            return self.trocar_posicao(n2, n1, ignorar_duplas)
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        if ignorar_duplas == False and pessoa1.dupla != n2 and (pessoa1.dupla != -1 or pessoa2.dupla != -1):
            if pessoa1.dupla != -1 and pessoa2.dupla != -1: #p1+p2 tem dupla. Se tiver dupla e se for trocar com alguem que nao é a propria dupla
                self.trocar_posicao(n1, pessoa2.dupla, ignorar_duplas=True)
                self.trocar_posicao(pessoa1.dupla, n2, ignorar_duplas=True)
            elif pessoa1.dupla != -1: #somente a p1 tem dupla
                self.trocar_posicao(n1, n2, ignorar_duplas=True)
                self.trocar_posicao(n1, pessoa1.dupla, ignorar_duplas=True)
            elif pessoa2.dupla != -1: #somente a p2 tem dupla
                self.trocar_posicao(n1, n2, ignorar_duplas=True)
                self.trocar_posicao(n2, pessoa2.dupla, ignorar_duplas=True)
            return 
        if pessoa1.dupla != -1:
            dupla = self.fila[pessoa1.dupla]
            dupla.dupla = n2
        if pessoa2.dupla != -1:
            dupla = self.fila[pessoa2.dupla]
            dupla.dupla = n1
        pessoa1.numero = n2
        pessoa2.numero = n1
        self.fila[n1] = pessoa2
        self.fila[n2] = pessoa1
        self.salvar_fila()

    def keys(self):
        return sorted(self.fila.keys())
    
    def criar_dupla(self, n1, n2):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível criar dupla!')
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        if pessoa1.dupla != -1 or pessoa2.dupla != -1:
            raise Exception ('Não é possível criar dupla uma pessoa de outra dupla!')
        pessoa1.dupla = n2
        pessoa2.dupla = n1
        self.salvar_fila()

    def cancelar_dupla(self, n1):
        if n1 not in self.fila:
            raise Exception ('Não foi possível cancelar a dupla!')
        pessoa1 = self.get(n1)
        pessoa2 = self.get(pessoa1.dupla)
        pessoa1.dupla = -1
        pessoa2.dupla = -1
        self.salvar_fila()

    def salvar_fila(self):
        with open(self.nome_arquivo, 'w') as f:
            for pessoa in self.values():
                f.write(f'{pessoa.csv()}\n')

    def ler_fila(self):
        with open(self.nome_arquivo, 'r') as f:
            for linha in f.read().splitlines():
                if not linha:
                    continue
                numero, nome, estado, camara, dupla, asterisco, observacao = linha.split(',', 6)
                pessoa = Pessoa(int(numero), nome, estado, camara, int(dupla), int(asterisco), observacao)
                self.adicionar_pessoa(pessoa, pessoa.numero)

    def toggle_asterisco(self, numero_atendido):
        pessoa = self.get(numero_atendido)
        pessoa.asterisco = 0 if pessoa.asterisco else 1
        self.salvar_fila()
    
    def adicionar_observacao(self, numero_atendido, observacao):
        pessoa = self.get(numero_atendido)
        pessoa.observacao = observacao
        self.salvar_fila()

    def get_posicao(self, numero):
        if numero in self.fila:
            for index, pessoa in enumerate(self.values()):
                if pessoa.numero == numero:
                    return index + 1
        return None


class Camara:
    fechada = '<span class="icone-fechada"></span> FECHADA'
    atendendo = '<span class="icone-atendendo"></span> ATENDENDO'
    avisar = '<span class="icone-avisar"></span> ÚLTIMO'
    avisado = '<span class="icone-avisado"></span> FOI AVISADO'

    def __init__(self, numero_camara, fila, nome_fila, estado=fechada, capacidade_maxima=5):
        self.numero_camara = numero_camara
        self.fila = fila
        self.nome_fila = nome_fila
        self.pessoa_em_atendimento = None
        self.numero_de_atendimentos = 0
        self.estado = estado
        self.audio = f'camara{numero_camara}.mp3'
        self.capacidade_maxima = capacidade_maxima

    def fechar(self):
        self.pessoa_em_atendimento = None
        self.estado = self.fechada

    def abrir(self):
        self.numero_de_atendimentos = 0
        self.estado = self.atendendo


    def chamar_atendido(self):
        '''Encontra a primeira pessoa da fila que não foi chamada, marca como chamada 
        e adiciona a self.pessoa_em_atendimento. Caso a pessoa tenha uma dupla, 
        a sua dupla também será marcada.'''
        if self.estado != self.atendendo:
            return self.estado
        for pessoa in self.fila.values():
            if pessoa.estado == pessoa.aguardando:
                break
        else:
            self.estado = self.avisar
            return self.estado
        if self.pessoa_em_atendimento:
            self.pessoa_em_atendimento.estado = self.pessoa_em_atendimento.riscado
            if self.pessoa_em_atendimento.dupla != -1:
                dupla = self.fila.get(self.pessoa_em_atendimento.dupla)
                dupla.estado = dupla.riscado
        self.pessoa_em_atendimento = pessoa
        self.pessoa_em_atendimento.camara = self.numero_camara
        self.pessoa_em_atendimento.estado = pessoa.atendendo
        self.numero_de_atendimentos += 1
        if self.pessoa_em_atendimento.dupla != -1:
            dupla = self.fila.get(self.pessoa_em_atendimento.dupla)
            dupla.camara = self.numero_camara
            dupla.estado = dupla.atendendo
            self.numero_de_atendimentos += 1

        retorno = f'Câmara {self.numero_camara} chamando {self.pessoa_em_atendimento}.'
        if self.numero_de_atendimentos >= self.capacidade_maxima:
            self.estado = self.avisar
        self.fila.salvar_fila()
        return retorno
    
    def bolinhas(self):
        bolinhas = []
        for bola in range(0, self.numero_de_atendimentos):
            if bola > 0 and bola % 5 == 0:
                bolinhas.append('<br>&nbsp;&#9899;')
            else:
                bolinhas.append('&#9899;')
        for bola in range(self.numero_de_atendimentos, self.capacidade_maxima):
            if  bola > 0 and bola % 5 == 0:
                bolinhas.append('<br>&nbsp;&#9898;')
            else:
                bolinhas.append('&#9898;')
        return ''.join(bolinhas)
    
def salvar_camaras(dict_camaras, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for camara in dict_camaras.values():
            f.write(f'{camara.numero_camara},{camara.pessoa_em_atendimento.numero if camara.pessoa_em_atendimento is not None else ""},{camara.numero_de_atendimentos},{camara.estado},{camara.capacidade_maxima}\n')

def ler_camaras(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return f.read().splitlines()