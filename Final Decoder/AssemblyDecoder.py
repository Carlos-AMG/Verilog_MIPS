import json
import sys

instruction_list = []
J_file = open("instructions.json")
full_instructions = json.load(J_file)
typeR_insts = full_instructions["typeR"]
typeI_insts = full_instructions["typeI"]
typeJ_inst = full_instructions["typeJ"]

instruction = ""
current_inst = ""
# leemos las instrucciones, las traducimos a binario y las almacenamos en una lista
with open("instrucciones.txt", "r") as file:
    for line in file:
        binary_list = []
        broken = False
        if line != "\n":
            for word in line.split():
                if word[0:2] == "//" and (len(binary_list) != 0 or current_inst == "nop"):
                    break
                elif word[0:2] == "//" and len(binary_list) == 0:
                    broken = True
                    break
                elif word in full_instructions["typeR"]:
                    current_inst = word
                    instruction = typeR_insts[word]
                elif word in full_instructions["typeI"]:
                    current_inst = word
                    instruction = typeI_insts[word]
                elif word in full_instructions["typeJ"]:
                    current_inst = word
                    instruction = typeJ_inst[word]
                else:
                    if word[0] == "$" and current_inst == "j":
                        try:
                            decimal_form = int(word.replace("$", ""))
                            binary_form = bin(decimal_form).replace("0b", "")
                            binary_number = ""
                            for x in range(0, 26 - len(binary_form)):
                                binary_number += "0"
                            binary_number += binary_form
                            binary_list.append(binary_number)
                        except ValueError:
                            print("Error de sintaxis en el lenguaje ensamblador, por favor intente de nuevo")
                            sys.exit()
                    elif word[0] == "$":
                        try:
                            decimal_form = int(word.replace("$", ""))
                            binary_form = bin(decimal_form).replace("0b", "")
                            binary_number = ""
                            for x in range(0, 5 - len(binary_form)):
                                binary_number += "0"
                            binary_number += binary_form
                            binary_list.append(binary_number)
                        except ValueError:
                            print("Error de sintaxis en el lenguaje ensamblador, por favor intente de nuevo")
                            sys.exit()
                    elif word[0] == "#":
                        try:
                            decimal_form = int(word.replace("#", ""))
                            binary_form = bin(decimal_form).replace("0b", "")
                            binary_number = ""
                            for x in range(0, 16 - len(binary_form)):
                                binary_number += "0"
                            binary_number += binary_form
                            binary_list.append(binary_number)
                        except ValueError:
                            print("Error de sintaxis en el lenguaje ensamblador, por favor intente de nuevo")
                            sys.exit()
                    elif current_inst in typeR_insts:
                        try:
                            decimal_form = int(word)
                            binary_form = bin(decimal_form).replace("0b", "")
                            binary_number = ""
                            for x in range(0, 5 - len(binary_form)):
                                binary_number += "0"
                            binary_number += binary_form
                            binary_list.append(binary_number)
                        except ValueError:
                            print("Error de sintaxis en el lenguaje ensamblador, por favor intente de nuevo")
                            sys.exit()
                    elif current_inst in typeI_insts:
                        try:
                            decimal_form = int(word)
                            binary_form = bin(decimal_form).replace("0b", "")
                            binary_number = ""
                            for x in range(0, 16 - len(binary_form)):
                                binary_number += "0"
                            binary_number += binary_form
                            binary_list.append(binary_number)
                        except ValueError:
                            print("Error de sintaxis en el lenguaje ensamblador, por favor intente de nuevo")
                            sys.exit()
                    elif current_inst in typeJ_inst:
                        try:
                            decimal_form = int(word)
                            binary_form = bin(decimal_form).replace("0b", "")
                            binary_number = ""
                            for x in range(0, 26 - len(binary_form)):
                                binary_number += "0"
                            binary_number += binary_form
                            binary_list.append(binary_number)
                        except ValueError:
                            print("Error de sintaxis en el lenguaje ensamblador, por favor intente de nuevo")
                            sys.exit()
            if broken:
                continue
            elif current_inst in typeR_insts:
                if current_inst == "nop":
                    decoded = "00000000000000000000000000000000"
                else:
                    decoded = instruction[0:6] + binary_list[1] + binary_list[2] + binary_list[0] + "00000"
                    decoded += instruction[7:]
            elif current_inst in typeI_insts:
                if current_inst == "sw" or current_inst == "lw":
                    decoded = instruction[0:6] + binary_list[1] + binary_list[0] + binary_list[2]
                elif current_inst == "beq":
                    decoded = instruction[0:6] + binary_list[0] + binary_list[1] + binary_list[2]
                else:
                    decoded = instruction[0:6] + binary_list[1] + binary_list[0] + binary_list[2]
            elif current_inst in typeJ_inst:  # pendiente en esta
                decoded = instruction[0:6]
                decoded += binary_list[0]
            instruction_list.append(decoded)
    print(instruction_list)
    file.close()

# escribimos el archivo mem
with open("decoded.mem", "w") as write_file:
    counter = 0
    decoded_instruction = ""
    for instruction in instruction_list:
        eof_counter = 0
        for bit in instruction:
            counter += 1
            if counter < 8:
                decoded_instruction += bit
            else:
                decoded_instruction += bit
                write_file.write(decoded_instruction + "\n")
                counter = 0
                # print(decoded_instruction)
                decoded_instruction = ""
write_file.close()

# leemos y sobreescribimos para eliminar una linea vacia
with open("decoded.mem", "r") as f:
    data = f.read()
    with open("decoded.mem", "w") as w:
        w.write(data[:-1])
        w.close()
    f.close()
