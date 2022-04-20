import re
str = "<button class=\"btn btn-primary\" type=\"submit\">Add Owner</button>"

m = re.search(">(.+?)<", str)
if m:
    solution = m.group(1)
print(solution)
