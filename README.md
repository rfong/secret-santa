secret santa
=====
Randomly generate a single cycle through a specified group of people, and 
automatically send out assignment emails so that you, the organizer, can 
retain the joy of surprise upon discovering your own Secret Santa.

Run `python secret_santa.py -f sample_people.json` to generate a sample cycle
without actually sending emails.

Set up your sender email in `config.py`.

Assumptions
-----
+ names specified are unique and consistent
+ there exists at least one possible cycle, i.e. you don't overconstrain 
the blacklists; if no cycles are possible, the algorithm is dumb and runs
forever
+ your JSON is valid
