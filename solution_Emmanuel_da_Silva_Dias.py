from itertools import chain
from collections import Counter

# FILE = "./test.txt"
# OUTPUT = "./test_out.txt"

FILE = "./small.txt"
OUTPUT = "./small_out.txt"
 
# FILE = "./large.txt"
# OUTPUT = "./large_out.txt"


def get_all_letters (strings: list[str]) -> set:
    """
    Retorna uma colecao com todas as letras presentes
    num determinado conjunto de strings
    """
    return set(chain.from_iterable(strings))


def get_position (str: str, ch: chr) -> int:
    """ 
    Retorna um inteiro correspondente as posicoes 
    do caractere em uma determinada palavra

    eg: get_position('aaba', 'a')
        >> 4 (1101 em binario)
    """
    pos = 0
    for letter in str:
        pos = (pos << 1)
        if letter == ch:
            pos += 1
    return pos


def get_all_positions (words: list[str], ch: chr) -> list:
    """
    Retorna as posicoes em que o caractere aparece
    para um determinado conjunto de palavras
    """
    curr_letter_positions = []
    for w in words:
        pos = get_position(w, ch)
        if pos > 0:
            curr_letter_positions.append(pos)
    return curr_letter_positions


def keep_compatible_words(words: list[str], ch: chr, pos: int) -> list[str]:
    """
    Para um determinado conjunto de palavras, retorna aquelas
    em que o caractere dado aparece na posicao especificada
    (removendo-o antes de retornar) 
    """
    subwords = []
    for w in words:
        if (get_position(w, ch) == pos):
            subwords.append(w.replace(ch, ""))
    return subwords


def remove_words_with_letter(words: list[str], ch: chr) -> list[str]:
    """
    Para um determinado conjunto de palavras, retorna aquelas
    em que o caractere dado nao aparece em nenhuma posicao
    """
    subwords = []
    for w in words:
        if get_position(w, ch) == 0:
            subwords.append(w)
    return subwords


def calculate_identifiable_words (words: list[str]) -> int:
    """
    Retorna a quantidade de palavras as quais o jogador
    atual sera capaz de acertar com a estrategia
    """
    all_letters = get_all_letters(words)
    max_identifiable_words = 0

    # Para cada letra, verifica quantas palavras podera
    # identificar e, se for a maxima ate entao, armazena-a
    for letter in all_letters:
        already_identified = 0
        will_identify = 0 
        other_didnt_identify = 0
        
        positions = get_all_positions(words, letter)
        # Aglutina as posicoes iguais, contando suas repeticoes
        position_and_quantity = Counter(positions)
        
        for pos, qty in position_and_quantity.items():
            # Caso haja mais de uma palavra para uma mesma disposicao
            # eh necessario verificar quantas serao identificaveis
            # para os palpites adicionais
            if qty > 1:
                subwords = keep_compatible_words(words, letter, pos)
                will_identify += calculate_identifiable_words(subwords)
            # Caso haja apenas uma palavra para uma dada disposicao
            # ela ja eh automaticamente identificavel
            else: 
                already_identified += 1
        
        words_without_letter = remove_words_with_letter(words, letter)

        # Dado que o segundo jogador joga com estrategia otima, ele tem p >= 0.5
        # de vencer e, portanto, identifica pelo menos metade das palavras restantes
        # Assim, other_didnt_identify eh no maximo len(words_without_letter)//2
        if max_identifiable_words < (already_identified + will_identify + (len(words_without_letter)//2)):
            if (words_without_letter != []):
                # Contabiliza as palavras que o adversario nao acerta na sua vez
                other_didnt_identify = len(words_without_letter) - calculate_identifiable_words(words_without_letter)
            
            if max_identifiable_words < (already_identified + will_identify + other_didnt_identify):
                max_identifiable_words = already_identified + will_identify + other_didnt_identify

    return max_identifiable_words
    

def main() -> None:
    """
    Ler linha a linha do arquivo e calcular a probabilidade
    para o conjunto de palavras lidas, escrevendo-a na saida
    """
    with open(FILE,'r') as data_file:
        
        with open(OUTPUT, 'w') as out_file:
            for line in data_file:
                words = line.split()
                probability = calculate_identifiable_words(words) / len(words)
                
                # print('{:.6f}'.format(probability))
                out_file.write('{:.6f}\n'.format(probability))


if __name__ == "__main__":
    main()
        