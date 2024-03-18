The intention of doing this project was to practice and create a useful tool for myself.\
\
Let's say we want to implement a trading bot that learns from the patterns in previous data. For the implementation of such trading bot, we need to always keep our historic price datasets up-to-date to learn from the most recent patterns.\
\
This project helps us by automatically updating our local datasets. By running `update_dataset.py -update`, the Python script checks the last element of our local dataset. Afterwards, it downloads, reformats, and appends the new data to our local dataset. \
\
In order to directly test the code and see how it works, I created the `dataset-5m.csv` file, which contains 5-minute candlesticks of Binance spot BTCUSDT from February 2024. This data, along with all other data that this project downloads, is from https://data.binance.vision. \
\
To further understand how the code works, I kindly ask you to go through the Python files and read the comments at the beginning of each file and function.