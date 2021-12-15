import re

# codes for jump condition
JMP_CODES = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

# codes for computation
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

MEMORY_BEGIN = 32  # the begin of free memory address


# remove all white characters and comments and white lines
def purify(lines: [str]):
    pattern = '\\s|(//.*)'
    return list(filter(lambda item: len(item) != 0, [
        re.sub(pattern, '', item) for item in lines
    ]))


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


# analyse codes to replace symbols with actual values
def analyse(lines: [str]):
    line_count = 0
    addr = MEMORY_BEGIN
    symbols = {}
    # scan for find symbols
    for line in lines:
        if line[0] == '(' and line[-1] == ')':  # detect a label
            symbols[line[1:-1]] = line_count
            continue

        if line[0] == '@' and not line[1:].isdigit() and line[1:] not in symbols:  # detect a variable
            symbols[line[1:]] = addr
            addr += 1
        line_count += 1

    # scan for replacing symbol with address
    return [
        f'@{symbols[line[1:]]}' if line[0] == '@' else line
        for line in lines if '(' not in line
    ]


# assemble to machine codes
def assemble(lines: [str]):
    return [
        asm_a(line) if line[0] == '@' else asm_c(line)
        for line in lines
    ]


def test(source, dest):
    with open(source) as fin, open(dest, 'w') as fout:
        lines = analyse(purify(list(fin)))
        for line in lines:
            fout.write(line + '\n')


if __name__ == '__main__':
    test('test.asm', 'test.o')
