import POM_GEN
driver = POM_GEN.Driver('http://localhost:8080/')


def main_navbar(input=""):
	main_navbar = POM_GEN.ObjectGen('main-navbar', driver.driver)
	if not input:
		main_navbar.object.click()
	else:
		main_navbar.object.send_keys(input)

