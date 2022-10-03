import POM_GEN
driver = POM_GEN.Driver('http://localhost:8080/owners/7/edit')


def main_navbar(input=""):
	main_navbar = POM_GEN.ObjectGen('main-navbar', driver.driver)
	if not input:
		main_navbar.object.click()
	else:
		main_navbar.object.send_keys(input)


def add_owner_form(input=""):
	add_owner_form = POM_GEN.ObjectGen('add-owner-form', driver.driver)
	if not input:
		add_owner_form.object.click()
	else:
		add_owner_form.object.send_keys(input)


def firstName(input=""):
	firstName = POM_GEN.ObjectGen('firstName', driver.driver)
	if not input:
		firstName.object.click()
	else:
		firstName.object.send_keys(input)


def lastName(input=""):
	lastName = POM_GEN.ObjectGen('lastName', driver.driver)
	if not input:
		lastName.object.click()
	else:
		lastName.object.send_keys(input)


def address(input=""):
	address = POM_GEN.ObjectGen('address', driver.driver)
	if not input:
		address.object.click()
	else:
		address.object.send_keys(input)


def city(input=""):
	city = POM_GEN.ObjectGen('city', driver.driver)
	if not input:
		city.object.click()
	else:
		city.object.send_keys(input)


def telephone(input=""):
	telephone = POM_GEN.ObjectGen('telephone', driver.driver)
	if not input:
		telephone.object.click()
	else:
		telephone.object.send_keys(input)

