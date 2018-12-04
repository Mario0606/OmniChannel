import hangups
request_token1 = None
email = hangups.CredentialsPrompt.get_email()
password = hangups.CredentialsPrompt.get_password()

print(email, password)
if(request_token1 == None): 
    x = hangups.get_auth([email,password],hangups.RefreshTokenCache("refresh_token.json"))
else:
    hangups.get_auth_stdin(request_token1)
print(x)

hangups.client.Client("cookies",max_retries=5)

