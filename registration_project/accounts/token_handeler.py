import jwt


'''
Custom token generator
'''
def generate_token(payload):
    token = jwt.encode(payload, 'SECRET').decode('utf-8')
    return token

   
# payload = ({'username':"deep" ,
#                 'password':'deep'})

# print(generate_token(payload))

# encoded_data = jwt.encode({'username' : "abc"}, 'SECRET', algorithm = 'HS256')
# print(encoded_data)

