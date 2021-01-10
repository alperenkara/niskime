from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("password1")
password2 = sha256_crypt.encrypt("password1")

print(password)
print(password2)

print(sha256_crypt.verify("password", password2))