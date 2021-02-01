from django.shortcuts import render, redirect
import random


STATES = [
	['RS'],
	['DF', 'GO', 'MS', 'MT', 'TO'],
	['AC', 'AM', 'AP', 'PA', 'RO', 'RR'],
	['CE', 'MA', 'PI'],
	['AL', 'PB', 'PE', 'RN'],
	['BA', 'SE'],
	['MG'],
	['ES', 'RJ'],
	['SP'], 
	['PR', 'SC']
]


def check_digits(primary_cpf):
	v_digits = []

	# Calculate the 2 check digits using the first 9 digits
	for i in range(2):
		position  = 10 + i
		result = 0

		for digit in primary_cpf:
			result += int(digit) * position
			position -= 1

		digit = str((result*10) % 11 % 10)

		v_digits.append(digit)
		primary_cpf += digit

	return v_digits


def format_cpf(num_cpf):
	return f"{num_cpf[:3]}.{num_cpf[3:6]}.{num_cpf[6:9]}-{num_cpf[9:]}"


def home(request):
	return redirect('explanation')


def explanation(request):
	return render(request, "application/explanation.html")


def generator(request):
	return render(request, "application/generator.html")


def validator(request):
	return render(request, "application/validator.html")


def generate_cpf(request):
	if request.method == 'GET':
		return redirect('generator')

	cpfs = {}
	quantity = int(request.POST['quantity'])
	state = request.POST['state'] if request.POST['state'] != 'Indiferete' else False
	state_digit = False

	if state:
		for index, states in enumerate(STATES):
			if state in states:
				state_digit = str(index)
				break

	
	for _ in range(quantity):
		if state_digit:
			primary_cpf = ''.join([str(random.randint(0, 9)) for _ in range(8)]) + state_digit
		else:
			primary_cpf = ''.join([str(random.randint(0, 9)) for _ in range(9)])

		if primary_cpf in cpfs:
			continue

		num_cpf = primary_cpf + ''.join(check_digits(primary_cpf))
		cpfs[num_cpf] = format_cpf(num_cpf)

	context = {
		'quantity': quantity,
		'state': state,
		'cpfs': cpfs.items(),
	}
	
	return render(request, "application/generator_results.html", context)


def validate_cpf(request):
	if request.method == 'GET':
		return redirect('validator')

	num_cpf = request.POST['cpf'].replace('.', '').replace('-', '')
	f_cpf = format_cpf(num_cpf)
	all_equal = num_cpf[:-2] == num_cpf[0]*(len(num_cpf)-2)

	if all_equal:
		context = {
			'num_cpf': num_cpf,
			'f_cpf': f_cpf,
			'all_equal': all_equal,
			'valid': False,
		}

	else:
		primary_cpf = num_cpf[:9]
		state = ' ou '.join(STATES[int(num_cpf[8])])
		v_digits = check_digits(primary_cpf)
		new_cpf = format_cpf(primary_cpf+''.join(v_digits))
		valid = v_digits == [num_cpf[9], num_cpf[10]]

		context = {
			'num_cpf': num_cpf,
			'f_cpf': f_cpf,
			'new_cpf': new_cpf,
			'state': state,
			'valid': valid,
			'all_equal': all_equal
		}

	return render(request, "application/validator_results.html", context)
