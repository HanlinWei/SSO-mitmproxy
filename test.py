from urllib.parse import urlparse
import re
url = 'https://www.facebook.com/dialog/oauth?client_id=500163113370079&redirect_uri=https%3a%2f%2faccount.fifa.com%2f5a7baeb7-e706-4830-ad9f-103eba126311%2foauth2%2fauthresp&response_type=code&scope=email&state=StateProperties%3deyJTSUQiOiJ4LW1zLWNwaW0tcmM6YzE5MzhiYmYtZGI5Zi00MjMzLWFiNzEtNzZlNjA2Yzc2ZTdmIiwiVElEIjoiNzhjOGU3Y2EtYzQ5Zi00MDU4LThjYWYtOTE0YmE0ZTE2ZmJiIn0'
parsed_result=urlparse(url)

print('parsed_result 包含了',len(parsed_result),'个元素')
print(parsed_result)

if "*" in "*":
    print("123"[2])

pattern = re.compile('\W*Ross\W*')
str = "Ross\"0Ross\" Ross"
print(pattern.search(str))

print(str.find("Ross", 1))

print(re.match("\W*"+"Ross"+"\W*", "Ross\"0Ross\" Ross"))
if re.match("\W", "-"):
    print("666")
