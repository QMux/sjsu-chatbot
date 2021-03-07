https://rasa.com/docs/rasa/installation/
installation guide above

instalation
•	python3 -m venv ./venv
•	source ./venv/bin/activate
•	pip3 install rasa
•	rasa init 	# to start it\


Training
•	rasa train


run
•	rasa run actions &
•	rasa shell
•	rasa shell --debug

other good commands
•	/stop       	# to stop it
•	/restart       	# to stop it


Dialog flow Example (all inputs from user):
note: we can simply input those values after we modified the entities values.
- hi
- are you a bot?
- what can you do?
- I want a cat
- do you have a dog image?
- I want to watch a dog videorasa 
- please help me to learn dog breeds
- any suggestion on dog group?
- let's go with sporting dog group
- any more information on dog activity level?
- i'd like a calm dog
- what is your suggestion on dog barking level?  
- let's go with vocal as barking level
- any additional information on dog's coat type
- I like fair coat type dogs
- any additional information on dog's shedding level
- I'd go with occasional as shedding level
- what are differences for dog size?
- I want xl dog
- any additional details on dog trainability?
- I like stubborn dogs

- let's restart (restart chatbot)
