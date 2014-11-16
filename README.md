# HackPrinceton 2014 #
A application for smarter scheduling.

## Datasets ##
TopProf pulls data from various sources like rate my professor, process the data, including comments to produce a set of metrics. Comments are handled by sentiment analysis to gauge how positively or negatively a person feels about a professor. TopProf also parses various Princeton pages to produce a list of courses, in addition to professors teaching them and when they are offered.

## Scheduling ##
TopProf uses all of this information to build a custom schedule, in addition to doing simulations to initialize the models. This data is fed into our calendar interface allowing users to select and deselect classes for their schedule. 
