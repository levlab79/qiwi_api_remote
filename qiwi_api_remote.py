##
# The program created by prod.z9L
# YouTube channel: https://www.youtube.com/channel/UCy5bHWLxO3RGqP92AuaOj5A
# My VK Group (for answers): https://vk.com/club185628534
# My Aura: @levlab79
# End date of program development: 13.04.2020
##
# Функция для взаимодействия с QIWI API (они будут обозначены*) я взял с сайта developer.qiwi.com
##

# подключаем библиотеку для получения информации по API
import requests
# подключаем библиотеку для работы с JSON
import json
# подключаем библиотеку для работы с pickle
import pickle
# библиотека для работы с системой
import os
# для перемещения в пространстве-времени
import time
# для рандома
import random

# функция для получения информации о профиле пользователя*


def get_profile(api_access_token):
	# открываем сессию с помощью модуля requests
	s7 = requests.Session()
	s7.headers['Accept'] = 'application/json'
	s7.headers['authorization'] = 'Bearer ' + api_access_token
	p = s7.get(
		'https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true')
	# если ответ успешно получен
	if p.status_code == 200:
		# возвращаем json
		return p.json()
	else:
		# иначе возвращаем False
		return False


# Функция для получения баланса QIWI Кошелька*
# login - это номер телефона
def get_balance(login, api_access_token):
	# открываем сессию с помощью модуля requests
	s = requests.Session()
	s.headers['Accept'] = 'application/json'
	s.headers['authorization'] = 'Bearer ' + api_access_token
	b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' +
			  login + '/accounts')
	# если ответ успешно получен
	if b.status_code == 200:
		# возвращаем json
		return b.json()
	else:
		# иначе возвращаем False
		return False


# функция для получения истории n платежей*
def get_history(my_login, api_access_token, rows_num):
	# открываем сессию с помощью модуля requests (да неужели)
	s = requests.Session()
	s.headers['authorization'] = 'Bearer ' + api_access_token
	parameters = {'rows': rows_num}
	h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' +
			  my_login + '/payments', params=parameters)
	# если ответ успешно получен
	if h.status_code == 200:
		# возвращаем json
		return h.json()
	else:
		# иначе возвращаем False
		return False


# функция для проверки существует ли определенный файл
# mode - определяет режим сохранения: json (текстовый) / pickle (байтовый)
# / False (текстовый)
def SaveInfo(file_name, info, mode=False):
	# определяем режим
	if not mode:
		# открываем файл в режиме записи текста
		with open(file_name, 'wt') as f:
			# записываем в файл нашу информацию
			f.write(info)
	else:
		if mode == 'pickle':
			# с помощью модуля pickle записываем информацию в виде байтов
			# открываем файл в режиме записи байтов
			with open(file_name, 'wb') as f:
				# записываем в файл с помощью pickle
				pickle.dump(info, f)
		elif mode == 'json':
			# с помощью модуля json записываем информацию в виде json-строки
			# т.к. это строка, открываем файл в режиме текстовой записи
			with open(file_name, 'wt') as f:
				# записываем в виде json-строки
				json.load(info, f)


# функция для проверки наличия сохранения
# mode - определяет режим чтения: json (текстовый) / pickle (байтовый) /
# False (текстовый)
def CheckSaving(file_name, mode=False):
	# проверяем существует ли файл вообще
	if os.path.exists(file_name):
		# определяем режим
		if not mode:
			# открываем файл в режим текстового чтения
			with open(file_name, 'rt') as f:
				# считываем информацию из файла
				result = f.read()
		else:
			if mode == 'pickle':
				# открываем файл в режим чтения байтов
				with open(file_name, 'rb') as f:
					# с помощью модуля pickle считываем байты
					result = pickle.load(f)
			elif mode == 'json':
				# открываем файл в режим текстового чтения
				with open(file_name, 'rt') as f:
					# с помощью модуля json считываем json-строку
					result = json.load(f)
		# возвращаем результат
		return result
	else:
		# иначе возвращаем False
		return False


