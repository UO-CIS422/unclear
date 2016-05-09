# unclear
An experiment in using https (unclear == no cleartext) with Heroku

## Why
I want my students to have some experience building applications that, while not highly secure, 
at least don't send confidential over the line as cleartext.  Setting up https on a local 
shared server has lots of problems; student projects can't use the security certificate that we use for 
more controlled parts of our environment.  Since Heroku provides https as a normal part of their 
service (provided we are deploying as foo.herokuapp.com), this seems like a very simple and 
lightweight way to do some very basic security hygiene. 
