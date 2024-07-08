## Intro
This script automates the tournament schedule verification process for SERVE. </br>
Some of these functions may not be the most optimum implementation due to specific use cases of SERVE tournament(Or me being lazy), but they should work. Feel free to make pull request to modify the script.
</br>
this should work with any # amount of signed up teams as one "team", aka works for both 3ps and reverses or any future tournament formats
## Prereq
- Have python installed on ur computer
- Knows how to clone a repository and use basic terminal commands, or has a friend that knows how to do it

## How to run the demo
1. make sure you have python on your computer and the command `python --version` shows your python version
2. open a terminal
3. clone the repository
4. change directory(`cd`) to the repository directory
5. execute the command below
```
python ./main.py ./example_input.txt 2 3
```
6. you should see the result in output.txt

## How to run your own input schedule
1. run the demo once, so you know how things work
2. read "Syntax of the input file" section so you know about the input file syntax
3. create your own input text file, call it whatever you want
3. run the following command 
```
python ./main.py <input_file_path> <max_number_play_with> <max_number_play_against>
or
python ./main.py <input_file_path>
```
note that `<max_number_play_with>` and `<max_number_play_against>` are optional arguments. Without them the script will still run and show you the results in `output.txt`

## Syntax of the input file
If you look at example_input.txt, the input schedule is in a very specific format and it has to be this way for the script to parse it properly. Well it has to be a series of numbers separated by space or tab character(s) but just follow the syntax of example.txt.
Each line is composed of team numbers separated by a single tab character and a string 'vs' to separate the sides. This format is handy because you can select the entire block in a text viewer and directly paste into excel. If you replace tab characters with spaces excel won't let you do that.

## Note for ppl modifying the script
1. All the indexes to the data types starts from 0, but when they are printed to output file or console the indexes are incremented by one to match team number. For example, information for team 1 in the excel schedule will exist in array index 0, so when you are indexing data types with team number, remember to -1. Same thing applies for game number index
2. Try not to use other packages so people who don't code can use this script with minimal configurations
3. Read the comments in the code, more detail there
4. Contact Anderson if you run into any issues