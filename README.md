# NetworkAnalyzerGoogleCloud
Google cloud base auto scaling project for network analyzer that uses a-star to search for most cost effective path to attack a network

useful links:

python library
https://cloud.google.com/compute/docs/tutorials/python-guide

pub-sub
https://cloud.google.com/pubsub/docs/quickstart-client-libraries#pubsub-client-libraries-python

auto scaling
https://cloud.google.com/compute/docs/autoscaler/
https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances
https://cloud.google.com/compute/docs/instance-templates/
https://cloud.google.com/blog/products/gcp/queue-based-scaling-made-easy-with-new-stackdriver-per-group-metrics
https://cloud.google.com/monitoring/api/resources

driver:
https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32

autoscaling flow control issue
https://github.com/googleapis/google-cloud-python/issues/4912



Driver
create_graph: function generates a two-dimensional graph with nodes assigned a random vulnerability. as Explained earlier also, these would be actual vulnerabilities existing on a node when a real user uploads the graph of their actual network.


send_request: function is responsible for sending asynchronous HTTP requests to the app using aiohttp library, waiting for the response and showing the results related to the respective request.

App

receive_request: This method takes the requests sent to the server over the internet. Creates a JSON object and passes that to publish method.

publish: This method publishes the JSON object on the pub/sub queue and generates a message id passed to check for output method.

check_for_output: Polls the storage bucket for output matching the message id received from publishing method.

Worker
subscribe: This method makes this code a subscriber to pull messages published on the queue. A single subscriber can process multiple requests in parallel.

get_score: this method takes cve-id as input and searches the NVD database extracts the CVSS score normalizes it dividing by 10 to make it a probability of compromising the node.
	  
get_cost: this method randomly assigns cost related to compromising a node on the network by exploiting the vulnerability present on the system. In reality, this can be done using open source databases that contain the costs associated with exploits. creating such DB is a novel idea in its and a good project to consider in future but beyond the scope of this project.

get_exp_time: similar to get_cost  method this routine assigns time-needed to exploit a vulnerability.

graph_from_json: creates the networkx graph object to be processed by ai algorithm a-star from JSON message pulled from the queue.

get_heuristic_cost: this method is from an ai concept where the estimated distance to the goal node is used to determine which node to explore next on the given graph. The heuristic function will return the estimated distance cost from the current node to the target node. For this project, it is  Manhattan distance.

a_star: is a graph search algorithm which considers all the paths to find the best possible path to reach the goal node. For choosing which node to explore next, it considers the most promising path depending on the factors like cost, time and probability in addition to heuristic mentioned above.

