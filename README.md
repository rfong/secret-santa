secret santa
=====
Randomly generate a single cycle through a specified group of people, and 
automatically send out assignment emails so that you, the organizer, can 
retain the joy of surprise upon discovering your own Secret Santa.

"Features"
-----
+ pairwise blacklisting option to spice things up (because it's less fun for
people to get assigned to their significant others or some other player's
relative they've never met)
+ list player addresses & roommates so secret santas can collaborate with each
other to hide presents in each others' houses

What to do
-----
Set up your sender email in `config.py`.

Run `python secret_santa.py --fake sample_people.json` to generate a sample
cycle without actually sending emails.

Write valid JSON.

Assumptions
-----
+ names specified are unique and consistent
+ there exists at least one possible cycle, i.e. you don't overconstrain 
the blacklists; if no cycles are possible, the algorithm is dumb and runs
forever
