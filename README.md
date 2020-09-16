# wiki-user-adder

The *wiki user adder` is a small python script to quickly add new members to the wiki, and grant them the appropiate permissions.

## Setup

1. Download this repo to your computer.

```bash
git clone https://github.com/illini-motorsports/wiki-user-adder
```

2. Modify `config.json` and set the following properties:

- auth 
  - username: the username of the wiki account to use (must be an admin account)
  - password: the password of the wiki account
- options
  - group: the Confluence group to add users to
- endpoint: the RPC API endpoint of the wiki
  - As of the time of writing, this is `http://wiki.motorsports.illinois.edu/rpc/json-rpc/confluenceservice-v2`
  
## Usage


## Notes

### RPC API

This script uses the ancient Confluence JSON RPC API. Unfortunately, the modern Confluence REST API has an extremely limited number of features, mostly relating to modifying pages.
In the (far) future, this script should be updated to preferably use the Confluence REST API if possible.

Documentation for the Confluence RPC API can be found [here.](https://developer.atlassian.com/server/confluence/confluence-xml-rpc-and-soap-apis)
