This project comprises a Python program that captures data
from Deriv.com via the website's API. The data is then
stored in a local database using Python's sqlite3 module. At
the moment, the goal is to create a GUI application that
would allow the user to set the parameters of the data they
want to download, including currency pair, start time, end
time, time zone.

## Project Status

The project is in its early days, so what's available right
now is the script for downloading the data from Deriv and
storing it in the database. No GUI yet.

## Key Concepts

-   Concurrency - Achieved through the `asyncio.gather()`
    method. The program downloads multiple batches of data
    at a time, instead of just one. After some
    experimentation, I determined that running 12 tasks
    gives optimal results.

## How to run it

You'll need to do the following before you use this program:

1. Ensure Python is installed in your machine. If not,
   follow the installation instructions in the following
   link: https://www.python.org/about/gettingstarted/
2. Install required libraries. You can do this by running
   this command in a terminal opened in the root folder of
   the project:

    ```
    pip install -r requirements.txt

    ```

3. Create a Deriv.com account, and create an application
   here: https://api.deriv.com/dashboard
4. Use your app ID in the following line in the run.py file:

```python
appid = os.environ["DERIV_APP_ID"]
```

5. Now, you can run the project by running the following
   command in a terminal opened in the root folder of the
   project:

```
python run.py
```

## Next Step

Creating a Graphical User Interface.
