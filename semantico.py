from colors import Colors
import sys

# atributos dos tokens
token = 0
linha = 1
coluna = 2
tipo = 3


class Semantico(object):
    token = list()
    tokens = list()
    linhaToken = 0
    pilha = list()
    escopo = list()
    pilha_execucao = list()
    sinaliza = False
    semente = 0
    tabela = list()
    msg = ''

    def __init__(self, tokens_de_entrada):
        self.tokens = tokens_de_entrada
        self.escopo.append(['0', 'livre'])

        if (self.programa()):
            print("\nTabela de simbolos:")
            for x in range(len(self.tabela)):
                print(x, self.tabela[x])
            print(Colors().sucess, "\n########SEMÂNTICO COM SUCESSO!!!##########\n", Colors().reset)
        else:
            print(Colors().danger, "\n\n########ERRO NO SEMÂNTICO########")
            print("\nLinha", self.token[1], "Coluna", self.token[2], "Posição", self.linhaToken)
            print(self.msg)

    def programa(self):
        ##print("função programa")
        self.nextToken()

        self.pilha += ['program']
        if (self.token[token] == "program"):
            ##print("encontrado", Colors().blue, "program", Colors().reset)
            ##print("sai da pilha:", self.pilha.pop())
            self.semente += 1
            self.escopo.append([self.semente, 'estrito'])
            self.nextToken()

            self.pilha += ['Identificador']
            if (self.token[tipo] == "Identificador"):
                ##print("encontrado", Colors().blue, self.token[token], Colors().reset)
                ##print("sai da pilha:", self.pilha.pop())
                if(self.inserir([self.token[token], self.escopo, 'program', ''], self.tabela)):

                    self.nextToken()
                    if (self.corpo()):
                        self.nextToken()

                        self.pilha += ['.']
                        if (self.token[token] == '.'):
                            ##print("encontrado", Colors().blue, " .", Colors().reset)
                            ##print("sai da pilha:", self.pilha.pop())
                            self.escopo.pop()
                            return True

        ##print(Colors().warning, "não é programa", Colors().reset)
        self.printPilha()
        return False

    #simbolo, escopo([semente, tipo]), tipo, valor
    def buscar(self, ident):
        idents = list()
        for x in self.tabela:
            if(x[0] == ident[0]):
                idents.append(x)
        id = ident.copy()
        for x in range(len(id[1])):
            if(id[1][-1][1] == 'livre'):
                if(id in idents):
                    print('achou na tabela o id!')
                    return True
                else:
                    id[1].pop()
            else:
                if (id in idents):
                    print(Colors().blue, 'achou', Colors().reset, 'id na tabela de simbolos!')
                    return True
                else:
                    print(' id ainda', Colors().blue, 'nao existe!', Colors().reset)
                    return False

    def inserir(self, linha, tabela):
        if(self.buscar(linha)):
            print(Colors().danger, 'erro', Colors().reset, 'id já existe na tabela de simbolos')
            self.msg = 'Token ' + self.token[token] + ' já declarada!'
            return False
        else:
            print(Colors().sucess, 'sucesso', Colors().reset, 'id inserido na tabela de simbolos')
            tabela.append(linha)
            return True

    def aplicarTipo(self, tipo):
        for x in self.pilha_execucao:
            x[2] = tipo
            if(not self.inserir(x, self.tabela)):
                self.msg += '\nerro em aplicarTipo'
                return False
        return True

    def comparar(self, tipo):
        if(tipo != self.sinaliza):
            return False
        return True

    def nextToken(self):
        self.token = self.tokens[self.linhaToken]
        self.linhaToken += 1
        if (self.token[tipo] == "Comentário"):
            print("encontrado", Colors().blue, "Comentário", Colors().reset)
            self.nextToken()

    def prevToken(self):
        ##print("função prevToken")
        self.linhaToken -= 1
        self.token = self.tokens[self.linhaToken]

    def printPilha(self):
        if(len(self.pilha) > 0):
            for x in range(len(self.pilha)):
                print(x+1, ":", self.pilha[x])
        else:
            print(Colors().sucess, "pilha vazia", Colors.reset)

    def corpo(self):
        ##print("função corpo")

        if (self.dc()):
            self.nextToken()

            self.pilha += ['begin']
            if (self.token[token] == "begin"):
                ##print("encontrado", Colors().blue, " begin", Colors().reset)
                self.semente += 1
                self.escopo.append([self.semente, 'livre'])
                self.nextToken()
                ##print("sai da pilha:", self.pilha.pop())

                if (self.comandos()):
                    self.escopo.pop()
                    self.nextToken()

                    self.pilha += ['end']
                    if (self.token[token] == "end"):
                        ##print("encontrado", Colors().blue, " end", Colors().reset)
                        ##print("sai da pilha:", self.pilha.pop())
                        return True

        ##print(Colors().warning, "não é corpo", Colors().reset)
        return False

    def dc(self):
        ##print("função dc")
        dc_v = self.dc_v()
        if (dc_v or dc_v == 'Deu ruim'):
            if ( dc_v == 'Deu ruim'):
                return False
            else:
                self.nextToken()
                if (self.mais_dc()):
                    return True

                return False

        elif (not dc_v):
            dc_p = self.dc_p()
            if (dc_p or dc_p == 'Deu ruim'):

                if (dc_p == 'Deu ruim'):
                    return False
                else:
                    self.nextToken()
                    if (self.mais_dc()):
                        return True

                    return False

            elif (' '):
                ##print("dc passou em branco")
                ##print("encontrado", Colors().blue, chr(955), Colors().reset)
                self.prevToken()
                return True

    def mais_dc(self):
        ##print("função mais_dc")

        if (self.token[token] == ';'):
            ##print("encontrado", Colors().blue, " ;", Colors().reset)
            self.nextToken()
            if (self.dc()):
                return True
            return False

        elif (' '):
            ##print(Colors().warning, "não é mais_dc", Colors().reset)
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def dc_v(self):
        ##print("função dc_v")

        if (self.token[token] == "var"):
            ##print("encontrado", Colors().blue, " var", Colors().reset)
            self.pilha_execucao.clear()
            self.nextToken()

            if (self.variaveis()):
                self.nextToken()

                self.pilha += [':']
                if (self.token[token] == ':'):
                    ##print("encontrado", Colors().blue, " :", Colors().reset)
                    ##print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    if (self.tipo_var()):
                        return True
            return 'Deu ruim'

        ##print(Colors().warning, "não é dc_v", Colors().reset)
        return False

    def tipo_var(self):
        ##print("função tipo_var")

        self.pilha += ['[ real | integer ]']
        if (self.token[token] == "real"):
            ##print("encontrado", Colors().blue, " real", Colors().reset)
            self.pilha.pop()
            if(self.aplicarTipo('real')):
                return True

        elif (self.token[token] == "integer"):
            ##print("encontrado", Colors().blue, " integer", Colors().reset)
            self.pilha.pop()
            if(self.aplicarTipo('integer')):
                return True

        ##print(Colors().warning, "não é tipo_var", Colors().reset)
        return False

    def variaveis(self):
        ##print("função variaveis")

        self.pilha += ['Variaveis ex: a, b']
        if (self.token[tipo] == "Identificador"):
            ##print("encontrado", Colors().blue, self.token[token], Colors().reset)
            if(self.inserir([self.token[token], self.escopo, 'ident', ''], self.pilha_execucao)):
                self.nextToken()
                ##print("sai da pilha:", self.pilha.pop())

                if (self.mais_var()):
                    return True

        ##print(Colors().warning, "não é variaveis", Colors().reset)
        return False

    def mais_var(self):
        ##print("função mais_var")
        if (self.token[token] == ','):
            ##print("encontrado", Colors().blue, " ,", Colors().reset)
            self.nextToken()

            if (self.variaveis()):
                return True
            return False

        elif (' '):
            ##print("mais_var passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def dc_p(self):
        ##print("função dc_p")

        if (self.token[token] == "procedure"):
            ##print("encontrado", Colors().blue, " procedure", Colors().reset)
            self.nextToken()

            self.pilha += ['ident']
            if (self.token[tipo] == "Identificador"):
                ##print("encontrado", Colors().blue, self.token[token], Colors().reset)
                self.nextToken()
                ##print("sai da pilha:", self.pilha.pop())

                if (self.parametros()):
                    self.nextToken()

                    if (self.corpo()):
                        return True
            return 'Deu ruim'

        ##print(Colors().warning, "não é dc_p", Colors().reset)
        return False

    def parametros(self):
        ##print("função parametros")

        if (self.token[token] == '('):
            ##print("encontrado", Colors().blue, " ( ", Colors().reset)
            self.nextToken()

            if (self.lista_par()):
                self.nextToken()

                self.pilha += [')']
                if (self.token[token] == ')'):
                    ##print("encontrado", Colors().blue, " )", Colors().reset)
                    self.pilha.pop()
                    return True

            return False

        elif (' '):
            ##print("parametros passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def lista_par(self):
        ##print("função lista_par")

        if (self.variaveis()):
            self.nextToken()

            self.pilha += [':']
            if (self.token[token] == ':'):
                ##print("encontrado", Colors().blue, " : ", Colors().reset)
                ##print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.tipo_var()):
                    self.nextToken()

                    if (self.mais_par()):
                        return True

        ##print(Colors().warning, "não é lista_par", Colors().reset)
        return False

    def mais_par(self):
        ##print("função mais_par")

        if (self.token[token] == ';'):
            ##print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()

            if (self.lista_par()):
                return True

            return False

        elif (' '):
            ##print("mais_par passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def corpo_p(self):
        ##print("função corpo_p")

        if (self.dc_loc()):
            self.nextToken()

            self.pilha += ['begin']
            if (self.token[token] == "begin"):
                ##print("encontrado", Colors().blue, " begin", Colors().reset)
                ##print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.comandos()):
                    self.nextToken()

                    self.pilha += 'end'
                    if (self.token[token] == "end"):
                        ##print("encontrado", Colors().blue, " end", Colors().reset)
                        ##print("sai da pilha:", self.pilha.pop())
                        return True

        ##print(Colors().warning, "não é corpo_p", Colors().reset)
        return False

    def dc_loc(self):
        ##print("função dc_loc")

        if (self.dc_v()):
            self.nextToken()

            if (self.mais_dcloc()):
                return True

            return False

        elif (' '):
            ##print("dc_loc passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            return True

    def mais_dcloc(self):
        ##print("função mais_dcloc")

        if (self.token[token] == ';'):
            ##print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()
            self.pilha += ['DC_LOC']

            if (self.dc_loc()):
                ##print("sai da pilha:", self.pilha.pop())
                return True

            return False

        elif (' '):
            ##print("mais_dcloc passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def lista_arg(self):
        ##print("função lista_arg")

        if (self.token[token] == '('):
            ##print("encontrado", Colors().blue, " ( ", Colors().reset)
            self.nextToken()

            if (self.argumentos()):
                self.nextToken()

                self.pilha += [')']
                if (self.token[token] == ')'):
                    ##print("encontrado", Colors().blue, " ( ", Colors().reset)
                    ##print("sai da pilha:", self.pilha.pop())
                    return True

            return False

        elif (' '):
            ##print("lista_arg")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def argumentos(self):
        ##print("função argumentos")

        if (self.token[tipo] == 'Identificador'):
            ##print("encontrado", Colors().blue, self.token[token], Colors().reset)
            self.nextToken()

            if (self.mais_ident()):
                return True

        return False

    def mais_ident(self):
        ##print("função mais_ident")

        if (self.token[token] == ';'):
            ##print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()

            if (self.argumentos()):
                return True

            return False

        elif (' '):
            ##print("mais_ident passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def pfalsa(self):
        ##print("função pfalsa")

        if (self.token[token] == "else"):
            ##print("encontrado", Colors().blue, " else", Colors().reset)
            self.nextToken()

            if (self.comandos()):
                return True
            return False

        elif (' '):
            ##print("pfalsa passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def comandos(self):
        ##print("função comandos")

        if (self.comando()):
            self.nextToken()

            if (self.mais_comandos()):
                return True

        return False

    def mais_comandos(self):
        ##print("função mais_comandos")

        if (self.token[token] == ';'):
            ##print("encontrado", Colors().blue, " ; ", Colors().reset)
            self.nextToken()

            if (self.comandos()):
                return True

            return False

        elif (' '):
            ##print("mais_comandos passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def comando(self):
        ##print("função comando")
        self.pilha += ['Comando: [ read | write | if | while | Identificador ]']

        if (self.token[token] == "read"):
            ##print("encontrado", Colors().blue, " read", Colors().reset)
            self.pilha.pop()
            self.nextToken()

            self.pilha += ['(']
            if (self.token[token] == "("):
                ##print("encontrado", Colors().blue, " (", Colors().reset)
                ##print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                self.pilha += ['VARIAVEIS']
                if (self.variaveis()):
                    ##print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    self.pilha += ['[ ) | , ]']
                    if (self.token[token] == ")"):
                        ##print("encontrado", Colors().blue, " )", Colors().reset)
                        ##print("sai da pilha:", self.pilha.pop())
                        return True

        elif (self.token[token] == "write"):
            ##print("encontrado", Colors().blue, " write", Colors().reset)
            self.nextToken()
            self.pilha.pop()

            self.pilha += ['(']
            if (self.token[token] == "("):
                ##print("encontrado", Colors().blue, " (", Colors().reset)
                ##print("sai da pilha:", self.pilha.pop())
                self.nextToken()

                if (self.variaveis()):
                    self.nextToken()

                    self.pilha += [')']
                    if (self.token[token] == ")"):
                        ##print("encontrado", Colors().blue, " )", Colors().reset)
                        ##print("sai da pilha:", self.pilha.pop())
                        return True

        elif (self.token[token] == "while"):
            ##print("encontrado", Colors().blue, " while", Colors().reset)
            self.nextToken()
            self.pilha.pop()

            if (self.condicao()):
                self.nextToken()

                self.pilha += ['do']
                if (self.token[token] == "do"):
                    ##print("encontrado", Colors().blue, " do", Colors().reset)
                    ##print("sai da pilha:", self.pilha.pop())
                    self.nextToken()

                    if (self.comandos()):
                        self.nextToken()

                        self.pilha += ['$']
                        if (self.token[token] == '$'):
                            ##print("encontrado", Colors().blue, " $", Colors().reset)
                            ##print("sai da pilha:", self.pilha.pop())
                            return True

        elif (self.token[token] == "if"):
            ##print("encontrado", Colors().blue, " if", Colors().reset)
            self.nextToken()
            self.pilha.pop()

            if (self.condicao()):
                self.nextToken()

                self.pilha += ['then']
                if (self.token[token] == "then"):
                    ##print("encontrado", Colors().blue, " then", Colors().reset)
                    self.nextToken()
                    ##print("sai da pilha:", self.pilha.pop())

                    if (self.comando()):
                        self.nextToken()

                        if (self.pfalsa()):
                            self.nextToken()

                            self.pilha += ['$']
                            if (self.token[token] == '$'):
                                ##print("encontrado", Colors().blue, " $", Colors().reset)
                                ##print("sai da pilha:", self.pilha.pop())
                                return True

        elif (self.token[tipo] == "Identificador"):
            ##print("encontrado", Colors().blue, self.token[token], Colors().reset)
            self.nextToken()
            self.pilha.pop()

            if (self.restoident()):
                return True

        ##print(Colors().warning, "não é comando", Colors().reset)
        return False

    def restoident(self):
        ##print("função restoident")

        if (self.token[token] == ":="):
            ##print("encontrado", Colors().blue, " :=", Colors().reset)
            self.nextToken()

            if (self.expressao()):
                return True

        elif (self.lista_arg()):
            return True

        ##print(Colors().warning, "não é restoident", Colors().reset)
        return False

    def condicao(self):
        ##print("função condicao")

        if (self.expressao()):
            self.nextToken()

            if (self.relacao()):
                self.nextToken()

                if (self.expressao()):
                    return True

        ##print(Colors().warning, "não é condicao", Colors().reset)
        return False

    def relacao(self):
        ##print("função relacao")

        if (self.token[token] == '='):
            ##print("encontrado", Colors().blue, " =", Colors().reset)
            return True

        elif (self.token[token] == "<>"):
            ##print("encontrado", Colors().blue, " <>", Colors().reset)
            return True

        elif (self.token[token] == ">="):
            ##print("encontrado", Colors().blue, " >=", Colors().reset)
            return True

        elif (self.token[token] == "<="):
            ##print("encontrado", Colors().blue, " <=", Colors().reset)
            return True

        elif (self.token[token] == '>'):
            ##print("encontrado", Colors().blue, " >", Colors().reset)
            return True

        elif (self.token[token] == '<'):
            ##print("encontrado", Colors().blue, " <", Colors().reset)
            return True

        ##print(Colors().warning, "não é relacao", Colors().reset)
        self.pilha += ['Relação: [ = | <> | >= | <= | > | < ]']
        return False

    def expressao(self):
        ##print("função expressao")

        self.pilha += ['Expressao ex: a + b * (c - a)']
        if (self.termo()):
            self.nextToken()

            if (self.outros_termos()):
                self.pilha.pop()
                return True

        ##print(Colors().warning, "não é expressao", Colors().reset)
        return False

    def op_un(self):
        ##print("função relacao")

        if (self.token[token] == '+'):
            ##print("encontrado", Colors().blue, " +", Colors().reset)
            return True

        elif (self.token[token] == '-'):
            ##print("encontrado", Colors().blue, " -", Colors().reset)
            return True

        elif (' '):
            ##print("op_un passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def outros_termos(self):
        ##print("função outros_termos")

        if (self.op_ad()):
            self.nextToken()

            if (self.termo()):
                self.nextToken()
                ##print('termo de outros_termos passou')
                if (self.outros_termos()):
                    return True

            return False

        elif (' '):
            ##print("outros_termos passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def op_ad(self):
        ##print("função op_ad")

        if (self.token[token] == '+'):
            ##print("encontrado", Colors().blue, " +", Colors().reset)
            return True

        elif (self.token[token] == '-'):
            ##print("encontrado", Colors().blue, " -", Colors().reset)
            return True

        ##print(Colors().warning, "não é op_ad", Colors().reset)
        return False

    def termo(self):
        ##print("função termo")

        if (self.op_un()):
            self.nextToken()

            if (self.fator()):
                self.nextToken()

                if (self.mais_fatores()):
                    return True

        ##print(Colors().warning, "não é termo", Colors().reset)
        return False

    def mais_fatores(self):
        ##print("função mais_fatores")

        if (self.op_mul()):
            self.nextToken()

            if (self.fator()):
                self.nextToken()

                if (self.mais_fatores()):
                    return True
            return False

        elif (' '):
            ##print("mais_fatores passou em branco")
            ##print("encontrado", Colors().blue, chr(955), Colors().reset)
            self.prevToken()
            return True

    def op_mul(self):
        ##print("função op_mul")

        if (self.token[token] == '*'):
            ##print("encontrado", Colors().blue, " *", Colors().reset)
            return True

        elif (self.token[token] == '/'):
            ##print("encontrado", Colors().blue, " /", Colors().reset)
            return True

        ##print(Colors().warning, "não é op_mul", Colors().reset)
        return False

    def fator(self):
        ##print("função fator")

        if (self.token[tipo] == "Identificador"):
            ##print("encontrado", Colors().blue, self.token[token], Colors().reset)
            return True

        elif (self.token[tipo] == "Numero inteiro"):
            ##print("encontrado", Colors().blue, " Numero inteiro", Colors().reset)
            return True

        elif (self.token[tipo] == "Numero de ponto flutuante"):
            ##print("encontrado", Colors().blue, " Numero de ponto flutuante", Colors().reset)
            return True

        elif (self.token[token] == '('):
            ##print("encontrado", Colors().blue, " (", Colors().reset)
            self.nextToken()

            if (self.expressao()):
                self.nextToken()

                self.pilha += [')']
                if (self.token[token] == ')'):
                    ##print("encontrado", Colors().blue, " )", Colors().reset)
                    ##print("sai da pilha:", self.pilha.pop())
                    return True

        ##print(Colors().warning, "não é fator", Colors().reset)
        return False