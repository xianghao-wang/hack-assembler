import re

JMP_CODES = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

COMP_CODES = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000', 'M': '110000',
    '!D': '001101',
    '!A': '110011', '!M': '110011',
    '-D': '001111',
    '-A': '110011', '-M': '110011',
    'D+1': '011111',
    'A+1': '110111', 'M+1': '110111',
    'D-1': '001110',
    'A-1': '110010', 'M-1': '110010',
    'D+A': '000010', 'D+M': '000010',
    'D-A': '010010', 'D-M': '010010',
    'A-D': '000111', 'M-D': '000111',
    'D&A': '000000', 'D&M': '000000',
    'D|A': '010101', 'D|M': '010101'
}


# remove all white characters and comments
def purify(line: str):
    pattern = '\\s|(//.*)'
    return re.sub(pattern, '', line)


# assemble A instruction
def asm_a(instruction: str):
    addr = int(instruction[1:])
    return '0' + bin(addr)[2:].zfill(15)


# assemble C instruction
def asm_c(instruction: str):
    des, jump = '', ''
    if '=' in instruction:
        pieces = instruction.split('=')
        des, instruction = pieces[0], pieces[1]

    if ';' in instruction:
        pieces = instruction.split(';')
        instruction, jump = pieces[0], pieces[1]

    comp = instruction

    # analyse destination
    des_code = ''.join(['1' if item in des else '0' for item in 'ADM'])

    # analyse jump
    jump_code = JMP_CODES[jump] if jump in JMP_CODES else '000'

    # analyse comp
    comp_code = ('1' if 'M' in comp else '0') + COMP_CODES[comp]

    return '111' + comp_code + des_code + jump_code


def test(source, dest):
    with open(source) as f, open(dest, 'w') as g:
        for line in f:
            line = purify(line)
            if len(line) == 0:
                continue
            if '@' in line:
                g.write(asm_a(line) + '\n')
            else:
                g.write(asm_c(line) + '\n')


if __name__ == '__main__':
    test('test.asm', 'test.hack')
