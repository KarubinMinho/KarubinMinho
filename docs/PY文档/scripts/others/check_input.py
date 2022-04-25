allow_counts = 3

while allow_counts:
    username = input('Username:')
    password = input('Password:')
    if username == 'ok_username' and password == 'ok_password':
        print("Login Success.")
        break
    else:
        print("Error username or password.")
        allow_counts -= 1

# 做得不错
