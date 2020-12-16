# Plex service Status

## Usage 

All responses will have the form 

```json 
{
	"data": "Mixed type holding the content of the responses",
	"message": "Description of what happened"
}
```

Subsequent response deffinitions will only details the expected value of the `data field`

### GET health of service

**Definition**

`GET /health`

**Response**

- `200 OK` on success

```json

[
	{
		"hostname": "frontend",
		"is-active": "active"

	}
]
```

### Sending Health Status

**Definitions**

 `POST /health`

**Arguements**

- `"hostname": string` a unique hostname 
- `"is-active": string` unique string to tune service for is active or not



If a device with the given identifer already exists, the device will be overwrittne'

**Response**

- `201 Created` on success
```json

[
	{
		"hostname": "frontend",
		"is-active": "active"

	}
]
```

## Lookup device details 

`GET /device/<hostname>`

**Response**

- `404 Not Found` if hostname doesn't exist 

- `200 OK` on success 

```json

[
	{
		"hostname": "frontend",
		"is-active": "active"

	}
]
```





