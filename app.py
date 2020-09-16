import requests, random, json, os, csv, questionary

# path to the config json file
CONFIG_FILE = "./config.json"

# wrapper for RPC calls to the wiki
class RPCClient:
    def __init__(self, url, username, password, version="2.0"):
        self.url = url
        self.username = username
        self.password = password
        self.version = version

    def _execute(self, method, params):

        data = {
            "jsonrpc": self.version,
            "method": method,
            "params": params,
            "id": random.randint(1000, 2000),
        }

        response = requests.post(
            self.url,
            json=data,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password),
        )
        return response

    def addUser(self, username, fullname, email):
        return self._execute(
            "addUser",
            [
                {"name": username, "fullname": fullname, "email": email},
                "Credential.NONE",
                True,
            ],
        )

    def addUserToGroup(self, username, group):
        return self._execute("addUserToGroup", [username, group])


if __name__ == "__main__":

    # load config, setup RPC client
    if not os.path.exists(CONFIG_FILE):
        print("Config file doesn't exist!")
        exit(1)
    config = json.load(open(CONFIG_FILE))
    client = RPCClient(
        config["endpoint"], config["auth"]["username"], config["auth"]["password"]
    )

    # get the input CSV file, and the proper columns
    input_file_path = input(
        "Enter the file path to the .csv file with the list of users to add: "
    ).strip()
    if not os.path.exists(input_file_path):
        print("File doesn't exist!")
        exit(1)

    input_file_reader = csv.reader(open(input_file_path))
    columns = next(input_file_reader)

    firstname_column = questionary.select(
        "Which column contains the students' first names?", choices=columns
    ).ask()
    firstname_column_idx = columns.index(firstname_column)

    lastname_column = questionary.select(
        "Which column contains the students' last names?", choices=columns
    ).ask()
    lastname_column_idx = columns.index(lastname_column)

    netid_column = questionary.select(
        "Which column contains the students' net IDs?", choices=columns
    ).ask()
    netid_column_idx = columns.index(netid_column)

    email_column = questionary.select(
        "Which column contains the students' emails?", choices=columns
    ).ask()
    email_column_idx = columns.index(email_column)

    # confirm one last time
    confirm = questionary.select("Confirm?", choices=["Yes", "No"]).ask()
    if confirm != "Yes":
        print("Cancelling...")
        exit(1)

    # iterate through each entry, adding to the wiki and the correct group
    for line in input_file_reader:
        firstname = line[firstname_column_idx]
        lastname = line[lastname_column_idx]
        fullname = "{} {}".format(firstname, lastname)
        netid = line[netid_column_idx]
        email = line[email_column_idx]

        res = client.addUser(netid, fullname, email)
        if "error" in json.loads(res.text):
            print(
                "Couldn't add user {} - {}, they probably already exist!".format(
                    fullname, netid
                )
            )
        else:
            print("Added user {} - {} to the wiki".format(fullname, netid))

        res = client.addUserToGroup(netid, config["options"]["group"])
        if "error" in json.loads(res.text):
            print(
                "Couldn't add user {} - {} to the correct group, your config is probably messed up!".format(
                    fullname, netid
                )
            )
        else:
            print(
                "\tAdded user {} - {} to the {} group".format(
                    fullname, netid, config["options"]["group"]
                )
            )
