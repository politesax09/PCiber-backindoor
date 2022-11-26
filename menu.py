# - OPCIONES INICIALES:
#   -- DESPLEGAR BACKDOOR:
#       --- SELECCIONAR MODULO
#       --- CONFIGURAR MODULO
#       --- LISTAR MODULOS DISPONIBLES

#   -- DESPLEGAR 2 TECNICAS DE PERSISTENCIA PARAMETRIZADAS

#   -- LISTAR PERSISTENCIAS ACTIVAS

#   -- MONITORIZAR PERSISTENCIA ACTIVA

from backdoor import Backdoor, get_saved_backdoors
from msf import Msf


def menu():

    msf = Msf()
    backdoor = Backdoor(None)

    while (True):
        print('\n\nBienvenido a B4ckInD00r\n\
Opnciones: \n \
\t> deploy\t[[Despliega una nueva backdoor]]\n \
\t> list\t[[Lista las backdoors activas]]\n\
\t> select <backdoor_name>\t[[Selecciona una backdoor activa]]\n\
\t> exit\t[[Salir]]\n')

        op = input('>>>   ').strip().lower()
        ops = []

        if (' ' in op):
            delim = op.index(' ')
            ops.append(op[:delim].strip())
            ops.append(op[delim+1:].strip())
        else:
            ops.append(op)

        if (ops[0] == 'exit'):
            break

        elif (ops[0] == 'deploy'):
            print('Desplegar nueva backdoor\n')
            name = input('Ponle nombre >>>   ').strip().lower()

            backdoor.name = name
            backdoor.status = 'created'

            while (True):

                print('\nOpciones:\n\
            > select <module_name || module_num>  [[Selecciona un modulo]]\n\
            > config    [[Configura el modulo seleccionado]]\n\
            > list  [[Lista los modulos disponibles]]\n\
            > back  [[Atras]]\n')

                op = input('>>>   ').strip().lower()

                # TODO: Configurar variables sin entrar en 'config' como en MSF

                ops.clear()
                if (' ' in op):
                    delim = op.index(' ')
                    ops.append(op[:delim].strip())
                    ops.append(op[delim+1:].strip())
                else:
                    ops.append(op)

                if (ops[0] == 'select'):
                    modules_list = msf.get_modules()

                    if (len(ops) > 1):
                        if (len(ops[1]) < 4):
                            if (int(ops[1]) < len(modules_list)):
                                backdoor.modules.append({'id': 'post/' + modules_list[int(ops[1])], 'tool': 'msf'})
                                print('Seleccionado modulo ' + modules_list[int(ops[1])])
                            else:
                                print('-- ERROR: El numero del modulo seleccionado no es correcto')
                        else:
                            if (ops[1] in modules_list):
                                backdoor.modules.append({'id': 'post/' + ops[1], 'tool': 'msf'})
                                print('Seleccionado modulo ' + ops[1])
                            else:
                                print('-- ERROR: El modulo seleccionado no es correcto')
                    else:
                        print('-- ERROR: Se debe indicar el modulo seleccionado')
                    
                    # TODO: DECIDIR Se puede escribir backdoor en DB en este punto aunque no este rellena
                    

                elif (ops[0] == 'config'):
                    print('Configuracion de ' + str(backdoor.name) + ':')

                    if (len(backdoor.modules) > 0):
                        module = msf.select_module(backdoor.modules[0]['id'])
                        config_missing = msf.get_missing_required(module)
                        for item in config_missing:
                            if (item == 'SESSION'):
                                print(item)
                    else: print('ERROR: No hay modulos seleccionados')


                    # op_target_ip = input('target_ip [' + str(backdoor.target_ip) + '] -> ')
                    # op_attacker_ip = input('attacker_ip [' + str(backdoor.attacker_ip) + '] -> ')
                    # op_payload_url = input('target_ip [' + str(backdoor.payload_url) + '] -> ')

                    # if (op_target_ip == ''):
                    #     backdoor.target_ip = None
                    # else: backdoor.target_ip = op_target_ip
                    # if (op_attacker_ip == ''):
                    #     backdoor.attacker_ip = '127.0.0.1'
                    # else: backdoor.attacker_ip = op_attacker_ip
                    # if (op_payload_url == ''):
                    #     backdoor.payload_url = None
                    # else: backdoor.payload_url = op_payload_url
                        


                elif (ops[0] == 'list'):
                    # TODO: DECIDIR De momento solo lista los modulos 'post', no se si parametrizar para listar por tipo o que se pueda elegir el tipo
                    modules_list = msf.get_modules()
                    i = 0
                    for module in modules_list:
                        i += 1
                        print(i, ' -> ', module)
                

                # elif (ops[0] == 'run'):

                

                elif (ops[0] == 'back'):
                    break

                else: print('-- ERROR: El comando no existe')


        elif (ops[0] == 'list'):
        # TODO: MEJORAR PRESENTACION DE LOS DATOS DE BACKDOORS
            print('Backdoors activas:\n')
            backdoors = get_saved_backdoors()
            for bdoor in backdoors:
                bdoor.print_backdoorclass()
                print()


        elif (ops[0] == 'select'):
            if (len(ops) > 1):
                backdoors = get_saved_backdoors()
                for bdoor in backdoors:
                    if (ops[1] == bdoor.name):
                        backdoor = bdoor
                        break
                if backdoor.name != None:
                    print('Seleccionada ' + backdoor.name)
                else:
                    print('La backdoor seleccionada no existe')

            else: print('-- ERROR: Debes seleccionar una backdoor disponible')

        # else: print('Error:')



menu()