def getInput(ciphers):
	"""
	Gets input from the user about whether they would like to continue on to the next cipher,
	Guess more words with the current cipher,
	Or finish crib dragging
	"""
	if len(ciphers) > 1:
		userInput = input('Would you like to continue with this cipher (Y) or move to the next (N)?: ')
	else:
		userInput = input('Would you like to continue (Y) or return original ciphers (N): ')
	
	while userInput != 'Y' and userInput != 'N':
		userInput = input('Please choose Y or N: ')
	return(userInput)

def nextGuessWord():
	userInput = input('Choose Next Guess Word: ')
	return(userInput)

def createXORCiphers(ciphertexts):
	"""
		This takes all ciphertexts, and XOR's them with all other Ciphertexts.
		Returns a list of all combinations of ciphertexts and the combinations reference ciphers
	"""
	xorCiphertexts = []
	referenceXOR = []

	#for every cipher, 
	while len(ciphertexts) > 0:
		#convert cipher to byte array
		original1 = ciphertexts[0]
		message1 = []
		conversion = bytes.fromhex(ciphertexts[0])
		[message1.append(x) for x in conversion]
			
		#Remove so it doesn't compare with itself, and isn't compared with again in future iterations
		ciphertexts.remove(ciphertexts[0])

		#compare to every other cipher
		for cipher in ciphertexts:
			original2 = cipher
			message2 = []
			conversion = bytes.fromhex(cipher)
			[message2.append(x) for x in conversion]
			#XOR together and append to a list			
			ciphertextxor = []
			[ciphertextxor.append(x ^ y) for x, y in zip(message1, message2)]

			referenceXOR.append([original1, original2])
			xorCiphertexts.append(ciphertextxor)

	return(xorCiphertexts, referenceXOR)

def convertToInt(s):
    guessword = []
    [guessword.append(ord(char)) for char in s]
   
    return(guessword)

def CribDragging(cipher, guessWord):
	"""
		Takes the guess word and the ciphertext and drags the guess words across the cipher
		returns the xor of the guess word with all combinations of the cipher possible
		removes guesses which contain unprintable characters
	"""
	guessWord = convertToInt(guessWord)
	cipherguesses = []

	#XOR the guess word with all locations of the cipher combination
	for i in range(0, len(cipher)):	
		cipherSection = cipher[i:i+len(guessWord)]
		cipherGuess = []

		[cipherGuess.append(x ^ y) for x, y in zip(cipherSection, guessWord)]

		for i in range(0, len(cipherGuess)):
			cipherGuess[i] = chr(cipherGuess[i])
			#if characters are not printable, delete
			if cipherGuess[i] not in list(string.printable):
				del cipherGuess[i]
				break
		#if there are deletted characters, don't append.
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
	ciphercombinations = createXORCiphers(ciphertexts)
	xorCiphertexts = ciphercombinations[0]
	xorReference = ciphercombinations[1]

	guessword = ''
	
	#While still recieving new words
	while guessword != False:
		#start with the first cipher combination, and iterate through all 
		cipher = 0
		continueWithCipher = ''
		guessword = nextGuessWord()
		
		#if quitting before first iteration
		if guessword == False:
			break
		
		# while continuing through combinations of ciphers
		while cipher < len(xorCiphertexts):

			#cribdrag with the current cipher and given guess word 
			cipherguesses = CribDragging(xorCiphertexts[cipher], guessword)
			if cipherguesses != None:
				print('Cipher Combination {} in use'.format(cipher + 1))
				print(cipherguesses)
				continueWithCipher = getInput(xorCiphertexts)

			#if a cipher is chosen, continue only with that cipher
			if continueWithCipher == 'Y':
				xorCiphertexts = [xorCiphertexts[cipher]]
				cipherReference = cipher
				break
			#If the user does not want to continue, and only has one combination exit.
			elif continueWithCipher == 'N' and len(xorCiphertexts) == 1:
				#print(continueWithCipher)
				guessword = False
				break

			cipher = cipher +1
	
	#print original ciphertexts
	if len(xorCiphertexts) == 1:
		print('cipher 1: {}'.format(xorReference[cipherReference][0]))

		print('cipher 2: {}'.format(xorReference[cipherReference][1]))	