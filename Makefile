
PWD := $(shell pwd)

default:
	echo Default rule

# These targets work only on Ubuntu

web:
	# Grab the latest nginx 
	docker pull nginx
	# Start the webserver, mapping from port 8080 to 80
	docker run -it --rm -d -p 8080:80 --name web -v $(PWD)/content:/usr/share/nginx/html nginx
