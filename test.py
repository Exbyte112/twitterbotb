unformatted_string = "Prestonkezo:x3ZQGp3761:armangmayumy@hotmail.com:x3ZQGp3761:63791a29537a70c1667965e1a00767e4df21a767:DRK5YFVGONH3KVVI"

formatted_string = unformatted_string.split(":")

formatted_dict = {
    "_id": formatted_string[0],
    "auth": formatted_string[1],
    "ct0": formatted_string[2],
    "email": formatted_string[3],
    "password": formatted_string[4],
    "username": formatted_string[5],
}

import json

with open("temp_accts.json", "w") as f:
    json.dump(formatted_dict, f)
