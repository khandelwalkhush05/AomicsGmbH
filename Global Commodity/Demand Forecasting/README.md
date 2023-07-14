# Demand forecasting

This folder contains different Demand forecasting scripts that produce results according to the given model used.

## How to start
- Clone the whole repository.
- Go into this folder in your terminal.
- First, navigate to the folder where you have cloned the repository. Now,  go to the desired folder by using the command
  
  ```cd AomicsGmbH/Global Commodity/Demand Forecasting```

  Press ```Tab``` key once and then execute the commands.


## Command for each model

Before proceeding with each model, some model-specific requirements are mentioned below, along with the command to run them.

### RNN
Run the following command before running the file and general Python modules

```pip install darts```

##### Command
```python "path to python file" -e 300 -lr 1e-3 -fcn 24 -fcsrd 10 -fcsrt "20181201" -tl 10 -hdd 20 -d 0 -b 16 -ml 240 -f "path to training file"```

### LSTM
Run the following command before running the file and general Python modules

```pip install darts```
##### Command
```python "path to python file" -e 300 -lr 1e-3 -fcn 24 -fcsrd 10 -fcsrt "20181201" -tl 10 -hdd 20 -d 0 -b 16 -ml 240 -f "path to training file"```

### Prophet
Run the following command before running the file and general Python modules

```pip install pandas matplotlib numpy cython```

```pip install pystan```
##### Command
```python "path to python file" -f "path to training file" -ttl "date till training" -tst "date when prediction starts"```

