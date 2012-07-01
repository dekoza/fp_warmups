#!/usr/bin/env python2
#coding: utf-8
"""Program zrobiony w stylu zbliżonym do overarchitectured.
Pominięto definicje specjalistycznych typów danych - typy wbudowane w Pythona zupełnie wystarczają.
Próbowałem zachować jak największą zgodność z Zen Pythona.

Podejście pierwsze.

Korzysta z wyrażeń regularnych i wyjątków.

Na końcu zaweria unittesty dla najważniejszych funkcji.

SPECYFIKACJA:
<cytat z oryginalnego mejla>
Program do zrealizowania jako rozgrzewka / test czy rozumiecie przykład _overarchitectured jest bardzo prosty:

1. Pobiera od użytkownika ścieżkę pliku tekstowego.

2. Pobiera z pliku tekstowego jakieś słowa (np. "Lorem ipsum" - w necie jest wyjaśnienie co to jest Lorem ipsum). Delimiterem (rozdzielnikiem) słów jest spacja.

3. Usuwa wszystkie słowa krótsze niż 4 litery (czyli akceptujemy 4+) i słowa zawierające coś innego niż tylko małe i duże litery alfabetu angielskiego (czyli azAZ). Usuwamy też wszystkie znaki nie będące literami azAZ.

4. Losuje cztery słowa z istniejących.

5. Znajduje część wspólną liter (nieważne czy wielkie czy małe, czyli 'case insensitive'):

"Aniela"
"Natalia"
"Anna"
"Irena"

da nam:

"a", "n", bo to jedyne litery występujące we wszystkich tych słowach (mimo, że w wersjach wielka i mała).

6. Wyświetli wylosowane słowa oraz część wspólną.

Zabezpieczcie się przed:

- możliwościami złośliwości użytkownika (3 słowa w pliku, brak 4 poprawnych słów, niewłaściwe znaki...) i zaraportujcie jeśli plik wejściowy jest niewłaściwy w odpowiedni sposób.

- błędną ścieżką ze strony użytkownika. Znowu, zaraportujcie to jakoś.

Sposób raportowania i wyświetlania jest dowolny, byle był zrozumiały ;-).
</cytat>

ZNANE BŁĘDY:
- Wyrazy nie mogą zawierać polskich liter.

Jak testować z użyciem unittest:
$ cd /ścieżka/do/katalogu/z/plikiem
$ python2 -m unittest warmup  # BEZ .py!


TODO:
- Poprawić dokumentację
"""
__author__ = 'Dominik Kozaczko'

# importy

import os
from exceptions import Exception
import re
import random
import unittest
import argparse

# domyślna konfiguracja
SETTINGS = {
    'MIN_LENGTH': 4,        # minimalna długość słowa
    'HOW_MANY': 4,          # minimalna liczba słów
}

# Definicje wyjątków:

class FilePathError(Exception):
    """Niepoprawna ścieżka do pliku."""
    pass


class NotAFileError(Exception):
    """Ścieżka nie wskazuje na plik"""
    pass


class NotEnoughCorrectWordsError(Exception):
    """Plik nie zawiera dostatecznej liczby poprawnych wyrazów."""
    pass


class NotEnoughWordsError(Exception):
    """Plik nie zawiera dostatecznej liczby wyrazów."""
    pass


# funkcje realizujące zadanie

def parse_arguments():
    """Umożliwia podanie ścieżki do pliku przez parametr.
    Zmienia domyślną konfigurację (na czas wykonania) w zależności od podanych parametrów."""
    parser = argparse.ArgumentParser(description="Randomly pick some words from a file and display common letters")
    parser.add_argument('file', metavar='FILE', help="File to play with; if ommited, you will be asked for a path", nargs='?', default=None)
    parser.add_argument('-l', '--min-length', metavar='L', type=int, help="Minimum length of a word (default: {})".format(SETTINGS['MIN_LENGTH']), default=SETTINGS['MIN_LENGTH'])
    parser.add_argument('-w', '--how-many', metavar='N', type=int, help="How many words should be picked (default: {})".format(SETTINGS['HOW_MANY']), default=SETTINGS['HOW_MANY'])
    args = parser.parse_args()
    # nie jestem pewny, czy to w dobrym guście, ale pasuje do Zen :)
    SETTINGS['MIN_LENGTH'] = args.min_length
    SETTINGS['HOW_MANY'] = args.how_many
    return args

def get_path():
    """Pobiera od użytkownika ścieżkę pliku tekstowego.
    Łatwo można zmienić sposób podawania pliku."""
    args = parse_arguments()
    if args.file is not None:
        filename = args.file
    else:
        try:
            # importuję dopiero tutaj, żeby wygodniej obsłużyć możliwe wyjątki ;)
            # np. może nie być biblioteki Tk lub ekranu graficznego
            from Tkinter import Tk
            from tkFileDialog import askopenfilename
            Tk().withdraw()
            filename = askopenfilename()
        except:
            # fallback do trybu tekstowego
            filename = raw_input("Podaj ścieżkę do pliku: ")
    return filename

