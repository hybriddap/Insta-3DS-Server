import requests
from flask import Response

def get_facebook_page_id(access_token):
    #Retrieve facebook page id data from Meta's API
    url = f'https://graph.facebook.com/v22.0/me/accounts?access_token={access_token}'
    response = requests.get(url)
    #return Response({'message':response,'access_token':access_token,'status':status.HTTP_200_OK})
    if response.status_code != 200:
        # Handle error response
        return None
    metasData = response.json()
    if not metasData.get("data"):
        return None
    #else return the page id
    return metasData.get("data")[0]["id"]

def returnInstagramDetails(facebookPageID,access_token):
    url = f'https://graph.facebook.com/v22.0/{facebookPageID}?fields=instagram_business_account&access_token={access_token}'
    response = requests.get(url)
    data=response.json()
    if response.status_code != 200:
        # Handle error retrieving insta account id   
        return None
    insta_account_data = data.get("instagram_business_account")
    if not insta_account_data:
        return None #return error if no instagram account found
    return insta_account_data.get("id") #return the instagram account id

def publishToFacebook(facebookPageID, token, caption, image_url):
    #Get page access token
    url = f'https://graph.facebook.com/v22.0/me/accounts?access_token={token}'
    
    response = requests.get(url)
    if response.status_code != 200:
        # Handle error response
        return Response(response=f"Unable to retrieve page access token. {response.text}", status=500)
    
    metasData = response.json()
    if not metasData.get("data"):
        return Response(response="Unable to retrieve page access token 2", status=500)
    
    #Get the page access token
    page_access_token = metasData.get("data")[0]["access_token"]
    
    # Create media object for Facebook
    url = f'https://graph.facebook.com/v22.0/{facebookPageID}/photos'
    data = {
        "url": image_url,
        "message": caption,
        "access_token": page_access_token
    }

    response = requests.post(url, data=data)
    if response.status_code != 200:
        # Handle error response
        return Response(response=f"Unable to create Media Obj for Facebook. {response.text}", status=500)
    
    media_data = response.json()
    if not media_data.get("post_id"):
        return Response(response="Unable to retrieve post ID", status=500)
    
    post_id = media_data.get("post_id")

    #Get URL to the post
    url = f'https://graph.facebook.com/v22.0/{post_id}?fields=permalink_url&access_token={page_access_token}'
    
    response = requests.get(url)
    if response.status_code != 200:
        # Handle error response
        return Response(response="Unable to get post url", status=500)
    
    post_data = response.json()
    if not post_data.get("permalink_url"):
        return Response(response="Unable to retrieve post url from json", status=500)
    
    post_url = post_data.get("permalink_url")
    
    return Response(response=f"{post_url}", status=200)


def publishToInsta(facebookPageID,token,caption,image_url):
    #Create media object
    # Get the Instagram account ID
    instagram_account_id = returnInstagramDetails(facebookPageID,token)
    if not instagram_account_id:
        return Response(response="Unable to retrieve Instagram Account ID!", status=500)
    
    url = f'https://graph.facebook.com/v22.0/{instagram_account_id}/media'
    data = {
        "image_url": image_url,
        "caption": caption,
        "alt_text": "This is the alt text for the image",
        "access_token": token
    }

    response = requests.post(url, data=data)
    if response.status_code != 200:
        # Handle error response
        return Response(response=f"Unable to create Media Obj. {response.text}", status=500)
    media_data = response.json()
    if not media_data.get("id"):
        return Response(response="Unable to retrieve media ID", status=500)
    media_id = media_data.get("id")

    #Publish the media object
    url = f'https://graph.facebook.com/v22.0/{instagram_account_id}/media_publish?creation_id={media_id}&access_token={token}'
    response = requests.post(url)
    if response.status_code != 200:
        # Handle error response
        return Response(response=f"Unable to publish media obj. {response.text}", status=500)
    publish_data = response.json()
    if not publish_data.get("id"):
        return Response(response="Unable to retrieve publish ID", status=500)
    post_id = publish_data.get("id")
    #Get the link to the post
    url = f'https://graph.facebook.com/v22.0/{post_id}?fields=permalink&access_token={token}'
    response = requests.get(url)
    if response.status_code != 200:
        # Handle error response
        return Response(response="Unable to get post url", status=500)
    post_data = response.json()
    if not post_data.get("permalink"):
        return Response(response="Unable to retrieve post url from json", status=500)
    post_url = post_data.get("permalink")
    # Return the post ID
    return Response(response=f"{post_url}", status=200)


def publishToMeta(platform, token, caption, image_url):
    facebookPageID = get_facebook_page_id(token)
    if not facebookPageID:
        return Response(response="Unable to retrieve Facebook Page ID! Make sure your Access Token is correct and isnt expired!", status=500)

    #For Facebook
    if platform == 'facebook':
        return publishToFacebook(facebookPageID,token,caption,image_url)

    #For Instagram
    return publishToInsta(facebookPageID,token,caption,image_url)