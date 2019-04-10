# development log

##2019-4-10
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