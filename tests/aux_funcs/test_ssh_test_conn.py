import subprocess

res = subprocess.run('timeout 5 bash -c "</dev/tcp/192.168.1.43/22"', shell=True, capture_output=True, text=True)
print(res.returncode)