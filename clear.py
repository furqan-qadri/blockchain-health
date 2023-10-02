from pyteal import *

def clear_program():
    return Return(Int(1))

if __name__ == "__main__":
    with open("clear_program.teal", "w") as f:
        compiled = compileTeal(clear_program(), mode=Mode.Application)
        f.write(compiled)