# функция непосредственного перевода на QIWI Кошелек*
def send_p2p(api_access_token, to_qw, comment, sum_p2p):
	# открываем сессию с помощью модуля requests (да неужели)
	s = requests.Session()
	s.headers = {'content-type': 'application/json'}
	s.headers['authorization'] = 'Bearer ' + api_access_token
	s.headers['User-Agent'] = 'Android v3.2.0 MKT'
	s.headers['Accept'] = 'application/json'
	# определяем словарь параметров
	postjson = {"id": "", "sum": {"amount": "", "currency": ""}, "paymentMethod": {
		"type": "Account", "accountId": "643"}, "comment": "", "fields": {"account": ""}}
	# Клиентский ID транзакции
	postjson['id'] = str(int(time.time() * 1000))
	# Сумма (можно указать рубли и копейки, разделитель .)
	postjson['sum']['amount'] = sum_p2p
	# Валюта (только 643, рубли)
	postjson['sum']['currency'] = '643'
	# Номер телефона получателя (с международным префиксом, но без +)
	postjson['fields']['account'] = to_qw
	# если есть комментарий
	if comment:
		postjson['comment'] = comment
	# отправляем пост запрос
	res = s.post(
		'https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
	# если ответ успешно получен
	if res.status_code == 200:
		# возвращаем json
		return res.json()
	else:
		# иначе возвращаем False
		return False


# функция для генерации символьного кода
def GenCharCode(length, step_symbol=''):
	chars = 'QWERTYUIOPASDFGHJKLZXCVBNM'
	# с помощью генератора получаем рандомный символьный код
	code_list = [chars[random.randint(0, len(chars) - 1)]
				 for i in range(length)]
	# возвращаем символьный код, объединенный через step_symbol
	code_s = step_symbol.join(code_list)
	code = ''.join(code_list)
	return code_s, code


# функция для проведения перевода на другой кошелек QIWI
# need_confirm - требовать подтверждение
def SendToQiwi(api_token, now_qiwi, now_balance, to_qiwi, sum_p2p, comment=False, need_confirm=True):
	# убираем на всякий случай '+'
	to_qiwi = to_qiwi.replace('+', '')
	# делаем проверку телефона получателя
	try:
		if int(to_qiwi) > 999999999:
			to_qiwi_cor = True
		else:
			to_qiwi_cor = False
	except:
		to_qiwi_cor = False

	# делаем проверку суммы перевода
	try:
		if 1 <= float(sum_p2p) <= now_balance:
			sum_p2p_cor = True
		else:
			sum_p2p_cor = False
	except:
		sum_p2p_cor = False

	# если номер введен корректно
	if to_qiwi_cor:
		# если сумма перевода введена корректно
		if sum_p2p_cor:
			# выводим информацию о переводе
			print('Информация о переводе')
			print('-' * 30)
			print('Отправитель (данный кошелек).')
			print('Телефон: {}'.format(now_qiwi))
			print('Баланс: {} RUB'.format(now_balance))
			print('-' * 30)
			print('Получатель.')
			print('Телефон: {}'.format(to_qiwi))
			print('Сумма перевода: {} RUB'.format(sum_p2p))
			print('-' * 30)
			if comment:
				print('Комментарий: {}'.format(comment))
				print('-' * 30)
			# если включено, то запрашиваем подтверждение
			if need_confirm:
				while True:
					# получаем рандомный символьный код
					show_code, prog_code = GenCharCode(
						length=5, step_symbol='.')
					user_code = input(
						'\nПодтвердите перевод (для этого введите без точек - {}): '.format(show_code))
					# сравниваем коды
					if prog_code == user_code:
						print('Код введен верно!')
						# начинаем проводить платеж
						send_answer = send_p2p(
							api_access_token=api_token, to_qw=to_qiwi, comment=comment, sum_p2p=sum_p2p)
						if send_answer:
							send_status = send_answer[
								"transaction"]["state"]["code"]
							print('Статус перевода: {}'.format(send_status))
						else:
							print('Ошибка! Перевод не выполнен.')
						# выходим из цикла
						break
					else:
						print('Код введен неверно!')
			else:
				# начинаем проводить платеж
				send_answer = send_p2p(
					api_access_token=api_token, to_qw=to_qiwi, comment=comment, sum_p2p=sum_p2p)
				print('Статус перевода: {}'.format(
					send_answer["transaction"]["state"]["code"]))
		else:
			print('Ошибка! Сумма перевода указана неверно.')
	else:
		print('Ошибка! Неверно введен номер получателя.')

print('=' * 90)
print('The program created by prod.z9L')
print('YouTube channel: https://www.youtube.com/channel/UCy5bHWLxO3RGqP92AuaOj5A')
print('My VK Group (for answers): https://vk.com/club185628534')
print('My Aura: @levlab79')
print('Thank you for your attention :)')
print('=' * 90)
print()
print()

check_token = input('Проверить сохранен ли токен? (y/n): ')
if check_token == 'y':
	# проверяем есть ли сохранение api токена
	token_dict = CheckSaving('token.save', mode='pickle')
	# если он есть
	if token_dict:
		api_token = token_dict["api_token"]
		print('Токен успешно загружен.')
		print()
		show_token = input('Отобразить токен? (y/n): ')
		if show_token == 'y':
			print('Токен: {}'.format(api_token))
	else:
		# если сохранений нет
		print('Сохраненного токена не найдено!')
		check_token = 'n'
print()

if check_token != 'y':
	api_token = input('Укажите токен: ')
	# создаем запись с токеном
	token_dict = {'api_token': api_token}
	save_token = input('Сохранить новый токен? (y/n): ')
	if save_token == 'y':
		SaveInfo('token.save', token_dict, mode='pickle')
		print('Токен успешно сохранен!')
	print()

print('Получаем информацию об аккаунте...')
# получаем информацию об аккаунте (нужно, чтобы узнать номер телефона)
acc_info = get_profile(api_token)
# в случае успеха
if acc_info:
	# получаем номер телефона
	user_mobile = str(acc_info["authInfo"]["personId"])
	# получаем почту
	user_email = acc_info["authInfo"]["boundEmail"]
	# получаем еще другие значения
	en_change = 'Да' if acc_info["contractInfo"][
		"nickname"]["canChange"] else "Нет"
	en_use = 'Да' if acc_info["contractInfo"]["nickname"]["canUse"] else "Нет"
	blocked = 'Да' if acc_info["contractInfo"]["blocked"] else "Нет"

	# получаем информацию о балансе
	balance_info = get_balance(user_mobile, api_token)
	# определяем переменные балансов
	balance_rub = 0
	balance_usd = 0
	balance_eur = 0
	# получаем балансы
	balances = balance_info["accounts"]
	# заполняем переменные балансов
	for balance in balances:
		# определяем в какой валюте представлен баланс
		# 643 - российский рубль, 840 - американский доллар, 978 - евро
		if balance["currency"] == 643:
			balance_rub = balance["balance"]["amount"]
		elif balance["currency"] == 840:
			balance_usd = balance["balance"]["amount"]
		elif balance["currency"] == 978:
			balance_eur = balance["balance"]["amount"]

	print('Успешно!\n')

	# выводим информацию об аккаунте
	print('Информация об аккаунте')
	print('-' * 30)
	print('Телефон: {}'.format(user_mobile))
	print('E-mail: {}'.format(user_email))
	print('Ник: {}'.format(acc_info["contractInfo"]["nickname"]["nickname"]))
	print('Статус: {}'.format(acc_info["contractInfo"][
		  "identificationInfo"][0]["identificationLevel"]))
	print('-' * 30)

	# выводим только те балансы, который существуют
	if balance_rub or balance_usd or balance_eur:
		print(f'Баланс RUB: {balance_rub}\n' if balance_rub else '', end='')
		print(f'Баланс USD: {balance_usd}\n' if balance_usd else '', end='')
		print(f'Баланс EUR: {balance_eur}\n' if balance_eur else '', end='')
	else:
		print('Не удалось загрузить баланс!')

	print('-' * 30)
	print('Доступны переводы: {}'.format(en_change))
	print('Доступна информация: {}'.format(en_use))
	print('Блокировка: {}'.format(blocked))
	print('-' * 30)
	# сделал цикл, чтобы можно было выполнить несколько действий, не
	# перезапуская программу
	while True:
		print('\nВыберите следующее действие (укажите номер пункта):')
		print('1. Посмотреть историю платежей (от 1 до 50).')
		print('2. Перевести на другой QIWI кошелек.')
		print('3. Выйти из программы.')
		action = input('Ввод: ')
		# обрабатываем выбранный пункт
		if action == '1':
			n_payments = input('\nУкажите число платежей: ')
			# проверяем ввел ли пользователь число
			try:
				if 50 >= int(n_payments) >= 1:
					int_correct = True
				else:
					int_correct = False
			except:
				int_correct = False
			if not int_correct:
				n_payments = 10
				print('Число платежей изменено на {}'.format(n_payments))
			# получаем историю платежей
			history = get_history(user_mobile, api_token, n_payments)
			print()
			i = 1
			# проверяем
			if history:
				# получаем список платежей
				payments_list = history["data"]
				# отображаем историю платежей
				for payment in payments_list:
					# получаем статус платежа
					payment_status = payment["status"]
					# получаем тип платежа (входящий/исходящий)
					payment_type = payment["type"]
					# получаем валюта платежа
					payment_currency = payment["total"]["currency"]
					# получаем сумму платежа
					payment_sum = payment["total"]["amount"]
					# получаем название платежа
					payment_name = payment["provider"]["shortName"]
					# определяем нашего друга по платежу
					payment_friend = payment["account"]
					# определяем дату платежа
					payment_date = payment["date"]
					payment_date = payment_date.replace(
						'T', ' ').replace('+', ' +')
					# определяем валюту
					# 643 - российский рубль, 840 - американский доллар, 978 -
					# евро
					if payment_currency == 643:
						currency_name = 'RUB'
					elif payment_currency == 840:
						currency_name = 'USD'
					elif payment_currency == 978:
						currency_name = 'EUR'
					else:
						currency_name = 'SMTH'
					# определяем "знак" перевода
					if payment_type == 'IN':
						symbol = '+'
					elif payment_type == "OUT" or payment_type == "QIWI_CARD":
						symbol = '-'
					else:
						symbol = ''
					# выводим информацию об платеже
					print(f'[{payment_status}] #{i}\t{payment_name}: {symbol}{payment_sum} {currency_name}\t[{payment_friend}] - {payment_date}')
					i += 1
			else:
				print('Ошибка, повторите запрос позже!')
		elif action == '2':
			saved_numbers = CheckSaving(
				file_name='mobiles.save', mode='pickle')
			# проверяем сколько найдено сохраненных номеров
			if saved_numbers:
				# получаем список номеров
				m_numbers = saved_numbers["numbers"]
				# определяем их кол-во
				n_numbers = len(m_numbers)
			else:
				# создаем основной словарь
				saved_numbers = {"numbers": list()}
				# создаем список номеров
				m_numbers = list()
				n_numbers = 0
			print('\nВыберите действие:')
			print(
				'1. Открыть список сохраненных контактов (доступно: {}).'.format(n_numbers))
			print('2. Ввести номер вручную (без сохранения).')
			print('3. Назад.')
			select = input('Ввод: ')
			# определяем выбранный пункт
			if select == '1':
				while True:
					print('\nВыберите действие/получателя:')
					print('1. Добавить получателя.')
					print('2. Назад.')
					# если количество сохраненных номеров > 0
					i = 3
					if n_numbers:
						for number in m_numbers:
							# получаем имя контакта
							m_name = number["name"]
							# получаем номер телефона
							m_number = number["number"]
							# получаем описание
							m_comment = number["comment"]
							print(f'{i}. {m_name}: {m_number} ({m_comment})')
							i += 1
					contacts_select = input('Ввод: ')
					if contacts_select == '1':
						print('\nЗаполните информацию о новом получателе.')
						new_name = input('Имя: ')
						new_number = input('Телефон (без +): ')
						new_comment = input('Описание: ')
						# записываем в список
						m_numbers.append(
							{"name": new_name, "number": new_number, "comment": new_comment})
						# перезаписываем словарь
						saved_numbers["numbers"] = m_numbers
						# сохраняем его
						SaveInfo(file_name='mobiles.save',
								 info=saved_numbers, mode='pickle')
						print('Успешно!')
						# выходим из цикла
						break
					elif contacts_select == '2':
						# выходим из цикла
						break
					else:
						# проверяем является ли строка числом
						if contacts_select.isdigit():
							# преобразуем в число
							contacts_select = int(contacts_select)
							# пытаемся получить выбранный контакт
							try:
								# получаем данные
								number = m_numbers[contacts_select - 3]
							except:
								print('\nОшибка. Некорректно выбран получатель.')
							else:
								# если данные успешно получаны
								print('\nВыбранный получатель.')
								print('Имя: {}'.format(number["name"]))
								print('Телефон: {}'.format(number["number"]))
								print('Описание: {}'.format(number["comment"]))
								print('\nВыберите действие')
								print('1. Перевести на этот номер кошелька QIWI.')
								print('2. Удалить получателя.')
								man_select = input('Ввод: ')
								# определяем выбор
								if man_select == '1':
									to_qiwi = number["number"]
									to_sum = input(f'\nУкажите сумму перевода RUB (от 1.0 до {balance_rub}): ')
									to_comment = input(
										'Введите комментарий (либо оставьте пустым): ')
									print()
									# если комментарий пустой
									if not to_comment:
										to_comment = False
									# вызываем функцию перевода qiwi
									SendToQiwi(api_token=api_token, now_qiwi=user_mobile, now_balance=balance_rub,
											   to_qiwi=to_qiwi, sum_p2p=to_sum, comment=to_comment, need_confirm=True)
								elif man_select == '2':
									cofirm_del = input(
										'Вы уверены, что хотите удалить получателя? (y/n): ')
									if cofirm_del == 'y':
										# удаляем элемент из списка
										del m_numbers[contacts_select - 3]
										# перезаписываем словарь
										saved_numbers["numbers"] = m_numbers
										# сохраняем изменения
										SaveInfo(file_name='mobiles.save',
												 info=saved_numbers, mode='pickle')
										print('Успешно!')
										# выходим из цикла
										break

			elif select == '2':
				to_qiwi = input('\nВведите номер кошелька QIWI (без +): ')
				to_sum = input(f'Укажите сумму перевода RUB (от 1.0 до {balance_rub}): ')
				to_comment = input(
					'Введите комментарий (либо оставьте пустым): ')
				print()
				# если комментарий пустой
				if not to_comment:
					to_comment = False
				# вызываем функцию перевода qiwi
				SendToQiwi(api_token=api_token, now_qiwi=user_mobile, now_balance=balance_rub,
						   to_qiwi=to_qiwi, sum_p2p=to_sum, comment=to_comment, need_confirm=True)
		elif action == '3':
			# этот пункт мой любимый (потому что я хочу спать :c)
			exit()
		else:
			print('\nНе удалось распознать действие')
else:
	print('Ошибка!')
	exit()
