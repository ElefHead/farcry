# FARCRY
This project is aimed at visualising the longitudinal impact of cancer center funding patterns on state cancer rates over the years and has be given the acronym - FARCRY. We are working with Dr. Katherine Tossas-Milligan and our main clients are cancer center leadership, administrators, staff and researchers. The aim is to achieve more granularity on this application and an eventual visualization for the general public. 

## Application
We have developed an application that visualizes the cancer mortality (or age-adjusted death rate) for each state by year (2000 - 2015). This application also pinpoints the location of each comprehensive cancer center in USA and some basic and clinical cancer center. The user has the option to use a slider to set the year and click on button to resize the states by their funding amounts.  
The choropleth on the landing page visualizes 5 variables:
1. Latitude
2. Longitude
3. Mortality
4. Funding
5. Time

Upon clicking on a state, the application zooms in to visualize the average age-adjusted death rate over 2011 - 2015 for each county in that state. It also reveals demographic information such as the mortality by gender, by race-ethnicity and the funding as compared to mean funding for each state from 2000-2015. All the time-series graphs can be filtered using the labels below.

## Details 
* This visualization shows the age-adjusted cancer death rate for each state over the years 2000-2015.
* The slider can be used to change the year; it only affects the state data on the zoomed-out map that shows all of USA.
* The county data is not year-wise. It is the 5 year average (2011-2015) age-adjusted death rate.
* The funding data is expressed in dollars per 1,000.
* The blue dots show the following:
  * The dark blue dots show Comprehensive cancer center.
  * The blue dots show Clinical cancer center.
  * The light blue dots show Basic cancer center.
* The timeseries graphs that display trends for a specific state can be filtered using the labels.

## Acknowledgements
We would like to thank [Dr. G. Elizabeth Marai](https://www.evl.uic.edu/marai/), the [Electronic Visualization Laboratory](https://www.evl.uic.edu/) and [University of Illinois at Chicago](https://www.uic.edu/) for the graduate course “Visual Data Science” and particularly Dr. Marai for structuring the course in a way to provide students with opportunities to work on real problems with clients, and providing much required guidance throughout the way. 

We also thank [Dr. Katherine Tossas-Milligan](https://www.linkedin.com/in/katherinetossasmilligan/) and [UI Cancer Center](https://cancer.uillinois.edu/) for their passionate collaboration and guidance.   

Further, we thank our course teaching assistant [Peter Hanula](https://www.evl.uic.edu/entry.php?id=2251) for his constant help and support.  

Finally, we thank our course-mates for their feedback at every step of the process.  
