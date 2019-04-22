import yaml

with open('E:/python/spider_airpollutants/config.yaml', 'r') as f:
    config = yaml.load(f)

WEBDR = config['WEBDRIVER']
resolution = WEBDR['resolution']
headless = WEBDR['headless']
refresh_wait = WEBDR['refresh_wait']
initial_wait = WEBDR['initial_wait']
zoom_wait = WEBDR['zoom_wait']
retry = WEBDR['retry']
switch_wait = WEBDR['switch_wait']


TASK = config['Task']
delay_max = TASK['delay_max']
schedule = TASK['schedule']