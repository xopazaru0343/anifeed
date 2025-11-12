# anifeed
**WIP**: This project aims to:
1. fetch anime entries from a user's AniList or MyAnimeList profile
2. Match anime entries with Nyaa Torrents API using AI
3. Broadcast torrents to endpoints (RSS, JSON, HTML)

Project architecture is based in MVCS architecture and SOLID principles

# Documentation
https://alocks.github.io/anifeed/

# TODO
- [ ] Develop WebServer using socketify
    - [ ] Routers
      - [ ] routers for the controllers
    - [ ] Views
        - [ ] RSS serializer
        - [ ] JSON Serializer
        - [ ] DTO for the response shape in all serializer
    - [ ] Controllers
        - [ ] Feedcontroller for the views
        - [x] HealthController for uptime checks
        - [ ] AnimeController to cache requests
- [ ] Services
    - [ ] Workflows for the controller using existing services
    - [ ] Create service to filter data given from similarity_service
    - [ ] Create DTO for similarity_service and replace returned value from compute()
- [x] Create SQlite database for caching
  - [x] Connection class
  - [x] Create the database model
  - [x] CRUD for anime entries
