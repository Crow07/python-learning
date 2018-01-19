
import _main_name_b
#print globals()['__name__']
#print("top-level in two.py")

#_main_name_b.func()
_main_name_b.test()

if __name__ == "__main__":
    print("two.py is being run directly")
else:
    print("two.py is being imported into another module")