import subprocess,sys
def check_new_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install",'-r','.\\files\\requirements.txt'])
