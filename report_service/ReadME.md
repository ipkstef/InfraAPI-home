# Service health reporter

## Overview 

**What it does**

Check to see if `jq` & `curl` are installed, if not it installs it. 
Then it generates an access token with a post request 

## Passwords

you need a passwords.json file in the `./report_service` directory structured liek this

**Example**

```json
{
	"username": "test",
	"password": "test"
}
```

## Crontab

*Every two mins, make sure to adjust rate limiting to match this*
*need to spawn a subshell if running from not root*

```bash
*/2 * * * *  (cd ~/Desktop/daphnis.api/report_service/ && ./send-service-status.sh )
```
