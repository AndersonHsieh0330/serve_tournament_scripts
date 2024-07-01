Some of these functions may not be the most optimum implementation due to specific use cases of SERVE tournament(Or me being lazy), but they should work. Feel free to make pull request to modify the script.

this should work with any # amount of signed up teams as one "team", aka works for both 3ps and reverses or any future tournament formats
# Prereq
Have python installed on ur computer

### How to use

## Note for ppl modifying the script
1. All the indexes to the data types starts from 0, but when they are printed to output file or console the indexes are incremented by one to match team number. For example, information for team 1 in the excel schedule will exist in array index 0, so when you are indexing data types with team number, remember to -1. Same thing applies for game number index
2. Try not to use other packages so people who don't code can use this script with minimal configurations
3. Read the comments in the code, more detail there