# Mchoice

Mchoice is a very simple web app built using Django v3. It parses word documents with multiple choice tests and and creates tests with those questions.

## Current Functionality
* Upload `.docx` files and parse them into tests (_A specific structure is needed in order to be parsed correctly, check below_)
* Have tests with 30 randomly picked questions from the question pool.
* Check the results wich includes score (_in scale of 10_) and also some basic stats and all the questions with your answers


## Features to be added
* Run tests as they are uploaded
* Ability to parse various types of `.docx` structures and maybe add more file types
* Improve the UI to offer a more pleasant experience.
* Handling images and tables inside questions text
* More to be added