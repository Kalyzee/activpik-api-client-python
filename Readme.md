Activpik API Client
===================

Manage your medias using Activpik REST API.

Getting started :
=================

You need an client_id and a client_secret. You can contact us to get one.

1/ Instanciate the client

from . import ActivpikClient

c = Client("my_client_id", "my_client_secret")

2/ Upload a media
result = c.add_media("/Users/ludovic/Documents/my_media.mp4", "My Media", "My Media")

get the media_id related to this new uploaded file : result["id"]

3/ Transcribe a media 
transcription_result = c.transcribe_media(result["id"])
get the transcription id  : transcription_result["id"]

4/ Get Transcription status
c.get_transcription_status(transcription_result["id"])

5/ Get all named entities
c.get_timecoded_named_entities()

6/ Get named entities for a media
c.get_timecoded_named_entities_for_media(transcription_result["id"])
