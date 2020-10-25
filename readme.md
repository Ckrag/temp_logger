# Temperature Tester
<p>A small script that logs temperature (and more) and outputs day-by-day logfiles, using 
<a href="https://shop.pimoroni.com/products/bme680-breakout">bme680-breakout</a>.
<p>Logfiles are stored in logs/ at the root of the project. Each log contains one day, and each line is a json-string
containing information about a single log.</p>

<h3>Dependencies</h3>

```
curl https://get.pimoroni.com/i2c | bash           # pi config
sudo apt install python-smbus python3-smbus
pip install -r requirements.txt
```
<h3>Running</h3>
<p>Run the script</p>

```./temp_logger.py```
<p>Options</p>

```./temp_logger.py <log interval> <host> <basic_auth_user> <basic_auth_pass>```
