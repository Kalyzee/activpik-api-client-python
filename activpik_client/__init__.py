# -*- coding: utf-8 -*-
import requests
import json

"""
    Activpik API Client 
    (c) Kalyzée
"""


class Oauth2ClientCredentialsAuth(requests.auth.AuthBase):
    """Basic Oauth2 Client for Activpik API

    Goal : Retrieve acces_token with given client_id and client_secret
    """

    def __init__(self, access_token_url, client_id, client_secret, grant_type="client_credentials"):
        """Initialise an Oauth2ClientCredentialsAuth

        Args:
            access_token_url: String: Complete url to get access_token
                http://beta.activpik.com/oauth2/access_token/
            client_id : String: User client_id
            client_secret : String: User client_secret 
        """
        self._access_token_url = access_token_url
        self._access_token = None
        self._grant_type = grant_type
        self._client_id = client_id
        self._client_secret = client_secret

    def _request_access_token(self):
        """Request an acces token
        Returns:
            A string : the access_token
        Raises:
            Exception: If the application can't get the access_token
        """
        request_access_token = {
            "grant_type": self._grant_type,
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }
        response = requests.post(
            self._access_token_url, data=request_access_token)
        if (response.status_code == 200):
            self._access_token = response.json()["access_token"]
        else:
            raise Exception("Can't get access token")

    def __call__(self, r):
        if not self._access_token:
            self._request_access_token()
        r.headers["Authorization"] = "OAuth %s" % (self._access_token)

        return r


