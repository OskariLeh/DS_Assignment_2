from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import datetime
import requests

def addData(topicName, noteName, text):
    tree = ET.parse("db.xml")
    root = tree.getroot()
    now = datetime.datetime.now()
    topicElement = None
    
    for topic in root.iter("topic"):
        name = topic.get("name")
        if (name == topicName):
            topicElement = topic
            newNote = ET.SubElement(topicElement, "note", name=noteName)
            newText = ET.SubElement(newNote, "text")
            newTimestamp = ET.SubElement(newNote, "timestamp")
            newTimestamp.text = "{0}/{1}/{2} - {3}:{4}:{5}".format(now.month, now.day, now.year, now.hour, now.minute, now.second)
            newText.text = text
            tree.write("db.xml")
            return "Added to existing topic"
    
    # Check if this topic alredy exists if not it will be created
    if topicElement == None:
        newEntry = ET.Element("topic", name=topicName)
        newNote = ET.SubElement(newEntry, "note", name=noteName)
        newText = ET.SubElement(newNote, "text")
        newTimestamp = ET.SubElement(newNote, "timestamp")
        newTimestamp.text = "{0}/{1}/{2} - {3}:{4}:{5}".format(now.month, now.day, now.year, now.hour, now.minute, now.second)
        newText.text = text
        root.append(newEntry)
        tree.write("db.xml")
        return "Added new element to database"
        
# Gets data from xml document, returns list of dictionaries containing data.        
def getData(topicName):
    data = []
    tree = ET.parse("db.xml")
    root = tree.getroot()
    for topic in root.iter("topic"):
        name = topic.get("name")
        if (name == topicName):
            for note in topic.iter("note"):
                dataEntry = {"name": note.get("name"), "text": note.findtext("text"), "timestamp": note.findtext("timestamp")}
                data.append(dataEntry)    
    
    return data
    
# Gets wikipedia link for given topic   
def getWikipediaData(topicName):
    data = ""
    s = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "namespace": "0",
        "search": topicName,
        "limit": "1",
        "format": "json"
    }
    
    r = s.get(url=URL, params=params)
    data = r.json()
    
    return data[3][0]    

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(addData, "addData")
    server.register_function(getData, "getData")
    server.register_function(getWikipediaData, "getWikipediaData")
    server.serve_forever()