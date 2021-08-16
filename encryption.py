#----------encryption mechanism for storing passwords safely------#
def encrypt(txt):                                                                               # Rotation Encryption function (5 forward alphabetical rotations)
    encrypted = ''                                                                              # Clears string cache
    for i in txt:                                                                               # New loop (len of txt)
        c = ord(i)+100                                                            # Ord gets the ASCII value for a character and increases its value by 100
        if ord(i) != c:                                                                         # If c is a new character
            b = chr(c)                                                                          # b equals the character of the ASCII value
            encrypted += b                                                                      # Adds each character to the encrypted string
    encrypted=str(encrypted.replace("\\","#"))                                                  # Replaces special characters so that a text file can be created
    encrypted=str(encrypted.replace("|","%"))                                                   # Replaces special characters so that a text file can be created
    return encrypted                                                                            # Returns this string when the function is called

def decrypt(txt):                                                                               # Rotation Decryption function (5 backward alphabetical rotations)
    txt.replace('#','\\')                                                                       # Replaces special characters so that the string can be decrypted
    txt.replace('%','|')                                                                        # Replaces special characters so that the string can be decrypted
    decrypted = ''                                                                              # Clears string cache
    for x in txt:                                                                               # New loop (len of txt)
        c = ord(x)-100                                                                    # Ord gets the ASCII value for a character and decreases its value by 100                                                      
        if ord(x) != c:                                                                         # If c is a new character
            b = chr(c)                                                                          # b equals the character of the ASCII value
            decrypted += b                                                                      # Adds each character to the encrypted string
    return decrypted      
