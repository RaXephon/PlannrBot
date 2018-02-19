## Inspiration
This idea was more of a challenge for ourselves to do something different in this hackathon in the sense that we wanted to explore new realms of computing, and we found natural language processing a really good choice. Our goal is to create something that is **practical** and **creative**, something that can actually make life easier.

## What it does
PlannrBot converses with the user to help create an itinerary for their upcoming trip using natural language processing and other machine learning algorithms. It also helps you find famous spots around the place the user is visiting and also looks up some local events via some APIs.

## How We built it
We built the project in stages, iteratively working the different components. While one was working on the parser, one was working on the user interface, while one was working on the speech input. After a few rounds of iteration, we converged on the decision to deploy our service as a web app that can take in speech input, which is converted to text via the Google Web Speech API wrapped in a library called Artyom. The text input then is sent to our server which extracts the right information (where you're going, what you're doing, when you're going, etc.) from the text. The NLP parser that is used to do this is actually a combination of a variety of methods that seek to extract individual attributes. For example, we have one algorithm to get time, one to get location, etc. Finally, the response from our service is sent back to the user and read back via using the Artyom.

## Challenges We ran into
Alexa.
It was not working - we tried their way and hacked ways, just wasn't working this time. So we pivoted to making a web interface.

## Accomplishments that We're proud of
We did it! We were able to make a technology that was able to do what we wanted to some extent. We also learned more about nlp and python libraries through all the challenges we ran into.

## What We learned
How difficult NLP is. Most NLP algorithms can't extract Boston as a location from "To Boston" but they can get Boston from "to Boston", i.e. case matters. Order matters. Quantity matters. We want structure to matter, but human speech is inherently so unstructured that no set of regex rules unless infinite could possibly extract all the data. 

## What's next for PlannrBot
We want to transform it into a full web experience, where you interface with the service using voice but the fact that laptops also have a display as opposed to Alexa, information can be shown as you converse with our service.