class ActivpikClient:
    """Activpik Client

    Rest Client using Activpik API to upload and manage media.
    """

    def __init__(self,
                 client_id,
                 client_secret,
                 activpik_urls=(
                 {"base_url": "http://beta.activpik.com", "oauth2_access_token": "/oauth2/access_token/",
                  "list_media": "/api/v1/media/", "get_media": "/api/v1/media/:id/",
                  "list_transcription": "/api/v1/transcription/", "get_transcription": "/api/v1/transcription/:id/",
                  "list_named_entities": "/api/v1/timecoded_entities/",
                  "list_named_entities_by_media": "/api/v1/timecoded_entities/?media__id=:id"
                  })):
        """Initialise an Activpik Client

        Args:
            client_id: Your client ID
            client_secret: Your client Secret
            activpik_urls: A tuple with the url to call
                (
                    base_url : "https://beta.activpik.com",
                    oauth2_access_token : "/oauth2/access_token/",
                                    list_media : "/api/v1/media/",
                                    get_media :  "/api/v1/media/:id/"
                                    get_transcription :  "/api/v1/transcription/:id/"
                                    list_transcription :  "/api/v1/transcription/"
                )
        """
        self._activpik_urls = activpik_urls
        oauth2_access_token_url = "%s%s" % (
            activpik_urls["base_url"], activpik_urls["oauth2_access_token"])

        self._auth = Oauth2ClientCredentialsAuth(
            oauth2_access_token_url, client_id, client_secret)

    def _get_url(self, suffix):
        """
                String to add after base URL
        """
        return "%s%s" % (self._activpik_urls["base_url"], suffix)

    def _get_url_for(self, key):
        """

        """
        return self._get_url(self._activpik_urls[key])

    def add_media(self, file, title, description):
        """Upload media
        Args: 
            file: string: FilePath
            title: string: Media Title
            description: string: Media description

        Returns:
            A media Record
            {
              "broadcast_state": "WA", 
              "created_at": "2014-11-21", 
              "duration": "423.88",
              "encoding_state": "DO",
              "file": "/medias/sources/5d9eae6d-2933-4765-bfa9-691e194d7812.mp4", 
              "hd_available": false, 
              "height": "480.00", 
              "id": 70, 
              "resource_uri": "/api/v1/media/70/", 
              "resume": "",
              "state": "DR",
              "thumbnail": null,
              "title": "Test",
              "updated_at": "2014-11-21",
              "white_mark": false,
              "width": "852.00"
            }
            see http://api.activpik.com/#api-Media-PostMedias
        """            
        files = [('file', (file, open(file, 'rb')))]
        data = {"title": title, "resume": description}

        r = requests.post(
            self._get_url_for("list_media"), auth=self._auth, data=data, files=files)
        print r.text
        if (r.status_code != 201):
            raise Exception("Can't create media")
        else:
            return r.json()

    def get_medias(self):
        """List media and get informations
        Returns:
            A media Record list with status
            { "meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1}, 
              "objects": [
                {
                  "broadcast_state": "WA", 
                  "created_at": "2014-11-21", 
                  "duration": "423.88",
                  "encoding_state": "DO",
                  "file": "/medias/sources/5d9eae6d-2933-4765-bfa9-691e194d7812.mp4", 
                  "hd_available": false, 
                  "height": "480.00", 
                  "id": 70, 
                  "resource_uri": "/api/v1/media/70/", 
                  "resume": "",
                  "state": "DR",
                  "thumbnail": null,
                  "title": "Test",
                  "updated_at": "2014-11-21",
                  "white_mark": false,
                  "width": "852.00"
                }
              ]
            }

            see http://api.activpik.com/#api-Media-GetMedia for details
        """
        response = requests.get(
            self._get_url_for("list_media"), auth=self._auth)
        return response.json()

    def get_media(self, id):
        """Get media informations
        Args: 
            id: Integer: The media ID
        Returns:
            An Media Record with status
            { 
                  "broadcast_state": "WA", 
                  "created_at": "2014-11-21", 
                  "duration": null, 
                  "encoding_state": "WA", 
                  "file": "/medias/sources/5d9eae6dfle.mp4", 
                  "hd_available": false, 
                  "height": null, 
                  "id": 70, 
                  "resource_uri": "/api/v1/media/70/", 
                  "resume": "", 
                  "state": "DR", 
                  "thumbnail": null, 
                  "title": "Test", 
                  "updated_at": "2014-11-21", 
                  "white_mark": false, 
                  "width": null    
            }

            see http://api.activpik.com/#api-Media-GetMedia for details
        """
        url_media = "%s%s" % (self._activpik_urls[
                              "base_url"], self._activpik_urls["get_media"].replace(":id", str(id)))
        response = requests.get(url_media, auth=self._auth)
        return response.json()

    def transcribe_media(self, media_id):
        """Launch an transcription for a given media
        Args: 
            media_id: Integer: The media Id
        Returns:
            An object representing the new record
                {
                  "callback_url": null, 
                  "created_at": "2014-11-21", 
                  "external_id": null, 
                  "id": 36,
                  "media": {
                    "broadcast_state": "WA", 
                    "created_at": "2014-11-21", 
                    "duration": "423.88", 
                    "encoding_state": "DO",
                    "file": "/medias/sources/5d9eae6d-2933-4765-bfa9-691e194d7812.mp4",
                    "hd_available": false,
                    "height": "480.00",
                    "id": 70,
                    "resource_uri": "/api/v1/media/70/",
                    "resume": "",
                    "state": "DR",
                    "thumbnail": null,
                    "title": "Test",
                    "updated_at": "2014-11-21",
                    "width": "852.00"
                    }, 
                  "resource_uri": "/api/v1/transcription/36/",
                  "state": "CR",
                  "updated_at": "2014-11-21"
                }
            see http://api.activpik.com/ for details
        """
        data = {"media": self._activpik_urls[
            "get_media"].replace(":id", str(media_id))}
        headers = {"content-type": 'application/json; charset=utf8'}
        r = requests.post(self._get_url_for("list_transcription"),
                          auth=self._auth, data=json.dumps(data), headers=headers)
        if (r.status_code != 201):
            raise Exception("Can't create transcription")
        else:
            return r.json()

    def get_timecoded_named_entities_for_media(self, media_id):
        """Get Timecoded Named Entities for a given Media
        Args: 
            media_id: Integer: The media Id
        Returns:
            A list of named entities
            {"meta": 
              {"limit": 20, "next": "/api/v1/timecoded_entities/?limit=20&media__id=70&offset=20", "offset": 0, "previous": null, "total_count": 171},
              "objects": [
                {
                  "begin": "2.00", 
                  "end": "5.00", 
                  "id": 2980, 
                  "media": 
                  "/api/v1/media/70/", 
                  "parent_type": "[u'Place', u'PopulatedPlace', u'Country']", 
                  "resource_uri": "/api/v1/timecoded_entities/2980/", 
                  "type": "Place\\PopulatedPlace\\Country", 
                  "value": "français"
                }, 
                {
                  "begin": "2.00", 
                  "end": "5.00", 
                  "id": 2981,
                  "media": "/api/v1/media/70/", 
                  "parent_type": "[u'Person', u'female']", 
                  "resource_uri": "/api/v1/timecoded_entities/2981/", 
                  "type": "Person\\female", 
                  "value": "Clara"
                } 
                ]
            }
            see http://api.activpik.com/#api-Named_Entities-ListNamedEntitiesForVideo for details
        """            
        response = requests.get(
            self._get_url(self._activpik_urls["list_named_entities_by_media"].replace(":id", str(media_id))), auth=self._auth)
        return response.json()

    def get_timecoded_named_entities(self):
        """Get Timecoded Named Entities available for media's owned by current user.
        Returns:
            A list of named entities
            {"meta": 
              {"limit": 20, "next": "/api/v1/timecoded_entities/?limit=20&media__id=70&offset=20", "offset": 0, "previous": null, "total_count": 171},
              "objects": [
                {
                  "begin": "2.00", 
                  "end": "5.00", 
                  "id": 2980, 
                  "media": 
                  "/api/v1/media/70/", 
                  "parent_type": "[u'Place', u'PopulatedPlace', u'Country']", 
                  "resource_uri": "/api/v1/timecoded_entities/2980/", 
                  "type": "Place\\PopulatedPlace\\Country", 
                  "value": "français"
                }, 
                {
                  "begin": "2.00", 
                  "end": "5.00", 
                  "id": 2981,
                  "media": "/api/v1/media/70/", 
                  "parent_type": "[u'Person', u'female']", 
                  "resource_uri": "/api/v1/timecoded_entities/2981/", 
                  "type": "Person\\female", 
                  "value": "Clara"
                } 
                ]
            }
            see http://api.activpik.com/#api-Named_Entities-ListNamedEntitiesForVideo for details
        """    
        response = requests.get(
            self._get_url_for("list_named_entities"), auth=self._auth)
        return response.json()

    def get_transcription_status(self, transcription_id):
        """Get transcription status
        Args: 
            transcription_id: Integer: The transcription
        Returns:
            An Transcription Job Record with status
                {
                  "callback_url": null, 
                  "created_at": "2014-11-21", 
                  "external_id": null,
                  "id": 36,
                  "media": {
                    "broadcast_state": "WA", 
                    "created_at": "2014-11-21", 
                    "duration": "423.88", 
                    "encoding_state": "DO", 
                    "file": "/medias/sources/5d9eae6d-2933-4765-bfa9-691e194d7812.mp4", 
                    "hd_available": false, 
                    "height": "480.00", 
                    "id": 70,
                    "resource_uri": "/api/v1/media/70/", 
                    "resume": "", 
                    "state": "DR", 
                    "thumbnail": null, 
                    "title": "Test", 
                    "updated_at": "2014-11-21",
                    "width": "852.00"
                  }, 
                  "resource_uri": "/api/v1/transcription/36/", 
                  "state": "CR", 
                  "updated_at": "2014-11-21"
                }

            see http://api.activpik.com/#api-Transcription-GetTranscription for details
        """    
        response = requests.get(
            self._get_url(self._activpik_urls["get_transcription"].replace(":id", str(transcription_id))), auth=self._auth)
        return response.json()
