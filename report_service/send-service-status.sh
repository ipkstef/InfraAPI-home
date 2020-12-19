#! /bin/bash

# seperate different OS into variables 
declare -A osInfo;
osInfo[/etc/debian_version]="apt-get install -y"
osInfo[/etc/alpine-release]="apk --update add"
osInfo[/etc/centos-release]="yum install -y"
osInfo[/etc/fedora-release]="dnf install -y"
osInfo[/etc/arch-release]="pacman -Syu"
osInfo[/etc/alpine-release]="apk add"

# loop through variables and test if release version file exists 
for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        package_manager=${osInfo[$f]}
    fi
done

package="curl"
if [ ! -e /usr/bin/curl ];then
  ${package_manager} ${package}
fi

package2="jq"
if [ ! -e /usr/bin/jq ];then
  ${package_manager} ${package2}
fi

package3="bash"
if [ ! -e /usr/bin/bash ];then
  ${package_manager} ${package3}
fi

package4="date"
if [ ! -e /usr/bin/date ];then
  ${package_manager} ${package4}
fi

echo `dirname "$0"`
#function to generate ACCESS token
generate_access_token() {
  /usr/bin/curl -s --request POST   --url http://api.fornjot.xyz:10070/login \
   --header 'Content-Type: application/json'  \
   -d @passwords.json | /usr/bin/jq --raw-output '.access_token'

}
ACCESS=$(generate_access_token)


# function that generates the post data of your script. 
#This saves you from all sort of headaches concerning shell quoting and makes it easier to read an maintain the script than feeding the post data on curl's invocation line as in your attempt

generate_post_data()
{
  cat <<EOF
{
		"hostname":"$hostname",
		"Containers-active": "$active",
		"uptime": "$uptime",
    		"date": "$date"
}
EOF
}

# pass variables
 # active variable is broken need ot fix docker absolute path

hostname=$(cat /etc/hostname)
active=$(/snap/bin/docker  ps --format '{{ .Names }} {{.Status}}' | paste -s -d, - )
uptime=$(uptime -p)
date=$(date)


/usr/bin/curl --header "Content-Type: application/json" \
  --header "Authorization: Bearer $ACCESS" \
  --request POST \
  --data "$(generate_post_data)" \
  http://api.fornjot.xyz:10070/devices




# TODO

# Crontab every min:

# `* * * * * /usr/local/bin/send-service-status.sh`
