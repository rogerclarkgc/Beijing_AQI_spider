# development log

## 2019-4-10
It seems the elements of page are changed when i 
try to use the chromedriver to click the air station 
points in the map


        task.click.screenshot(point_list[0]. "0.png")
        task.click.screenshot(point_list[0]. "0.png")
       
the results of code above are different

# solve it !!!

* plan A: refresh the page after each `click_screenshot` task

yes, i add the code in the test module to refresh the page, it seems some 
of the repeat results were fixed, but there are 3 points still return wrong result (same results)
After check the station map, i found these 3 points are very close in the map, maybe the i should 
change the css-selector to fit this narrow space between these points.

* plan B: use multi-threading, each threading a independent

 
* plan C: the mix of plan A & plan B, considering the balance of speed and resource usage

## 2019-4-11

Still try to fix the "repeat results" problem in plan A

Some useful information:

1. the backend of the map server may have some useful API to 
handle the map, such as zoom in \ zoom_out\drag

2. use keyboard to handle the map, because it's easy to send specific
keys to Chromedriver

3. find another selector to solve the repeat problem

    摸 鱼 一 天
    
## 2019-4-12

I've fix the "repeat results" bug in the screenshot module by using the 
`map.setZoom()` API, which support by the gis supporter. But A new problem has
encounter by the screenshot module. that is, if i run the code in a serialized 
mode, then the cost of time is un-acceptable. (7 pollutants, each has 34 monitor points,
that means half hour for data acquire!). So i decide to use multi-threading method to 
boost the process of data acquire and here are some problem need to solve

1. how many thread i should use, if i open two much thread, the web server of bjmemc may ban 
my ip, that's a risk
    try proxy pool??
    or just cut down the numbers of thread?

2. how to connect and transport the params of the screenshot task, each task has different 
task parameters.


## 2019-4-13

write a multi threading model, when a sub thread is called by main thread, a `time.sleep(seconds)`
is called to prevent two much connect request to the bjmemc server

## 2019-4-15

i've found it's difficult to use the tesseract to recognize the characters in the screenshot (results unstable, too much 
parameters to handle)

so i decided to use old school html parser method (base on bs4) to screen data from the page, it works well. but this 

method may still cost a lot of time in the long-term maintenance.

## 2019-4-18

work for data module now, use monogo database to store the air data.

## 2019-4-19

try to use celery to run the spider every 30 minutes, unknown bugs had
encountered, don't know how to fix it. 

## 2019-4-20-2019-4-22
use a lightweight schedule module to replace celery, run the stable test,
and add more function in the `DataDrawer` module
