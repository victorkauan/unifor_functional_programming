from os import path

# Constants
SEPARATOR = lambda: ";"
USER_FILE_PATH = lambda: path.abspath(path.join(__file__, "..", "q2", "users.txt"))

# Functions
# - Messages
user_list_title = lambda: print("USERS:")
question_title = lambda: print("QUESTION 02 BY VICTOR KAUAN LIMA DE OLIVEIRA")

invalid_operation_message = lambda *args, **kwargs: print("[ERROR] Invalid operation")

sign_up_success_message = lambda: print("[SUCCESS] User created successfully")
sign_up_failed_message = lambda: print("[ERROR] User already exists or invalid data")

sign_in_success_message = lambda: print("[SUCCESS] User authenticated successfully")
sign_in_failed_message = lambda: print("[ERROR] User not authenticated or invalid data")

no_users_registered_message = lambda: print("No users registered")

remove_user_success_message = lambda: print("[SUCCESS] User removed successfully")
remove_user_failed_message = lambda: print("[ERROR] User not found or invalid data")

clear_users_success_message = lambda: print("[SUCCESS] Users cleared successfully")
clear_users_failed_message = lambda: print("[ERROR] No users to clear")

# - Utilities
finish_app = lambda *args, **kwargs: exit(0)

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

# - Sign up
add_user = lambda user_dict, username, password: (
    add_dict_key(user_dict, username, password) or True
    if username and password and username not in user_dict.keys()
    else False
)
enter_username = lambda: input("Enter your username: ")
enter_password = lambda: input("Enter your password: ")

sign_up = lambda user_dict: (
    sign_up_success_message()
    if add_user(user_dict, enter_username(), enter_password())
    else sign_up_failed_message()
)

# - Sign in
authenticate = lambda user_dict, username, password: username and password and user_dict.get(username) == password
sign_in = lambda user_dict: (
    sign_in_success_message()
    if authenticate(user_dict, enter_username(), enter_password())
    else sign_in_failed_message()
)

# - Extra
list_users = lambda user_dict: (
    (user_list_title() or print(get_dict_key_list(user_dict)))
    if user_dict
    else no_users_registered_message()
)

clear_users = lambda user_dict: clear_users_success_message() if clear_dict(user_dict) else clear_users_failed_message()

enter_username_to_remove = lambda: input("Enter the username to remove: ")
remove_user_by_username = lambda user_dict, username: (
    user_dict.pop(username)
    if username and username in user_dict.keys()
    else False
)

remove_user = lambda user_dict: (
    remove_user_success_message()
    if remove_user_by_username(user_dict, enter_username_to_remove())
    else remove_user_failed_message()
)

menu_titles = lambda: {
    "0": "Exit",
    "1": "Sign up",
    "2": "Sign in",
    "3": "List users",
    "4": "Remove user",
    "5": "Clear users",
}

menu_functions = lambda: {
    None: invalid_operation_message,
    "0": finish_app,
    "1": sign_up,
    "2": sign_in,
    "3": list_users,
    "4": remove_user,
    "5": clear_users,
}

show_menu = lambda title_dictionary: print(f"OPERATIONS:\n{get_formatted_dict(title_dictionary)}")
choose_option = lambda: input("Choose an option: ")

loop = lambda: (
        show_menu(menu_titles()) or
        print() or
        all((
            menu_functions()[value_if_in_iterable(choose_option(), menu_functions().keys())](users),
            synchronize_file(USER_FILE_PATH(), users, SEPARATOR())
        )) or
        print() or
        loop()
)
app = lambda: question_title() or print() or loop()

if __name__ == "__main__":
    app()
