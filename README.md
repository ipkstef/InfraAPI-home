# Infrastructure Registry Service

## Usage 

All responses will have the form 

```json 
{
	"message": "Description of what happened",
	"data": "Mixed type holding the content of the responses"
}
```

Subsequent response deffinitions will only detail the expected value of the `data field`

### GET list of all services

**Definition**

`GET /devices`

**Response**

- `200 OK` on success

```json
{
  "message": "Success",
  "data": [
    {
      "hostname": "backendd",
      "is-active": "disabled",
      "uptime": "o days"
    },
    {
      "hostname": "osboxes",
      "is-active": "active",
      "uptime": "up 4 hours, 54 minutes"
    },
    {
      "hostname": "frontend",
      "is-active": "disabled",
      "uptime": "56 days"
    }
  ]
}
```

### Get health info of one service

**Definition**
`GET /health/<service-name>`


**Response**
- `200 OK` on success
- `404 Not Found` if hostname doesn't exist 

```json 
{
  "message": "Hostname exists in  DB",
  "data": {
    "hostname": "frontend",
    "is-active": "disabled",
    "uptime": "56 days"
  }
}
```


### Updating Health Status

**Definitions**

 `POST /device`

**Arguements**

- `"hostname": "service-name"` a unique hostname 
- `"is-active": "string"` unique string to tune service for is active or not

**Example POST request**
```bash 
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"hostname":"plex","is-active":"active"}' \
  http://localhost:5000/devices
```


- *If a device with the given identifer already exists, the device will be overwritten*

**Response**

- `201 Created` on success
```json
{
    "message": "Database has stored Service info",
    "data": {
        "hostname": "osboxes",
        "is-active": "active",
        "uptime": "up 4 hours, 54 minutes"
    }
}
```

## Delete a device

**Definition**

`DELETE /health/<service-name>`

**Response**

- `404 Not Found` if the device does not exist
- `204 No Content` on success







