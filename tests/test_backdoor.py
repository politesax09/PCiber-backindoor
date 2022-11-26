from backdoor import Backdoor


b1 = Backdoor('back1')
b1.type = 'tipo'
b1.target_ip = 12345
b1.save_backdoor()
b1.get_backdoor()
b1.print_backdoorclass()