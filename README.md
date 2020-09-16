# wiki-user-adder

The *wiki user adder` is a small python script to quickly add new members to the wiki, and grant them the appropiate permissions.

## Requirements

* python3 (and pip)

## Setup

1. Enable Remote API access on the wiki. This should be disabled when not using the script - even though the API requires authentication, for best security practices it should not be accessible normally. This can be done in *Confluence administration --> Further Configuration*

2. Download this repo to your computer, and install the dependencies:

    ```bash
    git clone https://github.com/illini-motorsports/    wiki-user-adder && cd wiki-user-adder

    pip install -r requirements.txt
    ```

3. Copy `sample_config.json` to  a new file `config.json` and set the following properties:

   - auth 
     - username: the username of the wiki account to use (must be an admin account)
     - password: the password of the wiki account
   - options
     - group: the Confluence group to add users to
       - As of the time of writing, this is `team-members`
   - endpoint: the RPC API endpoint of the wiki
     - As of the time of writing, this is `http://wiki.motorsports.illinois.edu/rpc/json-rpc/confluenceservice-v2`
  
4. Create a `.csv` file containing in *separate* columns, for the users you want to add to the wiki:
     - first name
     - last name
     - net ID
     - email

    You can use Google Forms to collect all the necessary information, and use *File -> Download -> Comma separated values* to export the CSV file.

    An example CSV file is shown below. Make sure that a) you have separate columns for the fields detailed above, and b) there's no extra lines in the file. Extraneous columns are okay, and it doesn't matter what the columns are named.

    ```
    Email Address,First Name,Last Name,NetID
    test@illinois.edu, John, Doe, jdoe1
    test2@illinois.edu, Jane, Doe, jdoe2
    ```



## Usage

Run the script with `python app.py`, and follow the prompts:

```
Enter the file path to the .csv file with the list of users to add: /Users/aditya/Downloads/roster.csv
? Which column contains the students' first names?  First Name
? Which column contains the students' last names?  Last Name
? Which column contains the students' net IDs?  NetID (e.g., doej2)
? Which column contains the students' emails?  Email Address
? Confirm?  (Use arrow keys)
 » Yes
   No
```

The script will then add every user in the file to the wiki, using each student's net ID as their username. Students will also be added to the specified wiki group. The script can be re-run, as it gracefully handles students who've already been added to the wiki or the target group. 

Note that the accounts are created with no password, but cannot directly be logged in to. This is due to a bug in our wiki setup - welcome emails are not sent to new users. Instead, have new accounts use the "Forgot password" option to set their password.

## Notes

### RPC API

This script uses the ancient Confluence JSON RPC API. Unfortunately, the modern Confluence REST API has an extremely limited number of features, mostly relating to modifying pages.
In the (far) future, this script should be updated to preferably use the Confluence REST API if possible.

Documentation for the Confluence RPC API can be found [here.](https://developer.atlassian.com/server/confluence/confluence-xml-rpc-and-soap-apis)
