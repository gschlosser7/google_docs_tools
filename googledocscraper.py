from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from google.oauth2 import service_account
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import requests
from google.auth.transport.requests import Request
import io
import pdfreader as PdfReader
import json
from apiclient import discovery

# Set doc ID, as found at `https://docs.google.com/document/d/YOUR_DOC_ID/edit`
x = input("input your document id using the format document/d/YOUR_DOC_ID/edit \n")

'''this script requires you to set up authentication with oauth2 for google api
as well as create your own credentials and token json files'''

#dumps jsonified html into a separate file named "googledocoutput.json"
def myfunc(x):
    
    if x==None:
        return print('please enter a doc id')
    # Set doc ID, as found at `https://docs.google.com/document/d/YOUR_DOC_ID/edit`
    #this only works on docs not spreadsheets
    DOCUMENT_ID = x

    # Set the scopes and discovery info
    #SCOPES = "https://www.googleapis.com/auth/drive.file"
    SCOPES = "https://www.googleapis.com/auth/documents.readonly"
    #SCOPES= "https://www.googleapis.com/auth/drive"
    DISCOVERY_DOC = "https://docs.googleapis.com/$discovery/rest?version=v1"

    # Initialize credentials and instantiate Docs API service
    store = file.Storage("token.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build(
        "docs",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
    )

    # Do a document "get" request and output the results as JSON
    result = service.documents().get(documentId=DOCUMENT_ID, includeTabsContent=True).execute()
    output = json.dumps(result, indent=4, sort_keys=True)
    with open('googledocoutput.json', 'w') as outputfile:
        json.dump(output, outputfile)

#check for user input and assign doc id 
if x:
    doc_id=str(x)
else:
    doc_id=None

myfunc(doc_id)   

