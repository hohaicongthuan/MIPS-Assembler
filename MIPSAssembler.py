import re

# Enter paths to input and output files here
INPUT_FILE = '/InputFile.in'
OUTPUT_FILE = '/Outputfile.out'
PC = 0

LABEL = {}
RType = {
			'add': '000000',
			'addu': '000000',
			'and': '000000',
			'jr': '000000'
		}
IType = {
			'addi': '001000',
			'addiu': '001001',
			'andi': '001100',
			'beq': '000100',
			'bne': '000101',
			'lbu': '100100',
			'lhu': '100101',
			'll': '110000',
			'lui': '001111',
			'lw': '100011'
		}
JType = {
			'j': '000010',
			'jal': '000011'
		}

Func = {
			'add': '100000',
			'addu': '100001',
			'and': '100100',
			'jr': '001000',
			'nor': '100111',
			'or': '100101'
		}

REG = 	{
			'$zero': '00000',
			'$v0': '00010',
			'$v1': '00011',
			'$a0': '00100',
			'$a1': '00101',
			'$a2': '00110',
			'$a3': '00111',
			'$t0': '01000',
			'$t1': '01001',
			'$t2': '01010',
			'$t3': '01011',
			'$t4': '01100',
			'$t5': '01101',
			'$t6': '01110',
			'$t7': '01111',
			'$s0': '10000',
			'$s1': '10001',
			'$s2': '10010',
			'$s3': '10011',
			'$s4': '10100',
			'$s5': '10101',
			'$s6': '10110',
			'$s7': '10111',
			'$t8': '11000',
			'$t9': '11001',
			'$gp': '11100',
			'$sp': '11101',
			'$fp': '11110',
			'$ra': '11111'
		}

fin = open(INPUT_FILE, 'r')
fout = open(OUTPUT_FILE, 'w')

for line in fin:
	# Split every word in the line
	words = line.split()
	# Check a word if it's a label
	isLabel = ':' in line
	
	if words[0] in RType:
		#codes
		OpCode = words[0]
		temp = words[1]
		rd = re.sub(',', '', temp)
		temp = words[2]
		rs = re.sub(',', '', temp)
		temp = words[3]
		rt = re.sub(',', '', temp)
		
		inst = RType[OpCode] + REG[rs]
		inst = inst + REG[rt]
		inst = inst + REG[rd]
		inst = inst + '00000'
		inst = inst + Func[OpCode]
		fout.write(hex(int(inst, 2)))
		fout.write('\n')

	elif words[0] in IType:
		#codes
		OpCode = words[0]
		if OpCode == 'lw':		# if it is 'load word'
			temp = words[1]
			rt = re.sub(',', '', temp)
			temp = words[2]
			rs = re.sub(',()', '', temp)
			immediate = int(rs[0])
			immediate = bin(immediate)[2:].zfill(16)
		else:
			temp = words[1]
			rs = re.sub(',', '', temp)
			temp = words[2]
			rt = re.sub(',', '', temp)
			#temp = words[3]
			immediate = ''
			words[3] = re.sub(',', '', words[3])
			inst = IType[OpCode] + REG[rs]
			inst = inst + REG[rt]
		
		if (OpCode != 'lw'):
			if words[3] in LABEL:
				immediate = LABEL[words[3]]
		elif '-' in immediate:
			immediate = int(immediate)
			immediate = abs(immediate)
			immediate = bin(immediate)[2:].zfill(16)
			for i in immediate:
				imme = ''
				if i == '0':
					imme = imme + '1'
				elif i == '1':
					imme = imme + '0'
			immediate = int(imme, 2) + 1
		inst = inst + immediate
		fout.write(hex(int(inst, 2)))
		fout.write('\n')
		
	elif words[0] in JType:
		#codes
		OpCode = words[0]
		if words[1] in LABEL:
			addr = LABEL[words[1]]
		else:
			print("Label doesn't exist")
		inst = JType[OpCode] + bin(LABEL[addr])
		fout.write(hex(int(inst, 2)))	
		fout.write('\n')
	
	if isLabel:
		LABEL[words[0]] = bin(PC)[2:].zfill(16)
	
	PC = PC + 4

fin.close()
fout.close()