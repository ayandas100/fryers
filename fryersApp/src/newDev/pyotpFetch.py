'''
Created on 14-Apr-2024

@author: User
'''
import pyotp
# otpuri = pyotp.totp.TOTP('QUDQF2DQOWIPL2FFACUVUMW6S44CYXDV').provisioning_uri(name='ayantab@google.com', issuer_name='Fryers')
# # otp=pyotp.TOTP("064198")
# # otp_code = otp.now()
# # print(otp_code)
# print(otpuri)
x = pyotp.parse_uri('otpauth://totp/Fryers:ayantab%40google.com?secret=QUDQF2DQOWIPL2FFACUVUMW6S44CYXDV&issuer=Fryers')
print(x.now())