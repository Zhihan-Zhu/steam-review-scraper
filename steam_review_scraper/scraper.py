from datetime import datetime as dt

import requests
import pandas as pd
from bs4 import BeautifulSoup

current_year = dt.today().year
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

def get_review_count(id):
    """Return total number of reviews of default language.

    Args:
        id (int or str): Game id.

    Returns:
        int: Number of reviews.
    """    

    url = 'https://store.steampowered.com/app/' + str(id)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    count = soup.find('label', {'for': 'review_language_mine'}).span.text
    count = count.strip('()').replace(',','')
    return int(count)


def search_game_id(search_term, all_results=False): 
    """Return Dataframe of game ids of the search term from Steam's search result page.

    Args:
        search_term (str): Game name to search.
        all_results (bool, optional): Whether to return all games results of the search term or the top one result. Defaults to False.

    Returns:
        Dataframe: Dataframe with two columns "game" and "id".
    """    
    page = 1
    game = []
    id = []
    if not all_results:
        url = f'https://store.steampowered.com/search/?category1=998&page={page}&term={search_term}'
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        search_results = soup.find(class_='search_result_row')
        game = search_results.find('span', class_='title').text
        id = search_results['data-ds-appid']
        return pd.DataFrame({
            'game':[game],
            'id':[id]
        })
    else:
        while True:
            url = f'https://store.steampowered.com/search/?category1=998&page={page}&term={search_term}'
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')
            search_results = soup.find_all(class_='search_result_row')
            if not search_results:
                break
            
            title = [result.find('span', class_='title').text for result in search_results]
            appid = [result['data-ds-appid'] for result in search_results]
            game.extend(title)
            id.extend(appid)
            page += 1
        
        return pd.DataFrame({
            'game':game,
            'id':id
        })


def get_game_ids(n, filter='topsellers'):
    """Return Dataframe of n games' ids from Steam's search result page.

    Args:
        n (int): number of games to collect.
        filter (str, optional): filter for search results. Defaults to 'topsellers'.

    Returns:
        Dataframe: Dataframe with two columns "game" and "id".
    """    
    page = 1
    game = []
    id = []
    while len(game) < n:
        url = f'https://store.steampowered.com/search/?category1=998&page={page}&filter={filter}'
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        search_results = soup.find_all(class_='search_result_row')
        if not search_results:
            break
        
        title = [result.find('span', class_='title').text for result in search_results]
        appid = [result['data-ds-appid'] for result in search_results]
        game.extend(title)
        id.extend(appid)
        page += 1
    num = min(n, len(game))
    return pd.DataFrame({
        'game':game[:num],
        'id':id[:num]
    })

def clean_date(date):
    """Helper function to clean review date pulled from Steam's review page for a game.

    Strip 'Posted: ' from the date string.
    Add current year to date if review was posted in the current year.

        Typical usage example:
        >>> clean_date('Posted: May 6')
        'May 6, 2021'

    Args:
        date (str): Date string pulled from review page.

    Returns:
        str: Clean date string.
    """    
    date = date.split(' ',1)[1]
    try: 
        dt.strptime(date,'%B %d, %Y')
        pass
    except ValueError:
        date += ', ' +str(current_year)
    return date


