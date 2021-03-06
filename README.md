# Steam Review Scraper

- [Steam Review Scraper](#steam-review-scraper)
  - [Installation](#installation)
  - [Usage](#usage)
    - [search_game_id(search_term, all_results=False)](#search_game_idsearch_term-all_resultsfalse)
    - [get_game_ids(n, filter='topsellers')](#get_game_idsn-filtertopsellers)
    - [get_review_count(id)](#get_review_countid)
    - [get_game_review(id, language='default')](#get_game_reviewid-languagedefault)

## Installation
The package can be installed by:
```bash
>>> pip install steam-review-scaper
```


## Usage
### search_game_id(search_term, all_results=False)
>Return Dataframe of game ids of the search term from Steam’s search result page.
>
>**Args**:
>
>>**search_term** (str): Game name to search.
>**all_results** (bool, optional): Whether to return all games results of the search term or the top one result. Defaults to False.
>
>**Returns**:
>
>>**Dataframe**: Dataframe with two columns `game`  and `id`.

**Example:**
```python
>>> from steam_review_scraper import search_game_id
>>> search_game_id("Counter-Strike: Global Offensive")
                               game   id
0  Counter-Strike: Global Offensive  730
```


### get_game_ids(n, filter='topsellers')
>Return Dataframe of n games’ ids from Steam’s search result page.
>
>**Args**:
>
>>**n** (int): number of games to collect.
>**filter** (str, optional): filter for search results. Defaults to ‘topsellers’.
>
>**Returns**:
>
>>**Dataframe**: Dataframe with two columns `game` and `id`.

**Example:**
```python
>>> from steam_review_scraper import get_game_ids
>>> get_game_ids(5)
                               game       id
0                         BIOMUTANT   597820
1    Mass Effect™ Legendary Edition  1328670
2                         Destiny 2  1085660
3  Counter-Strike: Global Offensive      730
4                     Apex Legends™  1172470
```

### get_review_count(id)
>Return total number of reviews of default language.
>
>**Args**:
>
>>**id** (int or str): Game id.
>
>**Returns**:
>
>>**int**: Number of reviews.

**Example:**
```python
>>> from steam_review_scraper import get_review_count
>>> get_review_count(730)
1646275
```


### get_game_review(id, language='default')
>Collect all review for a given game.

>**Args**:
>
>>**id** (int or str): Game id 
**language** (str, optional): The language in which to get the reviews. Defaults to ‘default’,
which is the default language of your Steam account.
>
>**Returns**:
>
>>**Dataframe**: Dataframe for reviews with the following columns:

| name                | description                                           | dtype   |
|---------------------|-------------------------------------------------------|---------|
| user                | user name of the review                               | object  |
| playtime            | total playtime (in hours) the user spent on this game | float64 |
| user_link           | user's profile page url                               | object  |
| post_date           | review's post date                                    | object  |
| helpfulness         | number of people found this review helpful            | int64   |
| review              | review content                                        | object  |
| recommend           | whether the user recommend the game.                  | object  |
| early_access_review | whether this is an early access review.               | object  |

**Example:**

English reviews for Counter-Strike: Global Offensive:
* Game id 730 can be found using `search_game_id(‘Counter-Strike: Global Offensive’)` 
or from game’s Steam page url https://store.steampowered.com/app/730/CounterStrike_Global_Offensive.

```python
>>> from steam_review_scraper import get_game_review 
>>> reviews = get_game_review(730, language=’english’)
```
