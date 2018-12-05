# krispyKernels
## Cheryl Qian, Derek Chan, Kendrick Liang, Simon Tsui

#### Krispy Tickets
A site for accessing concerts and musical events within a location range. Includes detailed information on each event, including directions to the venue, and weather on the day of. Information on artists (albums, biography) in the lineup of each event is also available. Users can register and save artists and events of their choosing.

#### Instructions to Runs
1. Clone our Repo:
    - To clone with SSH, enter ` git clone git@github.com:cqian2019/krispyKernels.git ` into terminal
2. Virtual Environment
    - Activate your python virtual environment if you already have one. If not, create one by entering
    - ` python3 -m venv <name-of-venv> `  
    - Enter ` . <path>/<name-of-venv>/bin/activate `  to activate.
3. Install Dependencies
    - ` pip install -r requirements.txt ` will install all necessary packages into your venv.
4. Launch with ` python app.py ` in terminal.
5. Open a new browser window and enter ` localhost:5000 ` into address bar to visit our home page.
**6. Insert API Keys into their respective files**
In the root of our directory there should be 4 .txt files named according to their API.
Procure keys, paste each in their respective files as shown below:
```
Insert API key for <INSERT API NAME HERE> in line below:
< INSERT API KEY HERE>
```

#### Procuring API Keys
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
