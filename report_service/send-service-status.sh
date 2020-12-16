#! /bin/bash


# First, write a function that generates the post data of your script. 
#This saves you from all sort of headaches concerning shell quoting and makes it easier to read an maintain the script than feeding the post data on curl's invocation line as in your attempt

generate_post_data()
{
  cat <<EOF
{
		"hostname":"$hostname",
		"is-active": "$active",
		"uptime": "$uptime"
}
EOF
}

# pass variables

hostname=$(hostname)
active=$(systemctl is-active snap.docker.dockerd.service)
uptime=$(uptime -p)


curl --header "Content-Type: application/json" \
  --request POST \
  --data "$(generate_post_data)" \
  http://localhost:5000/devices

