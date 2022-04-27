import string
from json import load as jsonload
from unidecode import unidecode

from math import sqrt

alphabet = string.ascii_lowercase
Alphabet = string.ascii_uppercase

def __mean(L: list) -> float:
    return sum(L) / len(L)

def __multi_mean(a: list, b: list) -> float:
    return __mean([b[i] * a[i] for i in range(len(a))])

def __variance(L: list) -> float:
    return __mean([e ** 2 for e in L]) - (__mean(L) ** 2)

def __covariance(a: list, b: list) -> float:
    return __multi_mean(a, b) - (__mean(a) * __mean(b))

def __coeff_corr(a: list, b: list) -> float:
    return (__covariance(a, b) / (sqrt(__variance(a)) * sqrt(__variance(b)))).real

def __get_frequency(text: str) -> dict:
    dictionary = dict([(letter, 0) for letter in alphabet])
    total = 0

    text = unidecode(text).lower()

    for letter in alphabet:
        occu = text.count(letter)
        dictionary[letter] += occu
        total += occu

    for letter in dictionary.keys():
        dictionary[letter] /= total

    return dictionary


def __shift_json(dict_, gap) -> dict:
    tmp = {}
    for a in dict_.keys():
        tmp[a] = dict_[crypt(a, gap)]
    
    return tmp


def crypt(message: str, key: int) -> str:
    """crypt the message with caesar key

    Args:
        msg (str): clear message
        key (int): caesar key

    Returns:
        str: the encrypt message
    """
    message = unidecode(message.replace("'", ""))
    encrypt = ""
    for letter in message:
        if letter == " ":
            encrypt += " "
        elif letter.lower() not in alphabet:
            continue
        elif letter == letter.lower():
            encrypt += alphabet[(alphabet.find(letter) + key) % 26]            
        elif letter == letter.upper():
            encrypt += Alphabet[(Alphabet.find(letter) + key) % 26]

    return encrypt


def decrypt_with_key(message: str, key: int) -> str:
    """decrypt the message with caesar key

    Args:
        msg (str): encrypt message
        key (int): caesar key

    Returns:
        str: clear message
    """
    return crypt(message, -key)


def decrypt_without_key(message: str, file_alphabet_frequency: str = "french_alphabet_frequency.json") -> dict:
    """decrypt the message with caesar key, the message must be large so that the program can deduce the key

    Args:
        msg (str): encrypt message
        file_alphabet_frequency (str, optional): file name of the alphabet frequency. Defaults to the french one.

    Returns:
        dict: clear message -> format: {key: int, text: str}
    """
    try:
        alphabet_frequency = jsonload(open(file_alphabet_frequency, "r"))
    except FileNotFoundError:
        raise FileNotFoundError(f"\"{file_alphabet_frequency}\" not found")

    encrypt_frequency = __get_frequency(message)

    dic = {}
    for i in range(26):
        dic[i] = __coeff_corr(list(encrypt_frequency.values()), list(__shift_json(alphabet_frequency, i).values()))

    response = ""
    max_ = max(list(dic.values()))
    for key, value in dic.items():
        if value == max_:
            response = crypt(message, key)
            return {"key": key, "text": response}