def get_file_content(path):
    """Wczytuje plik i zwraca jego zawartość w postaci łańcucha"""
    if os.path.exists(path):
        if os.path.isfile(path):
            return open(path).read()
        else:
            raise NotAFileError, "Podany zasób nie jest plikiem"
    else:
        raise FilePathError, "Nieprawidłowa ścieżka"

def get_words(words, min_length=None, how_many=None):
    """Usuwa słowa krótsze niż czteroliterowe ORAZ "wyrazy" zawierające niepoprawne znaki.
    Jako argument przyjmuje łańcuch i zwraca listę z oczekiwanymi wyrazami."""
    # wykorzystuję wyrażenia regularne - lepiej się nie da :) przy okazji wykorzystuję locals(), by łatwo dostać się do potrzebnej zmiennej
    if how_many is None:
        how_many = SETTINGS.get('HOW_MANY')
    if min_length is None:
        min_length = SETTINGS.get('MIN_LENGTH')
    pattern = re.compile(r"\b[a-zA-Z]{%(min_length)d,}\b" % locals())
    result = re.findall(pattern, words)
    if len(result) >= how_many:
        return result
    else:
        raise NotEnoughCorrectWordsError, "Plik zawiera za mało poprawnych wyrazów (potrzeba co najmniej %(needed)d, otrzymano %(got)d)" % {'needed':how_many, 'got': len(result)}

def get_random_words(wordlist, how_many=None):
    """Losuje kilka elementów z listy i zwraca jako listę."""
    if how_many is None:
        how_many = SETTINGS.get('HOW_MANY')
    if len(wordlist)>=how_many:
        return random.sample(wordlist,how_many)
    else:
        raise NotEnoughWordsError, "Za mało wyrazów. Potrzeba co najmniej %(needed)d, otrzymano %(got)d." % {'needed': how_many, 'got': len(wordlist)}
        # ten wyjątek normalnie nie powinien nigdy zostać zgłoszony w trakcie działania programu
        # powód jest prosty: zbyt mała liczba wyrazów zostanie wcześniej wyłapana w funkcji get_words :)

def find_intersections(wordlist):
    """Znajduje część wspólną w wyrazach podanych poprzez listę i zwraca jako listę."""
    data = [set(word.lower()) for word in wordlist] # korzystam z listy składanej - zamieniam każdy wyraz na małe litery, przerabiam na zbiór i każdy ze zbiorów wrzucam jako element listy
    return list(set.intersection(*data)) # zwraca listę elementów należących do części wspólnej zbiorów rozpakowanych z listy :)

def do_your_business():
    path = get_path()
    content = get_file_content(path)
    words = get_words(content)
    randwords = get_random_words(words)
    result = find_intersections(randwords)

    print "*** Oto wylosowane wyrazy: "
    for word in randwords:
        print(word)
    if len(result)>0:
        print "*** Część wspólna: "
        for letter in result:
            print(letter)
    else:
        print "Wyrazy nie mają części wspólnej"

def main():
    try:
        do_your_business()
    except IOError:
        print "Błąd otwarcia pliku"
    except Exception, e:
        print e

# HERE BE DRAGONS

class TestWarmup(unittest.TestCase):
    """Klasa zawiera wyłącznie testy funkcji nie związanych z IO."""
    def test_get_words(self):
        self.assertRaises(TypeError, get_words)

        test_input = "1 ala Ala ma kot h1"
        expected_result = []
        self.assertListEqual(get_words(test_input, min_length=4, how_many=0), expected_result)

        test_input = "NIkto 1 ala Aleksandra ma kota h1123123 234234"
        expected_result = ['NIkto', 'Aleksandra', 'kota']
        self.assertListEqual(get_words(test_input, min_length=4, how_many=0), expected_result)

        test_input = "1 ala Aleksandra ma kota h1"
        self.assertRaises(NotEnoughCorrectWordsError, get_words, words=test_input,min_length=4, how_many=4)

    def test_get_random_words(self):
        self.assertRaises(TypeError, get_random_words)

        test_input = ["Ala", 'ma', 'fajnego', 'kota']
        self.assertListEqual(sorted(get_random_words(test_input, how_many=4)), sorted(test_input))
        # sortowanie obu list jest konieczne ze względu na losową kolejność elementów w wyniku
        # zamiast tego można by ewentualnie zamienić listy na zbiory i porównać

        test_input = ["Ala", 'ma', 'kota']
        self.assertRaises(NotEnoughWordsError, get_random_words, wordlist=test_input, how_many=4)

    def test_find_intersections(self):
        self.assertRaises(TypeError, find_intersections)

        test_input = ["Ala", "Agi"]
        expected_result = ['a']
        self.assertListEqual(find_intersections(test_input), expected_result)

        test_input = ["Jurek", "Ala", "Ola"]
        expected_result = []
        self.assertListEqual(find_intersections(test_input), expected_result)

# Beam me up, Scotty

if __name__ == '__main__':
    main()
