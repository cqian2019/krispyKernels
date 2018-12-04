# krispyKernels
## - Yin On Chen, Kendrick Liang, Cheryl Qian, Simon Tsui

Project 01: ArRESTed Development

#### Overview

krispyKernels here delivering all your concert outing needs! We make calls to TicketMaster, The Audio DB, Public Transit, and NightSky API's. Users can look for events and info such as performing artists, genre of music, etc... Directions and weather available.


#### Instructions to Runs
1. Clone our Repo:

2. Virtual Environment: Starting from Scratch
  - ''' python3 -m venv venv '''  <makes virtual environment>
  - . venv/bin/activate  <launches virtual environment>
  - pip install ____  <Requirements: Flask, request>

3. python app.py to run the Flask server

4. Home page can be accessed on localhost:5000

5. As of now, all of our API keys are still in the python files so no accessing will be required.

#### Dependencies
- Public Transit API
  - Procure an API key [here](https://developer.here.com/documentation/transit/topics/quick-start-routing.html). Click on the "Get Started for Free button". Email registration required.
  - API is used to provide directions using public transit only.
- Dark Sky API
  - Procure an API key [here](https://darksky.net/dev). Email registration required.
  - API is used to provide information on the weather the day of an event.
- TicketMaster API
  - Procure an API key [here](https://developer-acct.ticketmaster.com/user/register). Email registration required.
  - API is used to provide event information such as: location, show name, lineups, and dates.
- TheAudioDB API
  - Procure an API key [here](https://www.theaudiodb.com/api_guide.php). Click on the register button. Email registration required.
  - API is used to provide information on the artist. Their albums, bios, and tracks.
