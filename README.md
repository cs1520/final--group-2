## Project Description
Our social media application “Acufuncture” will enable users to poke each other as the sole means of intercommunication. Users may set up an account with a distinctive username, search the usernames of individuals they wish to interact with, and poke them as many times as they are able.
The application will utilize the federated server-to-server API provided by ActivityPub in order to search for other users, view their information (e.g., display name, bio, how many times they have been poked), and poke them. Users of other ActivityPub-implementing websites, such as Mastodon, will be able to follow and poke our users in a similar fashion.

## Minimum Viable Product

* Barebones web interface
* Account system with your unique username, changeable display name & bio, and poke count
* Verbatim username search
* Accurate retrievable account information for every successful username search
* Ability to poke that user
* Friends list of your mutually poked users
* Signup and login pages

### Milestone 1 goals (Week 8)

* Design a website interface mockup
* Write HTML boilerplate for different web pages (without most functionality)
    * Search feature: A search bar at the top of each page and a list of your previous searches
    * Account tab: A web page displaying your username, display name, bio, and poke counter (i.e., a counter of how many times the user has been poked by all users)
    * Friends List tab: A web page displaying list of your mutually poked users
    * Login & Sign Up forms (non-functional)
* Write CSS stylesheets to implement mockup design

### Milestone 2 goals (Week 11)

* Implement tab web page functionality
    * Search feature: Exact username match in search bar correctly displays the account page of the corresponding user (if one exists). The page correctly displays your previous searches
    * Account tab: You can change their display name & bio, and a functional poke counter.
* Create signup page and implement functionality
    * You set your email, username, & password for a new account, and then prompted to set up your display name & bio
        * Uniqueness check for username, password hashing
* Implement Friends List tab functionality
    * Correctly displays mutually poked users
    * Possibly implemented using ActivityPub “*Follow*” activity

### Milestone 3 goals (Week 15)

* Implement login and signup functionality
    * You input your username and password to access your existing account
* Limited ActivityPub integration:
    * send/receive [Create activity](https://www.w3.org/TR/activitystreams-vocabulary/#activity-types) & Note objects only - *see* [Mastodon documentation](http://docs.joinmastodon.org/spec/activitypub/)
    * Use [Webfinger](https://tools.ietf.org/html/rfc7033) to resolve remote profile information (e.g. *sending pokes* to @user@another.domain.com)
* Poke suggestion list
* More refined search details (partial name search, etc.)

Links:

[ActivityPub specification](https://www.w3.org/TR/activitypub/)
[Flask-based ActivityPub server](https://github.com/rowanlupton/pylodon)
[Guide for new ActivityPub implementers](https://socialhub.activitypub.rocks/pub/guide-for-new-activitypub-implementers)
[The Flask Mega-Tutorial Part II: Templates](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates) 