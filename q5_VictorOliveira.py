from os import path
from flask import Flask, request

app = Flask(__name__, template_folder="templates")

# Constants
SEPARATOR = lambda: ";"
USER_FILE_PATH = lambda: path.abspath(path.join(__file__, "..", "q5", "users.txt"))

# Functions
# - Responses
success_sign_up_response = ({"message": "User created successfully"}, 200)
error_sign_up_response = ({"message": "User already exists or invalid data"}, 400)
success_sign_in_response = ({"message": "User authenticated successfully"}, 200)
error_sign_in_response = ({"message": "User not authenticated or invalid data"}, 400)

# - Utilities
get_dict_key_list = lambda dictionary: "\n".join([f"- {key}" for key in dictionary.keys()])
add_dict_key = lambda dictionary, key, value: dictionary.update({key: value}) or True if key and value else False
remove_dict_key = lambda dictionary, key: dictionary.pop(key) if key in dictionary.keys() else False
clear_dict = lambda dictionary: dictionary.clear() or True if dictionary else False

get_formatted_dict = lambda dictionary: "\n".join([f"{key} - {value}" for key, value in dictionary.items()])
value_if_in_iterable: callable = lambda value, iterable: value if value in iterable else None

create_user_dict_from_rows = lambda rows: {row[0]: row[1] for row in rows}
dict_to_csv = lambda dictionary_list, separator: [f"{key}{separator}{value}" for key, value in dictionary_list.items()]

get_rows = lambda lines: [line.split(SEPARATOR()) for line in lines]
get_file_lines = lambda file_path: open(file_path, "r").read().splitlines()
write_file_by_iterable = lambda file_path, iterable: open(file_path, "w").write("\n".join(iterable))

synchronize_file = lambda file_path, dictionary, separator: write_file_by_iterable(
    file_path,
    dict_to_csv(dictionary, separator)
)

user_file_lines = get_file_lines(USER_FILE_PATH())
users = create_user_dict_from_rows(get_rows(user_file_lines))

# Endpoints
# - Sign up
add_user = lambda user_dict, username, password: (
    add_dict_key(user_dict, username, password) or True
    if username and password and username not in user_dict.keys()
    else False
)

sign_up = lambda user_dict: add_user(user_dict, request.json.get("username"), request.json.get("password"))
sign_up_endpoint = lambda: (
    success_sign_up_response
    if sign_up(users) and synchronize_file(USER_FILE_PATH(), users, SEPARATOR())
    else error_sign_up_response
)

# - Sign in
authenticate = lambda user_dict, username, password: username and password and user_dict.get(username) == password
sign_in = lambda user_dict: authenticate(user_dict, request.json.get("username"), request.json.get("password"))

sign_in_endpoint = lambda: success_sign_in_response if sign_in(users) else error_sign_in_response

app.add_url_rule(rule="/sign_up", endpoint="sign_up", view_func=sign_up_endpoint, methods=["POST"])
app.add_url_rule(rule="/sign_in", endpoint="sign_in", view_func=sign_in_endpoint, methods=["POST"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
