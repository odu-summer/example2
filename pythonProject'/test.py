
import sys
from collections import Counter

if __name__ == '__main__':
	
	words = sys.argv[0:]
	print(type(words))
	word_count = Counter(words)

	print(word_count)

