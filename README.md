# WBMBOT
A simple selenium based python bot to check the website of WBM Wohnungsbaugesellschaft Berlin-Mitte mbH for new flats and automatically apply for them, since only the first 1000 applicants will be considered in the random selection process for apartment viewing.

# Getting started
To install all dependencies you can use the [`conda`](https://docs.conda.io/en/latest/) package manager and create an environment from the `environment.yaml` file located in the project directory as follows:
```
# create conda environment form environment file
conda env create -f environment.yaml

# activate conda environment
conda activate wbmbot
```
If you don't have `conda` installed I recommend installing it or installing all dependencies manually (good luck with that). Alternatively you can install the dependencies using `pip`, since all of them should be available on there too.


To start the bot simply run the below command in your terminal in the project directory:
```
python3 main.py
```

If you are running the bot for the first time the bot will start the setup process asking all the necessary information for applications on wbm.de.
Note that these informations will be saved unencrypted to a local `config.yaml` file in *human readable* format!!
If you don't want to use the setup process for this, you can just create a `config.yaml` file yourself in the project directory of format:

```
city: "cityname"
email: "email@adress"
first_name: "Max"
last_name: "Mustermann"
phone: "0123456789"
street: "Streetname 42"
wbs: "yes"
wbs_date: "23/04/1972"
wbs_num: "WBS 160"
wbs_rooms: '2'
zip_code: '12345'
```

# Filtering
Currently the bot will apply to all available flats on the WBM website, which most of the time is only like one per every 3 days anyway..
However a filtering feature is planned and will (probably) be implemented soon.

# Additional
The bot will save all successfull applications to a `log.txt` file. This file is also used to apply to every flat only once, so don't delete it unless you want to reapply to all available flats!
Per default wbm.de will be reloaded and checked for new flats every 5 minutes. There currently is no timeout or bot check / captcha on the website (lets hope it stays like this), but I dont think its necessary to check more often, as there are not many flats available anyway (in contrast to e.g. immoscout24).

Let the hunt begin! Good luck!
