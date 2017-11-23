def getUserInput():
	userInput = input('Would you like to continue with this cipher (Y) or move to the next (N)?: ')
	while userInput != 'Y' and userInput != 'N':
		userInput = input('Please choose Y or N: ')
	return(userInput)

def nextGuessWord():
	userInput = input('Choose Next Guess Word (Press enter to quit): ')
	if userInput is '':
		userInput = False
	return(userInput)

def createXORCiphers(ciphertexts):
	"""
		This takes all ciphertexts, and XOR's them with all other Ciphertexts.
		Returns a list of all combinations of ciphertexts
	"""
	xorCiphertexts = []

	#for every cipher, 
	for cipher in ciphertexts:
		#convert cipher to byte array
		message1 = []
		conversion = bytes.fromhex(cipher)
		[message1.append(x) for x in conversion]
			
		#Remove so it doesn't compare with itself, and isn't compared with again in future iterations
		ciphertexts.remove(cipher)

		#compare to every other cipher
		for cipher in ciphertexts:
			message2 = []
			conversion = bytes.fromhex(cipher)
			[message2.append(x) for x in conversion]
			
			ciphertextxor = []
			[ciphertextxor.append(x ^ y) for x, y in zip(message1, message2)]

			#XOR together and append to a list
			xorCiphertexts.append((ciphertextxor))

	return(xorCiphertexts)

def convert_to_int(s):
    guessword = []
    [guessword.append(ord(c)) for c in s]
   
    return(guessword)

def CribDragging(cipher, guessWord):
	"""
		Takes the guess word and the ciphertext and drags the guess words across the cipher
		returns the xor of the guess word with all combinations of the cipher possible
		removes guesses which contain unprintable characters
	"""
	guessWord = convert_to_int(guessWord) #121
	cipherguesses = []

	#XOR the guess word with all locations of the cipher combination
	for i in range(0, len(cipher)):	
		cipherSection = cipher[i:i+len(guessWord)]
		cipherGuess = []

		[cipherGuess.append(x ^ y) for x, y in zip(cipherSection, guessWord)]

		for i in range(0, len(cipherGuess)):
			cipherGuess[i] = chr(cipherGuess[i])
			if cipherGuess[i] not in list(string.printable):
				del cipherGuess[i]
				break
			
		if len(cipherGuess) >= len(guessWord):
				cipherguesses.append(''.join(cipherGuess))
		
	if len(cipherguesses) > 0:
		return(cipherguesses)


if __name__ == '__main__':
	import sys
	import string

	#Open ciphertexts file and store each cipher as an element in a list
	ciphertexts = [cipher.rstrip('\n') for cipher in open(sys.argv[1], 'r')]
	
	#XOR all ciphertexts together
	xorCiphertexts = createXORCiphers(ciphertexts)

	#For every combination of ciphers
	guessword = ' the '
	
	#While still giving new words
	while guessword != False:
		#start with the first cipher combination, and iterate through all 
		cipher = 0
		continueWithCipher = 'N'
		guessword = nextGuessWord()
		
		#if quitting before first iteration
		if guessword == False:
			break
		
		# while continuing through combinations of ciphers
		while continueWithCipher == 'N' and cipher < len(xorCiphertexts):
			print('Cipher Combination {} in use'.format(cipher + 1))

			#cribdrag with the current cipher and given guess word 
			cipherguesses = CribDragging(xorCiphertexts[cipher], guessword)
			print(cipherguesses)
			continueWithCipher = getUserInput()
			cipher = cipher +1

			#if a cipher is chosen, continue only with that cipher
			if continueWithCipher == 'Y':
				xorCiphertexts = [xorCiphertexts[cipher]]
				break




		

		