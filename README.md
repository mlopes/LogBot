LogBot
======

A bot that runs as daemon and keeps IRC logs for consulting.

Current Features
----------------

Currently the bot responds to private messages. It recognises the following commands:

- help: Replies with a list of recognised commands
- last n: shows the last n messages on the channel
- find word: shows the messages containing "word"
- date yyyy-mm-dd: show messages from date

Planned Improvements
--------------------

 - Add a sleep between replies to prevent issues with the server cutting longer responses (can be seen if the answer to your query is to big. For example "last 20" might stop before showing all resuts)
 - Improve presentation format of replies containing log data
