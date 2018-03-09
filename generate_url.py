def generate_all(user_in_nub):
	url = 'https://bj.lianjia.com/ershoufang/pg{}/'
	for url_next in range(1, int(user_in_nub)):
		yield url.format(url_next)

def main():
	user_in_nub = input('input pages:')
	for i in generate_all(user_in_nub):
		print(i)

if __name__ == '__main__':
	main()
