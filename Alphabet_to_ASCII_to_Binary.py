# Python 3.8.6 64-bit

ASCII_to_Binary_Conversion_Table = {}
ASCII_to_Binary_Calculation_Process_Table = {}

# Intializing Tables
def ASCII_to_Binary_Conversion_Table_Initialization():
    alphabet = ["#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz'"]
    ascii_dec = [int(i) for i in range(35, 123)]

    ASCII_to_Binary_Conversion_Table[' '] = 32
    ASCII_to_Binary_Conversion_Table['!'] = 33
    ASCII_to_Binary_Conversion_Table['"'] = 34

    for i in range(len(ascii_dec)):
        ASCII_to_Binary_Conversion_Table[alphabet[0][i]] = ascii_dec[i]

def ASCII_to_Binary_Calculation_Table_Initialization(): 
    alphabet = ["#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz'"]
    ascii_dec = [int(i) for i in range(35, 123)]

    ASCII_to_Binary_Calculation_Process_Table[' '] = 32
    ASCII_to_Binary_Calculation_Process_Table['!'] = 33
    ASCII_to_Binary_Calculation_Process_Table['"'] = 34

    for i in range(len(ascii_dec)):
        ASCII_to_Binary_Calculation_Process_Table[alphabet[0][i]] = ascii_dec[i]

ASCII_to_Binary_Conversion_Table_Initialization()
ASCII_to_Binary_Calculation_Table_Initialization()

class Binary_Conversion():

    def ascii_conversion(phrase: str):
        arr = []
        for char_id in range(len(phrase)):
            ascii_num = ASCII_to_Binary_Conversion_Table[phrase[char_id]]
            arr.append(ascii_num)
        return arr

    def binary_conversion(value: int) -> str:
        base_2 = [128, 64, 32, 16, 8, 4, 2, 1]
        binary_arr = ['0', '0', '0', '0', '0', '0', '0', '0']
        val = value
        for num_id in range(len(base_2)):
            if int(val) - base_2[num_id] >= 0:
                binary_arr[num_id] = '1'
                val = str(int(val) - base_2[num_id])
        return ''.join(binary_arr)

    def display_binary(phrase):
        ascii_arr = binary_convert.ascii_conversion(phrase)
        output = []
        for num_id in range(len(ascii_arr)):
            num = ascii_arr[num_id]
            binary = binary_convert.binary_conversion(num)
            output.append(binary)
        print("Binary:", output)
        print("-" * 100)
        binary_calculation.display_calculation(phrase)

class ASCII_to_Binary_Calculation_Process():
    def binary_conversion(value: int) -> str:
        base_2 = [128, 64, 32, 16, 8, 4, 2, 1]
        arr = []
        val = value
        for num_id in range(len(base_2)):
            if int(val) - base_2[num_id] >= 0:
                arr.append("%s - %s = %s" % (val, base_2[num_id], str(int(val) - base_2[num_id])))
                val = str(int(val) - base_2[num_id])
        return arr

    def base2_conversion():
        subtraction_process = {}
        for alphabet, ascii_num in ASCII_to_Binary_Calculation_Process_Table.items():
            subtraction_process[alphabet] = binary_calculation.binary_conversion(ascii_num)
        return subtraction_process

    def display_calculation(phrase):
        process_arr = binary_calculation.base2_conversion()
        for scan_id in range(len(phrase)):
            character = phrase[scan_id]
            print(character + ":", process_arr[character])

binary_convert = Binary_Conversion
binary_calculation = ASCII_to_Binary_Calculation_Process

binary_convert.display_binary(phrase = input("Enter a value: "))


