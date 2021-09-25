# Tech stacks

The docker container will output a json with tech stacks of websites for the NC survey.
 
JSON Format:

[ ..., {"url": NC survey website, "tech": tech from the url , "href": builtwith link with stats on tech }, ... ]


## Commands:

'docker build -t selenium_image .'

'docker container  run -it --name selenium_container selenium_image'

'docker cp selenium_container:/app/data.json data.json'