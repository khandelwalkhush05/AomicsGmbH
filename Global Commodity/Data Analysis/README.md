# Data Analysis

This folder contains different data analysis scripts that produce results according to the given task.

## How to start
- Clone the whole repository.
- Go into this folder in your terminal.
- First, navigate to the folder where you have cloned the repository. Now,  go to the desired folder by using command
  
  ```cd AomicsGmbH/Global Commodity/Data Analysis```

  Press ```Tab``` key once and then execute the commands.


## Command for each task
There are certain flags used in the commands,
- -re is the country from which goods are exported
- -pa is partner country
- -cat is catogory
- -y is year
- -o makes a new pdf file of the name mentoined in front of it


Command is:

```python <path to python script> -f <dataset> -re <country 1> -pa <country 2> -cat <category> -y <year> -o <file name>```

### Task 2 
```python task2.py -f TradeDataFinal.csv -re GERMANY -pa CHINA -cat 61 -y 2019 -o new2.pdf```

### Task 3 
```python task3.py -f TradeDataFinal.csv -re GERMANY -pa CHINA -cat 61 -y 2019 -o new3.pdf```

### Task 4 
```python task4.py -f TradeDataFinal.csv -re INDIA -pa FRANCE -ocsv trade.csv```

### Task 5 
```python task5.py -f TradeDataFinal.csv -re GERMANY -pa CHINA -o new5.pdf```

### Task 6 
```python task6.py -f TradeDataFinal.csv -re GERMANY -pa CHINA -o new6.pdf```
