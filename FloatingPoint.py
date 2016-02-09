# Performs a multiplication using 2 Floating Point Numbers 
# represented in IEEE 754 standard format.


DEBUG = 0

	 #S| Expo ||       Manti         |
	 #01234567890123456789012345678901
n1 = "01000000000101100110011001100110" #2.35
n2 = "00111111111111111101111100111011" #1.999
#n1 = "10000000000000000000010101000101"
#n2 = "11011111100000000000010101000101"
#n1 = "10001000011110010101010101000101"   # (-1)(16)()
#n2 = "00001000000110010101010101000101"   # 


def get_man_exp(num):
	manh_dec = 0
	manl_dec = 0
	exp_dec = 0

	sig = num[0]
	exp = num[1:9]
	
	man = num[9:]
	manh = "1" + man[:7]
	manl = man[7:]

	for i in range(len(manh)):
		if manh[i] == "1":
			manh_dec = (manh_dec << 1) | 1
		else:
			manh_dec = manh_dec << 1

	for i in range(len(manl)):
		if manl[i] == "1":
			manl_dec = (manl_dec << 1) | 1
		else:
			manl_dec = manl_dec << 1

	
	for i in range(len(exp)):
		if exp[i] == "1":
			exp_dec = (exp_dec << 1) | 1
		else:
			exp_dec = exp_dec << 1	
	exp_dec = exp_dec - 127				# Get exponent (-127 to 128)


	n = [sig, exp_dec, manh_dec, manl_dec]

	if DEBUG:
		n_debug = [sig, exp, manh, manl]
		print n_debug

	return n

def mult_man(n1, n2):
	mll = n1[3] * n2[3]
	mlh = (n1[3] * n2[2]) << 16
	mhl = (n1[2] * n2[3]) << 16
	mhh = (n1[2] * n2[2]) << 32

	if DEBUG:
		print "mll:", bin(mll)
		print "mlh:", bin(mlh)
		print "mhl:", bin(mhl)
		print "mhh:", bin(mhh)

	m = bin(mll + mlh + mhl + mhh)
	mm = m[3:] # Eliminates the 0b and the first "1"

	temp = 23-len(mm)
	if temp < 0:
		temp = 0
	result = "0" * temp
	result = result + mm[:23]

	return result

def mult_exp(n1,n2):
	flag = 0
	exp1 = int(n1[1])
	exp2 = int(n2[1])

	r = 127 + exp1 + exp2

	e = bin(r)
	ee = e[2:]

	temp = 8 - len(ee)
	if temp < 0:
		temp = 0
	result = "0" * temp
	result = result + ee[:8-temp]

	return result

def mult_sig(n1, n2):
	s1 = int(n1[0])
	s2 = int(n2[0])

	return str(s1^s2)


# Get Sign, exponent and mantissa as a list of strings
num1 = get_man_exp(n1)
num2 = get_man_exp(n2)

# Multiply mantissas and get result
m_mantissa = mult_man(num1, num2)
#print "012345678901234567890123456789012345678901234567"
print "Resultado de la mantisa:", m_mantissa

# Exponent operations
m_exponent = mult_exp(num1, num2)
print "Resultado del exponente:", m_exponent

# Sign operation
m_sign = mult_sig(num1, num2)
print "Resultado del signo:", m_sign

# Final result
print ""
print "bits:   01234567890123456789012345678901"
r = "Result: " + m_sign + m_exponent + m_mantissa
print r
print ""
