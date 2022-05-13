import _owners_new
import time

# WRITE TEST HERE
# main_navbar, add_owner_form, firstName, lastName, address, city, telephone, Add_Owner

_owners_new.driver.driver.maximize_window()

_owners_new.firstName("name")
time.sleep(0.5)
_owners_new.lastName("surname")
time.sleep(0.5)
_owners_new.address("home")
time.sleep(0.5)
_owners_new.city("city")
time.sleep(0.5)
_owners_new.telephone("1234")
time.sleep(0.5)
_owners_new.Add_Owner()
