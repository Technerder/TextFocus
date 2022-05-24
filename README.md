# TextFocus
A simple and lightweight web application that that tries to get rid of all distractions on web pages displaying articles.

## Known issues
- Websites that dynamically render their text content with Javascript are unable to be displayed (e.g. bloomberg)

## Installation
1. ``git clone https://github.com/Technerder/TextFocus.git textfocus``
2. ``cd textfocus``   
3. ``sudo docker build -t textfocus .``
4. ``sudo docker volume create textfocus-volume``
   - Run the following commands if you get permission errors
   - (docker run --rm --entrypoint id textfocus textfocususer)
   - (docker run --rm -it -v textfocus-volume:/data alpine chown -R 1000:1000 /data)  
5. ``sudo docker run -d --restart=always -v textfocus-volume:/data --name textfocus textfocus``
6. ``sudo docker run -it --rm -v textfocus-volume:/data --name textfocus textfocus``

## Disclaimers
- I suck at web design, and I would like to apologize in advance for the atrocious "design" of all pages.
- The index page looks alright on desktop but not on mobile, and the article view page is the opposite.