#coding: utf-8
"""Program zrobiony w stylu zbliżonym do overarchitectured.
Pominięto definicje specjalistycznych typów danych - typy wbudowane w Pythona zupełnie wystarczają.

Podejście pierwsze.

Korzysta z wyrażeń regularnych i wyjątków.

Na końcu zaweria unittesty dla najważniejszych funkcji.

ZNANE BŁĘDY:
- Wyrazy nie mogą zawierać polskich liter.

Jak testować:
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

def get_path():
	"""Pobiera od użytkownika ścieżkę pliku tekstowego.
	Łatwo można zmienić sposób podawania pliku."""
	return raw_input("Podaj ścieżkę dostępu: ")

def get_file_content(path=None):
	"""Wczytuje plik i zwraca jego zawartość w postaci łańcucha"""
	if os.path.exists(path):
		if os.path.isfile(path):
			return open(path).read()
		else:
			raise NotAFileError, "Podany zasób nie jest plikiem"
	else:
		raise FilePathError, "Nieprawidłowa ścieżka"

def get_words(words=None, min_length=4, how_many=4):
	"""Usuwa słowa krótsze niż czteroliterowe ORAZ "wyrazy" zawierające niepoprawne znaki.
	Jako argument przyjmuje łańcuch i zwraca listę z oczekiwanymi wyrazami."""
	pattern = re.compile(r"\b[a-zA-Z]{%d,}\b" % min_length) # wykorzystuję wyrażenia regularne - lepiej się nie da :)
	result = re.findall(pattern, words)
	if len(result) >= how_many:
		return result
	else:
		raise NotEnoughCorrectWordsError, "Plik zawiera za mało poprawnych wyrazów \
			(potrzeba co najmniej %(needed)d, otrzymano %(got)d)" % {'needed':how_many, 'got': len(result)}

def get_random_words(wordlist=None, how_many=4):
	"""Losuje kilka elementów z listy i zwraca jako listę"""
	if len(wordlist)>=how_many:
		return random.sample(wordlist,how_many)
	else:
		raise NotEnoughWordsError, "Za mało wyrazów. Potrzeba co najmniej %(needed)d, \
			otrzymano %(got)d." % {'needed': how_many, 'got': len(wordlist)}
		# ten wyjątek normalnie nie powinien nigdy zostać zgłoszony w trakcie działania programu
		# powód jest prosty: zbyt mała liczba wyrazów zostanie wcześniej wyłapana w funkcji get_words :)


def find_intersections(wordlist=None):
	"""Znajduje część wspólną w wyrazach podanych poprzez listę i zwraca jako zbiór"""
	data = [set(word.lower()) for word in wordlist] # korzystam z listy składanej
	return list(set.intersection(*data)) # zwraca listę zrobioną na podstawie zestawu zrobionego na podstawie rozpakowanej listy

def do_your_business():
	path = get_path()
	content = get_file_content(path)
	words = get_words(content)
	randwords = get_random_words(words)
	print "*** Oto wylosowane wyrazy: "
	for word in randwords:
		print(word)
	result = find_intersections(randwords)
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
		test_input = "1 ala Ala ma kot h1"
		expected_result = []
		self.assertListEqual(get_words(test_input, min_length=4, how_many=0), expected_result)

		test_input = "NIkto 1 ala Aleksandra ma kota h1123123 234234"
		expected_result = ['NIkto', 'Aleksandra', 'kota']
		self.assertListEqual(get_words(test_input, min_length=4, how_many=0), expected_result)

		test_input = "1 ala Aleksandra ma kota h1"
		self.assertRaises(NotEnoughCorrectWordsError, get_words, words=test_input,length=4, how_many=4)

	def test_get_random_words(self):
		test_input = ["Ala", 'ma', 'fajnego', 'kota']
		self.assertListEqual(sorted(get_random_words(test_input, how_many=4)), sorted(test_input))

		test_input = ["Ala", 'ma', 'kota']
		self.assertRaises(NotEnoughWordsError, get_random_words, wordlist=test_input, how_many=4)

	def test_find_intersections(self):
		test_input = ["Ala", "Agi"]
		expected_result = ['a']
		self.assertListEqual(find_intersections(test_input), expected_result)

		test_input = ["Jurek", "Ala", "Ola"]
		expected_result = []
		self.assertListEqual(find_intersections(test_input), expected_result)

# Beam me up, Scotty

if __name__ == '__main__':
	main()
