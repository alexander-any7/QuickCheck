# Hacker News Web App (Python Developer Case Study)

This web app provides a user-friendly interface to navigate and explore news items from Hacker News. It is built using [Django](https://www.djangoproject.com/), a high-level Python web framework. The app includes features such as listing the latest news items, filtering by item type, searching by text, and exposing an API for data consumption. It also implements additional functionality like displaying top-level items and their children (comments) on a detail page.

## Installation

1. Create a virtual environment and activate it.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the database migrations using the command `python manage.py migrate`.
4. Start the server by running `python manage.py runserver --noreload`.  The `--noreload` flag is necessary because it disables the auto-reloader so it doesn't run scheduled jobs twice.
5. Access the web app in your browser at `http://localhost:8000`.

*Additionally, please note that retrieving the first 100 posts from the Hacker News API takes less than 2 minutes. However, fetching the top-level children (comments) of each post can take close to 30 minutes due to the potentially large number of comments associated with each post.*

## Testing
There are 21 tests in total. They include tests for Registration, Login, Retrieving one and all posts, and Updating and Deleting posts by Authenticated users.

## Features

- Scheduled Jobs: The app includes two scheduled jobs; one that syncs the published news items from Hacker News to the local database every 5 minutes. It retrieves the latest 100 items initially and continuously syncs new items thereafter. The second gets all the top level children of each post and also syncs to the db.

- List View: The app provides a list view (the homepage) to display the latest news items. It supports pagination for efficient browsing.

- Filtering: Users can filter the news items by their type. Available types include 'job', 'story', 'poll', and 'pollopt'. Filtering can be done using the query parameter `type` in the URL.

- Search: The app includes a search box in the list view that allows users to search for news items by text content. Searching can be performed by entering keywords in the search box.

- API: The app exposes an API to access the news items. The API provides the following endpoints:

  - `GET /api/all-posts/`: Retrieves a list of news items. It accepts optional query parameters for filtering by type (`type`) and searching by text content (`search`).

  - `POST /api/add-post/`: Adds a new news item to the database. Requires authentication and authorization.

- Bonus Features: The app displays top-level items in the list view and provides a detail page (`/post/<post_id>`) that shows their children (comments). The API allows updating and deleting items created through the API.
