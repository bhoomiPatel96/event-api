# event-api
EventAPI is an event management system built using Django, Django REST Framework (DRF).
It uses PostgreSQL as the database. It provides role-based access control for users.

# Features
- User authentication (Admin/User roles)
- Role-based access control
- API endpoints using DRF to register users, create events, purchase tickets, and list events

# Built With
- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Authentication: Django’s built-in user model extended with role field

# How to Use
- With cURL.exe in cmd.
    - To register a user.
        - curl.exe -X POST {BASE_URL}/api/register/ -H "Content-Type: application/json" -d "{\"username\": \"{username}\", \"password\": \"{password}\", \"role\": \"{User|Admin}\"}"
    - To create an event. (Admin role only).
        - curl.exe -X POST {BASE_URL}/api/events/ -H "Content-Type: application/json" -u {admin_username}:{password} -d "{\"name\": \"{event_name}\", \"date\": \"{YYYY-MM-DD}\", \"total_tickets\": {integer}}"
        - Throws error when User role tries to post.
            - E.g.
                curl.exe -X POST http://127.0.0.1:8000/api/events/ -H "Content-Type: application/json" -u {user_username}:{password} -d "{\"name\": \"Conference1\", \"date\": \"2025-03-19\", \"total_tickets\": 100}"
            - Returns
                {"detail":"You do not have permission to perform this action."}
    - To get a list of events (Both User and Admin).
        - curl.exe -X GET {BASE_URL}/api/events/ -H "Content-Type: application/json" -u {username}:{password}
        - E.g. 
            curl.exe -X GET http://127.0.0.1:8000/api/events/ -H "Content-Type: application/json" -u {username}:{password}
        - Returns
            [
                {"id":1,"name":"Conference","date":"2025-03-19","total_tickets":100,"tickets_sold":2},
                {"id":2,"name":"Tech Expo","date":"2025-03-30","total_tickets":500,"tickets_sold":0}    
            ]
    - To purchase a ticket (User role only).
        - curl.exe -X POST {BASE_URL}/api/events/{event-id}/purchase/ -H "Content-Type: application/json" -u {user_username}:{password} -d "{\"quantity\": {Integer}}"
        - Returns a success message on successful ticket purchase.
            - E.g. 
                curl.exe -X POST http://127.0.0.1:8000/api/events/1/purchase/ -H "Content-Type: application/json" -u {user_username}:{password} -d "{\"quantity\": 1}"
            - Returns 
                {"message":"Tickets Purchased Successfully"}
        - Throws an error when Admin role tries to purchase ticket
            - E.g. 
                curl.exe -X POST http://127.0.0.1:8000/api/events/1/purchase/ -H "Content-Type: application/json" -u {admin_username}:{password} -d "{\"quantity\": 1}"
            - Returns
                {"detail":"You do not have permission to perform this action."}
        - Throws an error when event does not exist
            - E.g. 
                curl.exe -X POST http://127.0.0.1:8000/api/events/2/purchase/ -H "Content-Type: application/json" -u {user_username}:{password} -d "{\"quantity\": 1}"
            - Returns 
                {"error":"Purchasing for a non-existent event"}
        - Throws an error when Invalid quantity (negative or non-integer value) is passed
            - E.g.
                curl.exe -X POST http://127.0.0.1:8000/api/events/1/purchase/ -H "Content-Type: application/json" -u {user_username}:{password} -d "{\"quantity\": -4}"
            - Returns
                {"error":"Invalid ticket quantity"}
        - Throws an error if requested tickets are more than available tickets.
            - E.g.
                curl.exe -X POST http://127.0.0.1:8000/api/events/1/purchase/ -H "Content-Type: application/json" -u {user_username}:{password} -d "{\"quantity\": 100}"
            - Returns
                {"error":"Available tickets less than requested tickets"}


