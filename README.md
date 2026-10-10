# Entrega-Semana-5-Python
Entrega-Semana-2-Python Aluno: Luis Gustavo Marques dos Santos RA: 199949

Programa em Python que lê o arquivo dados.csv (nome, e-mail, CPF, telefone, data e idade), valida cada campo e mostra no terminal um relatório com o total de registros, quantos são válidos e quais falharam, com o motivo. 

As validações usam regex (módulo re) e conferem só o formato, sem calcular dígitos do CPF nem checar se a data existe. As exceções tratadas são FileNotFoundError, ValueError e KeyError, com try/except/else/finally na leitura do arquivo, além de duas exceções personalizadas, FormatoInvalidoError e IdadeInvalidaError.

O dados.csv está "ruim" de propósito: só 2 dos 8 registros são válidos, e cada um dos outros 6 tem um tipo de erro diferente, para mostrar todas as validações funcionando.
