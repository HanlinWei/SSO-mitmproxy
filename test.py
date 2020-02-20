from urllib.parse import urlparse
import re
url = "https://api.entrepreneur.com/v1.1/fblogin?code=AQC9F3mFlostzMvOxDfxhArKOG5Vknb8M2hkzlXbiCPTullOu2tA0_se0Xz9gJ69KYnVzCxH3euaGdUy9uZn2S-sEm_bWpZZAK8uL6gHgjW9KDqR12_G27UI4MKaSq2YttgcoO6XbIL2IsC_gz93fnPSlzy9UM3XzZLN7UcKDHS3cpXUNVmewKPOCvOSD-EerWw1Q0N2M3ZXE4aIT7HMTKnwVrHazKFUPlJj1WOAGQ2sNZHRRISvZLI5GQKvjzQBD4ibDwxaoNSzrMF8yicfo7dOhvQUZiPcKo_UL6W4GK5c2vhB3fJQ220i-I1Vm9YgnXRjzGVL3hF8NkSr0GriyWu5&state=d9a9e74f3a27436672c1f1aad18f918b"
parsed_result=urlparse(url)

print(parsed_result.query.split("&"))

if "*" in "*":
    print("123"[2])

pattern = re.compile('\W*Ross\W*')
str = "Ross\"0Ross\" Ross"
print(pattern.search(str))

print(str.find("Ross", 1))

print(re.match("\W*"+"Ross"+"\W*", "Ross\"0Ross\" Ross"))
if re.match("\W", "c"):
    print("666")

content = ""