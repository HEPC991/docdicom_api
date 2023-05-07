import os

os.system("python -m virtualenv env")
os.system(os.path.join(os.getcwd(), "env", "Scripts", "activate"))
os.system("pip install -r requirements.txt")
