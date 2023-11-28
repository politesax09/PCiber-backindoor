# Guardar directorio HOME del usuario
import os
import paramiko

home_dir = os.environ['HOME']
# Generar una nueva clave SSH
private_key = paramiko.RSAKey.generate(2048)
# Guardar la clave privada en un archivo
private_key.write_private_key_file(home_dir + '/.ssh/bid0_key')

# Guardar la clave pública en un archivo
with open(home_dir + '/.ssh/bid0_key.pub', 'w') as file:
    file.write(f'{private_key.get_name()} {private_key.get_base64()}')
    print(os.path.basename(file.name))
print('COOL: Clave SSH generada exitosamente.')