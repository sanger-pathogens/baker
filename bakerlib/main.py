
from bakerlib.softwares import get_softwares

def bake(input_dirs, output_dir):
	softwares = get_softwares(input_dirs)
	print("I am baking", output_dir, input_dirs)
	print("I have loaded ", softwares)
	return softwares
