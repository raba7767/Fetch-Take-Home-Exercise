# Fetch-Take-Home-Exercise

Endpoint Availability Monitor

How to Run: 

    - Open a command prompt
    - Install dependencies: pip install -r requirements.txt
    - Start the script: python monitor.py config.yaml
    - Replace config.yaml with the path to your YAML config file.

Changes made to prompt file:  

  - Move "import sys" to top of file with rest of imports. Discovered in first file lookover
  - Add defaults to "method, "header", and body. Looking over code requirments confirms the missing defaults, also best practice to have a default
  - Added 500ms timeout to request. Looking over code requirments confirms this need, but missing from original. Also a very important practice to avoid getting hung on one bad request.
  - Import a new library to help better and cleanly parse domains. Original method was not great but seemed to work in this example. Change needed when looking over requirments and need to ignore port numbers.
  - Adjust the 15 second sleep time to take into account how long the health check took. Spotted in first lookover, likely the biggest issue with original code. The new method is not 100% perfect depending on how long the list of domains we are checking, it is possible it takes longer than 15 seconds to check them all, in which case it will run as frequently as it can but may exceed 15 seconds. Requirments state to run every 15 second regardless of number of endpoints and response times, so another possible solution is to implement multiple threads. But given a large enough list this too will eventually use all available threads and then take longer than 15 seconds. I believe it is better to take a practical approach to this problem, given the abstract nature. 

