# SmartMarks (http://www.smartmarks.co/)

SmartMarks is a web application and browser extension which attempts to replace current browser bookmarking with a better alternative. The basic idea is that current browser bookmarking is useless because you usually do not remember to bookmark a site that could be useful later and when you do it gets lost among the many other bookmarks you have. SmartMarks attempts to make bookmarking a thing of the past. It does this by remembering every site you visit and then using different data about the sites to make searching your history extremely easy.

## Current State

Right now SmartMarks is a WIP. There is a Chrome Extension and the web application to view and search your Marks. Currently the search only allows you to search by website title and only improves on browser history search by only showing one result for each individual URL visited.

## Future Plans

I plan to continue to build out SmartMarks to make finding a website you visited but forgot the URL for very easy. To do this I plan to gather information like meta data and crawling user's history. To see what exact steps I plan to take next check out the [issues page](https://github.com/srmor/smartmarks/issues).

## Technologies Used

* Python
* Flask
* MongoDB
* Javascript
* jQuery
* Bootstrap

## Technology plans

I am planning to remove Bootstrap and create a better brand design in the near future. I will also be transitioning the site from being a multi-page Python site to being a Python API with Backbone.js or Ember.js handling the frontend. I also plan to use Redis to help with queuing for crawling users history items as they visit pages. Also, the CSS is currently badly organized and will get a re-write once I remove Bootstrap and I will rewrite it in Sass.