def get_game_review(id, language='default'):
    """Collect all review for a given game.

    Typical usage example:

    English reviews for Counter-Strike: Global Offensive.
    Game id can be found using search_game_id("Counter-Strike: Global Offensive")
    or from game's Steam page url.
    >>> reviews = get_game_review(730, language='english')

    Args:
        id (int or str): Game id 
        language (str, optional): The language in which to get the reviews. Defaults to 'default', 
            which is the default language of your Steam account.

    Returns:
        Dataframe: Dataframe for reviews with the following columns:

        | name                | description                                           | dtype   |
        |---------------------|-------------------------------------------------------|---------|
        | user                | user name of the review                               | object  |
        | playtime            | total playtime (in hours) the user spent on this game | float64 |
        | user_link           | user's profile page url                               | object  |
        | post_date           | review's post date                                    | object  |
        | helpfulness         | number of people found this review helpful            | int64   |
        | review              | review content                                        | object  |
        | recommend           | whether the user recommend the game                   | object  |
        | early_access_review | whether this is an early access review                | object  |
            """    
    user_name_list = []
    hour_list = []
    user_link_list = []
    post_date_list = []
    helpful_list = []
    comment_list = []
    title_list = []
    early_access_list = []

    cursor = ''
    i=0
    while True:
        url=f'https://steamcommunity.com/app/{id}/homecontent/'
        params = {
            'userreviewsoffset': i  * 10,
            'p': i + 1,
            'workshopitemspage': i + 1,
            'readytouseitemspage': i + 1,
            'mtxitemspage': i + 1,
            'itemspage': i + 1,
            'screenshotspage': i + 1,
            'videospage': i + 1,
            'artpage': i + 1,
            'allguidepage': i + 1,
            'webguidepage': i + 1,
            'integeratedguidepage': i + 1,
            'discussionspage': i + 1,
            'numperpage': 10,
            'browsefilter': 'toprated',
            'browsefilter': 'toprated',
            'appid': id,
            'appHubSubSection': 10,
            'l': 'english',
            'filterLanguage': language,
            'searchText': '',
            'forceanon':1,
            'maxInappropriateScore':50,
        }
        if i > 0:
            params['userreviewscursor'] = cursor
        html = requests.get(url, headers=headers, params=params).text
        soup = BeautifulSoup(html, 'html.parser')
        reviews=soup.find_all('div', {'class': 'apphub_Card'})
        
        if not reviews:
            break
            
        users = [review.find('div', {'class': 'apphub_CardContentAuthorName'}) for review in reviews]
        user_name = [user.find('a').text for user in users]
        user_link = [user.find('a').attrs['href'] for user in users]
        title = [review.find('div', {'class': 'title'}).text for review in reviews]
        hour = [float(review.find('div', {'class': 'hours'}).text.split(' ')[0]) if review.find('div', {'class': 'hours'}) 
                else np.nan for review in reviews]
        helpful = [review.find('div',{'class': 'found_helpful'}).get_text(strip=True).split(' ')[0] for review in reviews]
        helpful = [0 if num == 'No' else int(num) for num in helpful]
        comment_section = [review.find('div', {'class': 'apphub_CardTextContent'}) for review in reviews]
        raw_post_date = [x.find('div',{'class':'date_posted'}).get_text(strip=True) for x in comment_section]
        post_date = [clean_date(date) for date in raw_post_date]
        comment = [''.join(review.find_all(text=True, recursive=False)).strip() for review in comment_section]
        early_access = [x.find('div',{'class': 'early_access_review'}).text if x.find('div',{'class': 'early_access_review'}) 
                        else None for x in comment_section]
        # A response includes a ‘userreviewscursor’ attribute, marking which review your request completed on. 
        # Adding same cursor in the next request’s parameters to get the next 10 reviews. 
        # Otherwise it will return the same 10 reivews as last request.
        cursor = soup.find_all('form')[0].find('input',{'name': 'userreviewscursor'})['value']

        user_name_list.extend(user_name)
        hour_list.extend(hour)
        user_link_list.extend(user_link)
        post_date_list.extend(post_date)
        helpful_list.extend(helpful)
        comment_list.extend(comment)
        title_list.extend(title)
        early_access_list.extend(early_access)
        i += 1

    review_df=pd.DataFrame({
        'user': user_name_list,
        'playtime': hour_list,
        'user_url': user_link_list,
        'post_date': post_date_list,
        'helpfulness': helpful_list,
        'review': comment_list,
        'recommend': title_list,
        'early_access_review': early_access_list
    })
    return review_df